#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Mixin class containing Lineage specific methods

To be used by OpenMetadata class
"""
import functools
import json
import traceback
from typing import Generic, List, Optional, Set, Type, TypeVar

from pydantic import BaseModel
from requests.utils import quote

from metadata.generated.schema.api.createEventPublisherJob import (
    CreateEventPublisherJob,
)
from metadata.generated.schema.entity.data.query import Query
from metadata.generated.schema.system.eventPublisherJob import EventPublisherResult
from metadata.ingestion.ometa.client import REST, APIError
from metadata.utils.elasticsearch import ES_INDEX_MAP
from metadata.utils.logger import ometa_logger

logger = ometa_logger()

T = TypeVar("T", bound=BaseModel)


class ESMixin(Generic[T]):
    """
    OpenMetadata API methods related to Elasticsearch.

    To be inherited by OpenMetadata
    """

    client: REST

    fqdn_search = (
        "/search/fieldQuery?fieldName=fullyQualifiedName&fieldValue={fqn}&from={from_}"
        "&size={size}&index={index}"
    )

    @functools.lru_cache(maxsize=512)
    def _search_es_entity(
        self,
        entity_type: Type[T],
        query_string: str,
        fields: Optional[str] = None,
    ) -> Optional[List[T]]:
        """
        Run the ES query and return a list of entities that match. It does an extra query to the OM API with the
        requested fields per each entity found in ES.
        :param entity_type: Entity to look for
        :param query_string: Query to run
        :return: List of Entities or None
        """
        response = self.client.get(query_string)

        if response:
            if fields:
                fields = fields.split(",")
            return [
                self.get_by_name(
                    entity=entity_type,
                    fqn=hit["_source"]["fullyQualifiedName"],
                    fields=fields,
                )
                for hit in response["hits"]["hits"]
            ] or None

        return None

    def _get_entity_from_es(
        self, entity: Type[T], query_string: str, fields: Optional[list] = None
    ) -> Optional[T]:
        """Fetch an entity instance from ES"""

        try:
            entity_list = self._search_es_entity(
                entity_type=entity, query_string=query_string, fields=fields
            )
            for instance in entity_list or []:
                return instance
        except Exception as err:
            logger.debug(traceback.format_exc())
            logger.warning(f"Could not get {entity.__name__} info from ES due to {err}")

        return None

    def es_search_from_fqn(
        self,
        entity_type: Type[T],
        fqn_search_string: str,
        from_count: int = 0,
        size: int = 10,
        fields: Optional[str] = None,
    ) -> Optional[List[T]]:
        """
        Given a service_name and some filters, search for entities using ES

        :param entity_type: Entity to look for
        :param fqn_search_string: string used to search by FQN. E.g., service.*.schema.table
        :param from_count: Records to expect
        :param size: Number of records
        :param fields: Comma separated list of fields to be returned
        :return: List of entities
        """
        query_string = self.fqdn_search.format(
            fqn=fqn_search_string,
            from_=from_count,
            size=size,
            index=ES_INDEX_MAP[entity_type.__name__],  # Fail if not exists
        )

        try:
            response = self._search_es_entity(
                entity_type=entity_type, query_string=query_string, fields=fields
            )
            return response
        except KeyError as err:
            logger.debug(traceback.format_exc())
            logger.warning(
                f"Cannot find the index in ES_INDEX_MAP for {entity_type.__name__}: {err}"
            )
        except Exception as exc:
            logger.debug(traceback.format_exc())
            logger.warning(
                f"Elasticsearch search failed for query [{query_string}]: {exc}"
            )
        return None

    def reindex_es(
        self,
        config: CreateEventPublisherJob,
    ) -> Optional[EventPublisherResult]:
        """
        Method to trigger elasticsearch reindex
        """
        try:
            resp = self.client.post(path="/search/reindex", data=config.json())
            return EventPublisherResult(**resp)
        except APIError as err:
            logger.debug(traceback.format_exc())
            logger.debug(f"Failed to trigger es reindex job due to {err}")
            return None

    def get_reindex_job_status(self, job_id: str) -> Optional[EventPublisherResult]:
        """
        Method to fetch the elasticsearch reindex job status
        """
        try:
            resp = self.client.get(path=f"/search/reindex/{job_id}")
            return EventPublisherResult(**resp)
        except APIError as err:
            logger.debug(traceback.format_exc())
            logger.debug(f"Failed to fetch reindex job status due to {err}")
            return None

    @staticmethod
    def get_query_with_lineage_filter(service_name: str) -> str:
        query_lineage_filter = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"processedLineage": True}},
                        {"term": {"service.name.keyword": service_name}},
                    ]
                }
            }
        }
        return quote(json.dumps(query_lineage_filter))

    @functools.lru_cache(maxsize=12)
    def es_get_queries_with_lineage(self, service_name: str) -> Optional[Set[str]]:
        """Get a set of query checksums that have already been processed for lineage"""
        try:
            resp = self.client.get(
                f"/search/query?q=&index={ES_INDEX_MAP[Query.__name__]}"
                "&include_source_fields=checksum&include_source_fields="
                f"processedLineage&query_filter={self.get_query_with_lineage_filter(service_name)}"
            )
            return {elem["_source"]["checksum"] for elem in resp["hits"]["hits"]}

        except APIError as err:
            logger.debug(traceback.format_exc())
            logger.warning(f"Could not get queries from ES due to [{err}]")
            return None

        except Exception as err:
            logger.debug(traceback.format_exc())
            logger.warning(f"Unknown error extracting results from ES query [{err}]")
            return None
