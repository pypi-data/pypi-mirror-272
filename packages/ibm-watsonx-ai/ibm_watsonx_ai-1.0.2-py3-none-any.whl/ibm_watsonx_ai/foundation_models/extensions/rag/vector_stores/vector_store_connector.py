#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from enum import Enum

import logging
from typing import Any

from ibm_watsonx_ai.foundation_models.extensions.rag.vector_stores.base_vector_store import (
    BaseVectorStore,
)
from ibm_watsonx_ai.foundation_models.extensions.rag.vector_stores.langchain_vector_store_adapter import (
    LangchainVectorStoreAdapter,
)
from ibm_watsonx_ai.foundation_models.extensions.rag.utils.utils import (
    get_ssl_certificate,
)

from langchain_core.vectorstores import VectorStore as LangchainVectorStore

logger = logging.getLogger(__name__)


class VectorStoreDataSourceType(str, Enum):
    ELASTICSEARCH = "elasticsearch"
    CHROMA = "chroma"
    MILVUS = "milvus"
    UNDEFINED = "undefined"


class VectorStoreConnector:
    """Creates proper vector store client using provided properties.

    :param properties: dictionary with all required key values to establish connection.
    :type properties: dict
    """

    def __init__(self, properties: dict | None = None) -> None:
        self.properties: dict = (
            properties.copy() if isinstance(properties, dict) else {}
        )

    @staticmethod
    def get_type_from_langchain_vector_store(
        langchain_vector_store: Any,
    ) -> VectorStoreDataSourceType:
        """Returns ``DataSourceType`` for concrete langchain ``VectorStore`` class.

        :param langchain_vector_store: vector store object from Langchain
        :type langchain_vector_store: Any

        :return: DataSourceType name
        :rtype: VectorStoreDataSourceType
        """
        vs_type = langchain_vector_store.__class__.__name__

        match vs_type:
            case "ElasticsearchStore":
                return VectorStoreDataSourceType.ELASTICSEARCH
            case "Chroma":
                return VectorStoreDataSourceType.CHROMA
            case "Milvus":
                return VectorStoreDataSourceType.MILVUS
            case _:
                return VectorStoreDataSourceType.UNDEFINED

    def get_from_type(self, type: VectorStoreDataSourceType) -> BaseVectorStore:
        """Gets a vector store based on provided type (matching from DataSource names from SDK API).

        :param type: DataSource type string from SDK API
        :type type: VectorStoreDataSourceType

        :raises TypeError: unsupported type
        :return: proper BaseVectorStore type constructed from properties
        :rtype: BaseVectorStore
        """
        match type:
            case VectorStoreDataSourceType.ELASTICSEARCH:
                return self.get_elasticsearch()
            case VectorStoreDataSourceType.CHROMA:
                return self.get_chroma()
            case VectorStoreDataSourceType.MILVUS:
                return self.get_milvus()
            case _:
                raise TypeError("Data source type not supported.")

    def get_langchain_adapter(              # type: ignore[return]
        self, langchain_vector_store: Any
    ) -> LangchainVectorStoreAdapter | None:  
        """Creates adapter for concrete vector store from langchain.

        :param langchain_vector_store: object that is subclass of Langchain VectorStore
        :type langchain_vector_store: Any

        :raises ImportError: langchain required
        :return: proper adapter for the vector store
        :rtype: LangchainVectorStoreAdapter
        """

        if isinstance(langchain_vector_store, LangchainVectorStore):
            return LangchainVectorStoreAdapter(vector_store=langchain_vector_store)

    def get_chroma(self) -> LangchainVectorStoreAdapter:
        """Creates Chroma in-memory vector store.

        :raises ImportError: langchain required
        :return: vector store adapter for langchain's Chroma
        :rtype: LangchainVectorStoreAdapter
        """
        from langchain_community.vectorstores import Chroma

        parsed_params = self.properties
        return LangchainVectorStoreAdapter(Chroma(**parsed_params))

    def get_milvus(self) -> LangchainVectorStoreAdapter:
        """Creates Milvus vector store.

        :raises ImportError: langchain required
        :return: vector store adapter for langchain's Milvus
        :rtype: LangchainVectorStoreAdapter
        """
        from langchain_community.vectorstores import Milvus

        parsed_params = self.properties
        return LangchainVectorStoreAdapter(Milvus(**parsed_params))

    def get_elasticsearch(self) -> LangchainVectorStoreAdapter:
        """Creates Elasticsearch vector store.

        :raises ImportError: langchain required
        :return: vector store adapter for langchain's Elasticsearch
        :rtype: LangchainVectorStoreAdapter
        """
        from langchain_community.vectorstores.elasticsearch import (
            ElasticsearchStore,
            SparseRetrievalStrategy,
            ApproxRetrievalStrategy,
            ExactRetrievalStrategy,
            BaseRetrievalStrategy,
        )

        parsed_params = self.properties

        # Always use empty es_params if not provided
        parsed_params["es_params"] = self.properties.pop("es_params", {})

        # Drop unnecessary stuff from connection asset if they are present
        parsed_params.pop("auth_method", None)
        parsed_params.pop("use_anonymous_access", None)

        # Parse ES connection data - select proper connection type
        # Connecting by 'url': username/password or api_key
        if {"url"}.issubset(parsed_params):
            # Get URL of ES instance
            parsed_params["es_url"] = parsed_params.pop("url")

            # Detect credentials given in connection asset
            if {"username", "password"}.issubset(parsed_params):
                # Connect by username and password extracted from connection
                parsed_params["es_user"] = parsed_params.pop("username")
                parsed_params["es_password"] = parsed_params.pop("password")

                parsed_params.pop("api_key", None)
            elif {"api_key"}.issubset(parsed_params):
                # Connect by api key
                parsed_params["es_api_key"] = parsed_params.pop("api_key")

                parsed_params.pop("username", None)
                parsed_params.pop("password", None)
            else:
                raise ValueError(
                    """To connect to given hostname ['url'] provide
                                either ['username', 'password'] or ['api_key'].
                                Make sure those fields are present in connection details or parameters given
                                upon VectorStore initialization. """
                )
        elif {"es_url"}.issubset(parsed_params):
            if {"es_user", "es_password"}.issubset(parsed_params):
                pass
            elif {"es_api_key"}.issubset(parsed_params):
                pass
            else:
                raise ValueError(
                    """To connect to given hostname ['es_url'] provide
                                either ['es_user', 'es_password'] or ['es_api_key'].
                                Make sure those fields are present in parameters given
                                upon VectorStore initialization. """
                )
        # Connecting by '(es_)cloud_id' to Elasticsearch cloud
        elif {"cloud_id", "api_key"}.issubset(parsed_params):
            parsed_params["es_cloud_id"] = parsed_params.pop("cloud_id", None)
            parsed_params["es_api_key"] = parsed_params.pop("api_key", None)
        elif {"es_cloud_id", "es_api_key"}.issubset(parsed_params):
            pass
        else:
            raise ValueError(
                """Connection data was not sufficent. Either provide:
                             - ['url', 'username', 'password'],
                             - ['url', 'api_key'],
                             - ['cloud_id', 'api_key']
                             or
                             - ['es_url', 'es_user', 'es_password'],
                             - ['es_url', 'es_api_key'],
                             - ['es_cloud_id', 'es_api_key'],
                             in your connection asset or in params for VectorStore."""
            )

        if not {"index_name"}.issubset(parsed_params):
            raise ValueError("Provide 'index_name' in params.")

        # Parse SSL certificate
        ssl_certificate_content = parsed_params.pop("ssl_certificate", None)

        if ssl_certificate_content:
            ssl_certificate_content = get_ssl_certificate(ssl_certificate_content)
            cert_file_path = "es_conn_temp.crt"
            with open(cert_file_path, "w") as file:
                file.write(ssl_certificate_content)

            parsed_params["es_params"]["ca_certs"] = cert_file_path

            logger.info(
                f"SSL certificate was found and written to {cert_file_path}. It will be used for the connection for the VectorStore."
            )

        # Determine retrieval strategy type from parameters
        if "strategy" not in parsed_params or not isinstance(
            parsed_params["strategy"], BaseRetrievalStrategy
        ):
            if "model_id" in parsed_params:
                parsed_params["strategy"] = SparseRetrievalStrategy(
                    parsed_params.pop("model_id")
                )
            elif "query_model_id" in parsed_params:
                parsed_params["strategy"] = ApproxRetrievalStrategy(
                    parsed_params.pop("query_model_id")
                )
            else:
                parsed_params["strategy"] = ExactRetrievalStrategy()

        es_store = ElasticsearchStore(
            **parsed_params,
        )

        return LangchainVectorStoreAdapter(es_store)
