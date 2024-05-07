#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import pytest

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models.extensions.rag import VectorStore
from ibm_watsonx_ai.tests.utils import get_wml_credentials, get_db_credentials

from langchain_community.embeddings import DeterministicFakeEmbedding


@pytest.fixture(scope="class", name='rag_client')
def fixture_setup_rag_client():
    credentials = get_wml_credentials()
    project_id = credentials.project_id
    client = APIClient(credentials, project_id=project_id)
    return client


@pytest.fixture(scope="class", name='vectorstore_elasticsearch')
def fixture_setup_vectorstore_elasticsearch(rag_client):

    # Prepare elasticsearch
    es_credentials = get_db_credentials('elasticsearch')

    # Create connection
    elasticsearch_data_source_type_id = rag_client.connections.get_datasource_type_uid_by_name('elasticsearch')
    details = rag_client.connections.create(
        {
            rag_client.connections.ConfigurationMetaNames.NAME: "ES Connection",
            rag_client.connections.ConfigurationMetaNames.DESCRIPTION: "connection description",
            rag_client.connections.ConfigurationMetaNames.DATASOURCE_TYPE: elasticsearch_data_source_type_id,
            rag_client.connections.ConfigurationMetaNames.PROPERTIES:
            {
                "password": es_credentials['password'],
                "url": es_credentials['url'],
                "username": es_credentials['username'],
                "use_anonymous_access": 'false',
                'ssl_certificate': es_credentials['base64_cert']
            }
        }
    )

    connection_id = rag_client.connections.get_uid(details)

    # Create VectorStore (that uses elasticsearch) for testing
    vector_store = VectorStore(rag_client, connection_id=connection_id,
                               params={'index_name': 'test_vector_store_index'})
    vector_store.set_embeddings(DeterministicFakeEmbedding(size=1))

    yield vector_store

    rag_client.connections.delete(connection_id)


@pytest.fixture(scope='function', name='ids_to_delete_es')
def fixture_ids_to_delete_es(vectorstore_elasticsearch):
    ids = []
    yield ids
    vectorstore_elasticsearch.delete(ids)
