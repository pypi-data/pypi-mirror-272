#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watsonx_ai.foundation_models.embeddings.base_embeddings import BaseEmbeddings


class DebugEmbeddings(BaseEmbeddings):
    """Embeddings used for debugging/tests.
    Always return the same 1 element list with value.

    :param val: default value to set up
    :type val: float
    """

    def __init__(self, val: float = 0.0) -> None:
        super().__init__()
        self.val = val

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[self.val] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return [self.val]

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({'val': self.val})
        return d
