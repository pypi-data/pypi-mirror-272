#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from langchain_core.documents import Document


class TestVectorStoreElasticsearch:
    """
    These tests cover:
    - Elasticsearch support for VectorStore class
    - base vector store functionalities
    - duplicate handling

    Embedding is done via fake/random embedding from langchain.
    It is deterministic and should give same results on all devices or environments.
    """

    def test_01_add_and_retrieve_documents(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            {'content': 'aaa', 'metadata': {'url': 'ibm.com'}},
            {'content': 'bbb', 'metadata': {'url': 'ibm_test.com'}},
            {'content': 'ccc'}
        ]

        ids_to_delete_es.extend(vectorstore_elasticsearch.add_documents(docs))

        result = vectorstore_elasticsearch.search('bbb', k=1)

        assert len(result) == 1, "since k=1"

        assert result[0].page_content == docs[1]['content'], "should be 'bbb'"
        assert result[0].metadata['url'] == docs[1]['metadata']['url'], "should be 'ibm_test.com'"

    def test_02_add_and_retrieve_documents_empty(self, vectorstore_elasticsearch):
        result = vectorstore_elasticsearch.search('text', k=1)

        assert len(result) == 0

    def test_03_add_and_delete_documents(self, vectorstore_elasticsearch):
        docs = [
            {'content': 'aaa', 'metadata': {'url': 'ibm.com'}},
            {'content': 'bbb', 'metadata': {'url': 'ibm_test.com'}},
            {'content': 'ccc'}
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        result = vectorstore_elasticsearch.search('search query', k=5)

        assert len(result) == 3, "k=5 but 3 were added"

        vectorstore_elasticsearch.delete(ids)
        result = vectorstore_elasticsearch.search('search query', k=3)

        assert len(result) == 0, "should be 0 because deleted"

    def test_04_add_and_delete_documents_wrong_ids(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            {'content': 'aaa', 'metadata': {'url': 'ibm.com'}},
            {'content': 'bbb', 'metadata': {'url': 'ibm_test.com'}},
            {'content': 'ccc'}
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        ids_to_delete_es.extend(ids)
        result = vectorstore_elasticsearch.search('search query', k=5)

        assert len(result) == 3

        vectorstore_elasticsearch.delete(['wrong id1', 'wrong id2', 'wrong id3'])
        result = vectorstore_elasticsearch.search('search query', k=5)

        assert len(result) == 3, "after delete of not found ids, the number still should be 3"

    def test_05_add_incorrect_content(self, vectorstore_elasticsearch):
        docs = [
            {'file_content': 'aaa', 'metadata': {'url': 'ibm.com'}},
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)

        assert len(ids) == 0, "0 since 'file_content' should be 'content'"

        result = vectorstore_elasticsearch.search('search query', k=1)

        assert len(result) == 0, "search should also return 0"

    def test_06_add_document_from_langchain(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            Document(page_content="abc", metadata={'url': 'ibm.com'}),
            {'content': 'def'},
            {'error': 'error'}
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        ids_to_delete_es.extend(ids)

        assert len(ids) == 2, "both Document 'abc' and dict 'def'"

        result = vectorstore_elasticsearch.search('search query', k=3)

        assert len(result) == 2, "two docs were added, two docs should be found"

        assert result[0].page_content == docs[0].page_content, "should be 'abc'"
        assert result[0].metadata['url'] == docs[0].metadata['url'], "should be 'ibm.com'"

        assert result[1].page_content == docs[1]['content'], "should be 'def'"
        assert result[1].metadata == {}, "{'content': 'def'} had no metadata"

    def test_07_add_document_duplicates(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            Document(page_content="abc", metadata={'url': 'ibm.com/test/1'}),
            Document(page_content="abc", metadata={'url': 'ibm.com/test/2'}),
            {'content': 'abc'},
            {'content': 'abc', 'metadata': {'url': 'ibm.com/test/3'}},
            {'error': 'error'}
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        ids_to_delete_es.extend(ids)

        assert len(ids) == 1, "1 since 'abc' page content did repeat"

        result = vectorstore_elasticsearch.search('search query', k=3)

        assert len(result) == 1, "verify the search results with num of ids"

        assert result[0].page_content == docs[3]['content'], "search result content should be 'abc'"
        assert result[0].metadata['url'] == docs[3]['metadata']['url'], "metadata should be '{'url': 'ibm.com/test/3'}' because last one should be added"

    def test_08_add_document_strings(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            "Hello there!",
            {'content': 'Hello there!'},
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        ids_to_delete_es.extend(ids)

        assert len(ids) == 1, "1 since string and content of dict is the same"

        result = vectorstore_elasticsearch.search('search query', k=5)

        assert len(result) == 1, "same for search"

        assert result[0].page_content == docs[0], "should be 'Hello there!'"

    def test_09_add_document_strings(self, vectorstore_elasticsearch, ids_to_delete_es):
        docs = [
            "Hello there!",
            "Bye, bye!"
        ]

        ids = vectorstore_elasticsearch.add_documents(docs)
        ids_to_delete_es.extend(ids)

        assert len(ids) == 2, "2 since two strings were added"

        result = vectorstore_elasticsearch.search('search query', k=5)

        assert len(result) == 2, "same for search"

        assert result[0].page_content == docs[0], "should be 'Hello there!'"
        assert result[1].page_content == docs[1], "should be 'Bye, bye!'"
