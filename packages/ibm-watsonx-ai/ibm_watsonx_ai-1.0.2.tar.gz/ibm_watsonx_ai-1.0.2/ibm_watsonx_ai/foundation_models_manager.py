#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations

from typing import TYPE_CHECKING, Generator
import warnings

from ibm_watsonx_ai.wml_resource import WMLResource
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.messages.messages import Messages
from ibm_watsonx_ai.wml_client_error import WMLClientError

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient


class FoundationModelsManager(WMLResource):
    def __init__(self, client: APIClient):
        WMLResource.__init__(self, __name__, client)
        self._client = client

    def _get_spec(
        self,
        url: str,
        operation_name: str,
        error_msg_id: str,
        model_id: str | None = None,
        limit: int | None = 50,
        filters: str | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict | None:
        params = self._client._params(skip_userfs=True)
        if filters:
            params.update({"filters": filters})

        try:
            if model_id:
                result = self._get_with_or_without_limit(
                    url,
                    limit=None,
                    op_name=operation_name,
                    query_params=params,
                    _all=True,
                    _async=False,
                )

                if isinstance(model_id, ModelTypes):
                    model_id = model_id.value

                model_res = [
                    res for res in result["resources"] if res["model_id"] == model_id
                ]

                if len(model_res) > 0:
                    return model_res[0]
                else:
                    return None
            else:
                return self._get_with_or_without_limit(
                    url=url,
                    limit=limit,
                    op_name=operation_name,
                    query_params=params,
                    _async=asynchronous,
                    _all=get_all,
                )
        except WMLClientError as e:
            raise WMLClientError(
                Messages.get_message(
                    self._client.credentials.url,
                    message_id=error_msg_id,
                ),
                e,
            )

    def get_model_specs(
        self,
        model_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict | Generator | None:
        """
        Operations to retrieve the list of deployed foundation models specifications.

        :param model_id: Id of the model, defaults to None (all models specs are returned).
        :type model_id: str or ModelTypes, optional

        :param limit:  limit number of fetched records
        :type limit: int, optional

        :param asynchronous:  if True, it will work as a generator
        :type asynchronous: bool, optional

        :param get_all:  if True, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: list of deployed foundation model specs
        :rtype: dict or generator

        **Example**

        .. code-block:: python

            # GET ALL MODEL SPECS
            client.foundation_models.get_model_specs()

            # GET MODEL SPECS BY MODEL_ID
            client.foundation_models.get_model_specs(model_id="google/flan-ul2")
        """
        return self._get_spec(
            url=self._client.service_instance._href_definitions.get_fm_specifications_href(),
            operation_name="Get available foundation models",
            error_msg_id="fm_prompt_tuning_no_model_specs",
            model_id=model_id,
            limit=limit,
            asynchronous=asynchronous,
            get_all=get_all,
        )

    def get_custom_model_specs(
        self,
        model_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict | Generator | None:
        """Get details on available custom model(s) as dict or as generator (``asynchronous``).
        If ``asynchronous`` or ``get_all`` is set, then ``model_id`` is ignored.

        :param model_id: Id of the model, defaults to None (all models specs are returned).
        :type model_id: str, optional

        :param limit:  limit number of fetched records
        :type limit: int, optional

        :param asynchronous:  if True, it will work as a generator
        :type asynchronous: bool, optional

        :param get_all:  if True, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: details of supported custom models, None if for given model_id non is found
        :rtype: dict or generator

        **Example**

        .. code-block:: python

            client.foundation_models.get_custom_models_spec()
            client.foundation_models.get_custom_models_spec()
            client.foundation_models.get_custom_models_spec(model_id='mistralai/Mistral-7B-Instruct-v0.2')
            client.foundation_models.get_custom_models_spec(limit=20)
            client.foundation_models.get_custom_models_spec(limit=20, get_all=True)
            for spec in client.foundation_models.get_custom_model_specs(limit=20, asynchronous=True, get_all=True):
                print(spec, end="")

        """
        warnings.warn(
            "Model needs to be first stored via client.repository.store_model(model_id, meta_props=metadata)"
            " and deployed via client.deployments.create(asset_id, metadata) to be used."
        )

        return self._get_spec(
            url=self._client.service_instance._href_definitions.get_fm_custom_foundation_models_href(),
            operation_name="Get custom model specs",
            error_msg_id="custom_models_no_model_specs",
            model_id=model_id,
            limit=limit,
            asynchronous=asynchronous,
            get_all=get_all,
        )

    def get_embeddings_model_specs(
        self,
        model_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict | Generator | None:
        """
        Operation to retrieve the embeddings model specs.

        :param model_id: Id of the model, defaults to None (all models specs are returned).
        :type model_id: str, optional

        :param limit:  limit number of fetched records
        :type limit: int, optional

        :param asynchronous:  if True, it will work as a generator
        :type asynchronous: bool, optional

        :param get_all:  if True, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: embeddings model specs
        :rtype: dict or generator

        **Example**

        .. code-block:: python

            client.foundation_models.get_embeddings_model_specs()
            client.foundation_models.get_embeddings_model_specs('ibm/slate-125m-english-rtrvr')
        """
        return self._get_spec(
            url=self._client.service_instance._href_definitions.get_fm_specifications_href(),
            operation_name="Get available embedding models",
            error_msg_id="fm_prompt_tuning_no_model_specs",
            model_id=model_id,
            filters="function_embedding",
            limit=limit,
            asynchronous=asynchronous,
            get_all=get_all,
        )

    def get_model_specs_with_prompt_tuning_support(
        self,
        model_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict | Generator | None:
        """
        Operations to query the details of the deployed foundation models with prompt tuning support.

        :param model_id: Id of the model, defaults to None (all models specs are returned).
        :type model_id: str, optional

        :param limit:  limit number of fetched records
        :type limit: int, optional

        :param asynchronous:  if True, it will work as a generator
        :type asynchronous: bool, optional

        :param get_all:  if True, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: list of deployed foundation model specs with prompt tuning support
        :rtype: dict or generator

        **Example**

        .. code-block:: python

            client.foundation_models.get_model_specs_with_prompt_tuning_support()
            client.foundation_models.get_model_specs_with_prompt_tuning_support('google/flan-t5-xl')
        """
        return self._get_spec(
            url=self._client.service_instance._href_definitions.get_fm_specifications_href(),
            operation_name="Get available foundation models",
            error_msg_id="fm_prompt_tuning_no_model_specs",
            model_id=model_id,
            filters="function_prompt_tune_trainable",
            limit=limit,
            asynchronous=asynchronous,
            get_all=get_all,
        )

    def get_model_lifecycle(self, model_id: str) -> list | None:
        """
        Operation to retrieve the list of model lifecycle data.

        :param model_id: the type of model to use
        :type model_id: str

        :return: list of deployed foundation model lifecycle data
        :rtype: list

        **Example**

        .. code-block:: python

            client.foundation_models.get_model_lifecycle(
                model_id="ibm/granite-13b-instruct-v2"
                )
        """
        model_spec = self.get_model_specs(model_id)
        return model_spec.get("lifecycle") if model_spec is not None else None
