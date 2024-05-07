#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations

from typing import TYPE_CHECKING, cast, Any

if TYPE_CHECKING:
    import langchain
    from langchain.prompts import PromptTemplate as LcPromptTemplate
from dataclasses import dataclass
from datetime import datetime

import pandas

import ibm_watsonx_ai._wrappers.requests as requests
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.wml_client_error import (
    WMLClientError,
    ValidationError,
    InvalidValue,
    InvalidMultipleArguments,
    PromptVariablesError,
)
from ibm_watsonx_ai.wml_resource import WMLResource
from ibm_watsonx_ai.foundation_models.utils.enums import (
    ModelTypes,
    PromptTemplateFormats,
)
from ibm_watsonx_ai.foundation_models.utils.utils import TemplateFormatter


@dataclass
class PromptTemplateLock:
    """Storage for lock object."""

    locked: bool
    locked_by: str | None = None


class PromptTemplate:
    """Storage for prompt template parameters.

    :param prompt_id: Id of prompt template, defaults to None.
    :type prompt_id: str, attribute setting not allowed

    :param created_at: Time the prompt was created (UTC), defaults to None.
    :type created_at: str, attribute setting not allowed

    :param lock: Locked state of asset, defaults to None.
    :type lock: Optional[PromptTemplateLock], attribute setting not allowed

    :param is_template: True if prompt is a template, False otherwise; defaults to None.
    :type is_template: Optional[bool], attribute setting not allowed

    :param name: Prompt template name, defaults to None.
    :type name: str, optional

    :param model_id: Foundation model id, defaults to None.
    :type model_id: Optional[ModelTypes], optional

    :param model_params: Model parameters, defaults to None.
    :type model_params: dict, optional

    :param template_version: Semvar version for tracking in IBM AI Factsheets, defaults to None.
    :type template_version: str, optional

    :param task_ids: List of task ids, defaults to None.
    :type task_ids: Optional[List[str]], optional

    :param description: Prompt template asset description, defaults to None.
    :type description: str, optional

    :param input_text: Input text for prompt, defaults to None.
    :type input_text: str, optional

    :param input_variables: Input variables can be present in fields: `instruction`,
                            `input_prefix`, `output_prefix`, `input_text`, `examples`
                            and are identified by braces ('{' and '}'), defaults to None.
    :type input_variables: (list | dict[str, dict[str, str]]), optional

    :param instruction: Instruction for model, defaults to None.
    :type instruction: str, optional

    :param input_prefix: Prefix string placed before input text, defaults to None.
    :type input_prefix: str, optional

    :param output_prefix: Prefix before model response, defaults to None.
    :type output_prefix: str, optional

    :param examples: Examples may help the model to adjust the response; [[input1, output1], ...], defaults to None.
    :type examples: list[list[str]]], optional

    :param validate_template: If True, the Prompt Template is validated for the presence of input variables, defaults to True.
    :type validate_template: bool, optional

    **Examples**

    Example of invalid Prompt Template:

    .. code-block:: python

        prompt_template = PromptTemplate(input_text='What are the most famous monuments in ?',
                                         input_variables=['country'])

        Traceback (most recent call last):
            ...
        ValidationError: Invalid prompt template; check for mismatched or missing input variables. Missing input variable: {'country'}

    Example of valid Prompt Template:

    .. code-block:: python

        prompt_template = PromptTemplate(input_text='What are the most famous monuments in {country}?',
                                         input_variables=['country'])

    """

    def __init__(
        self,
        name: str | None = None,
        model_id: ModelTypes | None = None,
        model_params: dict | None = None,
        template_version: str | None = None,
        task_ids: list[str] | None = None,
        description: str | None = None,
        input_text: str | None = None,
        input_variables: list | dict[str, dict[str, str]] | None = None,
        instruction: str | None = None,
        input_prefix: str | None = None,
        output_prefix: str | None = None,
        examples: list[list[str]] | None = None,
        validate_template: bool = True,
        **kwargs: Any,
    ) -> None:
        self.name = name
        self._prompt_id: str | None = None
        self._created_at: int | None = None
        self._lock: PromptTemplateLock | None = None
        self._is_template: bool | None = None
        self.model_id: ModelTypes | str | None = model_id
        if isinstance(self.model_id, ModelTypes):
            self.model_id = self.model_id.value
        self.model_params = (
            model_params.copy() if model_params is not None else model_params
        )
        self.task_ids = task_ids.copy() if task_ids is not None else task_ids
        self.template_version = template_version
        self.description = description
        self.input_text = input_text
        self.input_variables = (
            input_variables.copy() if input_variables is not None else input_variables
        )
        self.instruction = instruction
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
        self.examples = examples.copy() if examples is not None else examples

        supported_pt_kwargs = ["input_mode", "external_information"]
        unsupported_pt_keys = [
            key for key in kwargs.keys() if key not in supported_pt_kwargs
        ]
        if unsupported_pt_keys:
            raise WMLClientError(
                f"Unsupported kwargs: {', '.join(unsupported_pt_keys)}. "
                f"Supported kwargs are: {', '.join(supported_pt_kwargs)}."
            )

        for key, value in kwargs.items():
            setattr(self, key, value)

        # template validation
        if validate_template:
            self._validation()

    def __repr__(self) -> str:
        args = [
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_") and value is not None
        ]
        return f"{type(self).__name__}({ ', '.join(args)})"

    @property
    def prompt_id(self) -> str | None:
        return self._prompt_id

    @property
    def created_at(self) -> str:
        self._created_at = cast(int, self._created_at)
        return str(datetime.fromtimestamp(self._created_at / 1000)).split(".")[0]

    @property
    def lock(self) -> PromptTemplateLock | None:
        return self._lock

    @property
    def is_template(self) -> bool | None:
        return self._is_template

    def _validation(self) -> None:
        """Validate template structure.

        :raises ValidationError: raises when input_variables does not fit placeholders in input body.
        """
        input_variables = (
            self.input_variables if self.input_variables is not None else []
        )
        template_text = " ".join(
            filter(None, [self.instruction, self.input_prefix, self.output_prefix])
        )
        if self.examples:
            for example in self.examples:
                template_text += " ".join(example)
        try:

            def _validate(input_text: str) -> None:
                dummy_inputs = {
                    input_variable: "wx" for input_variable in input_variables
                }
                TemplateFormatter().format(
                    "".join([template_text, input_text]), **dummy_inputs
                )

            if self.input_text:
                _validate(template_text + self.input_text)
            else:
                if template_text:
                    _validate(template_text)
        except KeyError as key:
            raise ValidationError(
                str(key),
                additional_msg="One can turn off validation step setting `validate_template` to False.",
            )


class PromptTemplateManager(WMLResource):
    """Instantiate the prompt template manager.

    :param credentials: Credentials to watsonx.ai instance.
    :type credentials: Credentials

    :param project_id: ID of project
    :type project_id: str

    :param space_id: ID of project
    :type space_id: str

    :param verify: user can pass as verify one of following:
        - the path to a CA_BUNDLE file
        - the path of directory with certificates of trusted CAs
        - `True` - default path to truststore will be taken
        - `False` - no verification will be made
    :type verify: bool or str, optional

    .. note::
        One of these parameters is required: ['project_id ', 'space_id']

    **Example**

    .. code-block:: python

        from ibm_watsonx_ai import Credentials

        from ibm_watsonx_ai.foundation_models.prompts import PromptTemplate, PromptTemplateManager
        from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

        prompt_mgr = PromptTemplateManager(
                        credentials=Credentials(
                            api_key="***",
                            url="https://us-south.ml.cloud.ibm.com"
                        ),
                        project_id="*****"
                        )

        prompt_template = PromptTemplate(name="My prompt",
                                         model_id=ModelTypes.GRANITE_13B_CHAT_V2,
                                         input_prefix="Human:",
                                         output_prefix="Assistant:",
                                         input_text="What is {object} and how does it work?",
                                         input_variables=['object'],
                                         examples=[['What is the Stock Market?',
                                                    'A stock market is a place where investors buy and sell shares of publicly traded companies.']])

        stored_prompt_template = prompt_mgr.store_prompt(prompt_template)
        print(stored_prompt_template.prompt_id)   # id of prompt template asset

    """

    def __init__(
        self,
        credentials: Credentials | dict | None = None,
        *,
        project_id: str | None = None,
        space_id: str | None = None,
        verify: str | bool | None = None,
        api_client: APIClient | None = None,
    ) -> None:
        self.project_id = project_id
        self.space_id = space_id
        if credentials:
            self._client = APIClient(credentials, verify=verify)
        elif api_client:
            api_client = cast(APIClient, api_client)
            self._client = api_client
        else:
            raise InvalidMultipleArguments(
                params_names_list=["credentials", "api_client"],
                reason="None of the arguments were provided.",
            )

        if self.space_id is not None and self.project_id is not None:
            raise InvalidMultipleArguments(
                params_names_list=["project_id", "space_id"],
                reason="Both arguments were provided.",
            )
        self.params = {}
        if self.space_id:
            self._client.set.default_space(space_id)
            self.params = {"space_id": self.space_id}
        elif self.project_id:
            project_id = cast(str, project_id)
            self._client.set.default_project(project_id)
            self.params = {"project_id": self.project_id}
        elif api_client:
            if project_id := self._client.default_project_id:
                self.params = {"project_id": project_id}
            elif space_id := self._client.default_space_id:
                self.params = {"space_id": space_id}
            else:
                pass
        elif not api_client:
            raise InvalidMultipleArguments(
                params_names_list=["space_id", "project_id"],
                reason="None of the arguments were provided.",
            )

        if not self._client.CLOUD_PLATFORM_SPACES and self._client.CPD_version < 4.8:
            raise WMLClientError(error_msg="Operation is unsupported for this release.")

        WMLResource.__init__(self, __name__, self._client)

    def _create_request_body(self, prompt_template: PromptTemplate) -> dict:
        """Method is used to create request body from PromptTemplate object.

        :param prompt_template: Object of type PromptTemplate based on which the request
                                body will be created.
        :type prompt_template: PromptTemplate

        :return: Request body
        :rtype: dict
        """
        json_data: dict = {"prompt": dict()}
        if prompt_template.description is not None:
            json_data.update({"description": prompt_template.description})
        if prompt_template.input_variables is not None:
            PromptTemplateManager._validate_type(
                prompt_template.input_variables, "input_variables", [dict, list], False
            )
            if isinstance(prompt_template.input_variables, list):
                json_data.update(
                    {
                        "prompt_variables": {
                            key: {} for key in prompt_template.input_variables
                        }
                    }
                )
            else:
                json_data.update({"prompt_variables": prompt_template.input_variables})
        if prompt_template.task_ids is not None:
            PromptTemplateManager._validate_type(
                prompt_template.task_ids, "task_ids", list, False
            )
            json_data.update({"task_ids": prompt_template.task_ids})
        if prompt_template.template_version is not None:
            json_data.update(
                {"model_version": {"number": prompt_template.template_version}}
            )
        if hasattr(prompt_template, "input_mode"):
            json_data.update({"input_mode": prompt_template.input_mode})

        if prompt_template.input_text:
            PromptTemplateManager._validate_type(
                prompt_template.input_text, "input_text", str, False
            )
            json_data["prompt"].update({"input": [[prompt_template.input_text, ""]]})

        PromptTemplateManager._validate_type(
            prompt_template.model_id, "model_id", str, True
        )
        if prompt_template.model_id is not None:
            json_data["prompt"].update({"model_id": prompt_template.model_id})

        if prompt_template.model_params is not None:
            PromptTemplateManager._validate_type(
                prompt_template.model_params, "model_parameters", dict, False
            )
            json_data["prompt"].update(
                {"model_parameters": prompt_template.model_params}
            )

        if hasattr(prompt_template, "external_information"):
            json_data["prompt"].update(
                {"external_information": prompt_template.external_information}
            )

        data: dict = dict()
        if prompt_template.instruction is not None:
            data.update({"instruction": prompt_template.instruction})

        if prompt_template.input_prefix is not None:
            data.update({"input_prefix": prompt_template.input_prefix})

        if prompt_template.output_prefix is not None:
            data.update({"output_prefix": prompt_template.output_prefix})
        if prompt_template.examples is not None:
            PromptTemplateManager._validate_type(
                prompt_template.examples, "examples", list, False
            )
            data.update({"examples": prompt_template.examples})

        json_data["prompt"].update({"data": data})

        return json_data

    def _from_json_to_prompt(self, response: dict) -> PromptTemplate:
        """Convert json response to PromptTemplate object.

        :param response: Response body after request operation.
        :type response: dict

        :return: PromptTemplate object with given details.
        :rtype: PromptTemplate
        """
        prompt_field: dict = response.get("prompt", dict())
        data_field: dict = prompt_field.get("data", dict())
        prompt_template = PromptTemplate(
            name=response.get("name"),
            description=response.get("description"),
            model_id=prompt_field.get("model_id"),
            model_params=prompt_field.get("model_parameters"),
            task_ids=response.get("task_ids"),
            template_version=response.get("model_version", dict()).get("number"),
            input_variables=response.get("prompt_variables"),
            input_text=prompt_field.get("input", [[None, None]])[0][0],
            instruction=data_field.get("instruction"),
            input_prefix=data_field.get("input_prefix"),
            output_prefix=data_field.get("output_prefix"),
            examples=data_field.get("examples"),
            validate_template=False,
        )

        prompt_template._prompt_id = response.get("id")
        prompt_template._created_at = response.get("created_at")
        if "lock_type" in response.get("lock", dict()):
            del response["lock"]["lock_type"]
        prompt_template._lock = PromptTemplateLock(
            **response.get("lock", {"locked": None, "locked_by": None})
        )
        prompt_template._is_template = response.get("is_template")

        return prompt_template

    def _get_details(self, limit: int | None = None) -> list:
        """Method retrives details of all prompt templates. If limit is set to None
        then all prompt templates are fetched.

        :param limit: limit number of fetched records, defaults to None.
        :type limit: int | None

        :return: List of prompts metadata
        :rtype: List
        """
        headers = self._client._get_headers()
        url = self._client.service_instance._href_definitions.get_prompts_all_href()
        json_data: dict[str, int | str] = {
            "query": "asset.asset_type:wx_prompt",
            "sort": "-asset.created_at<string>",
        }
        if limit is not None:
            if limit < 1:
                raise WMLClientError("Limit cannot be lower than 1.")
            elif limit > 200:
                raise WMLClientError("Limit cannot be larger than 200.")

            json_data.update({"limit": limit})
        else:
            json_data.update({"limit": 200})
        prompts_list = []
        bookmark = True
        while bookmark is not None:
            response = requests.post(
                url=url, json=json_data, headers=headers, params=self.params
            )
            details_json = self._handle_response(200, "Get next details", response)
            bookmark = details_json.get("next", {"href": None}).get("bookmark", None)
            prompts_list.extend(details_json.get("results", []))
            if limit is not None:
                break
            json_data.update({"bookmark": bookmark})
        return prompts_list

    def _change_lock(self, prompt_id: str, locked: bool, force: bool = False) -> dict:
        """Change prompt template lock state.

        :param prompt_id: Id of prompt template.
        :type prompt_id: str

        :param locked: New lock state.
        :type locked: bool

        :param force: force lock state overwrite, defaults to False.
        :type force: bool, optional

        :return: Response content after lock state change.
        :rtype: dict
        """
        headers = self._client._get_headers()
        params = self.params | {"prompt_id": prompt_id, "force": force}
        json_data = {"locked": locked}

        url = (
            self._client.service_instance._href_definitions.get_prompts_href()
            + f"/{prompt_id}/lock"
        )
        response = requests.put(url=url, json=json_data, headers=headers, params=params)

        return self._handle_response(200, "change_lock", response)

    def load_prompt(
        self,
        prompt_id: str,
        astype: PromptTemplateFormats | str = PromptTemplateFormats.PROMPTTEMPLATE,
        *,
        prompt_variables: dict[str, str] | None = None,
    ) -> LcPromptTemplate | PromptTemplate | str:
        """Retrive a prompt template asset.

        :param prompt_id: Id of prompt template which is processed.
        :type prompt_id: str

        :param astype: Type of return object.
        :type astype: PromptTemplateFormats

        :param prompt_variables: dictionary of input variables and values with which input variables will be replaced.
        :type prompt_variables: dict[str, str]

        :return: Prompt template asset.
        :rtype: PromptTemplate | str | langchain.prompts.PromptTemplate

        **Example**

        .. code-block:: python

            loaded_prompt_template = prompt_mgr.load_prompt(prompt_id)
            loaded_prompt_template_lc = prompt_mgr.load_prompt(prompt_id, PromptTemplateFormats.LANGCHAIN)
            loaded_prompt_template_string = prompt_mgr.load_prompt(prompt_id, PromptTemplateFormats.STRING)
        """
        headers = self._client._get_headers()
        params = self.params | {"prompt_id": prompt_id}
        url = (
            self._client.service_instance._href_definitions.get_prompts_href()
            + f"/{prompt_id}"
        )

        if isinstance(astype, PromptTemplateFormats):
            astype = astype.value

        if astype == "prompt":
            response = requests.get(url=url, headers=headers, params=params)
            return self._from_json_to_prompt(
                self._handle_response(200, "_load_json_prompt", response)
            )
        elif astype in ("langchain", "string"):
            response = requests.post(url=url + "/input", headers=headers, params=params)
            response_input = self._handle_response(200, "load_prompt", response).get(
                "input"
            )
            response_input = cast(str, response_input)
            if astype == "string":
                try:
                    return (
                        response_input
                        if prompt_variables is None
                        else response_input.format(**prompt_variables)
                    )
                except KeyError as key:
                    raise PromptVariablesError(str(key))
            else:
                from langchain.prompts import PromptTemplate as LcPromptTemplate

                return LcPromptTemplate.from_template(response_input)
        else:
            raise InvalidValue("astype")

    def list(self, *, limit: int | None = None) -> pandas.core.frame.DataFrame:
        """List all available prompt templates in the DataFrame format.

        :param limit: limit number of fetched records, defaults to None.
        :type limit: int, optional

        :return: Dataframe of fundamental properties of availabale prompts.
        :rtype: pandas.core.frame.DataFram

        **Example**

        .. code-block:: python

            prompt_mgr.list(limit=5)    # list of 5 recent created prompt template assets

        .. hint::
            Additionally you can sort available prompt templates by "LAST MODIFIED" field.

            .. code-block:: python

                df_prompts = prompt_mgr.list()
                df_prompts.sort_values("LAST MODIFIED", ascending=False)

        """
        details = [
            "metadata.asset_id",
            "metadata.name",
            "metadata.created_at",
            "metadata.usage.last_updated_at",
        ]
        prompts_details = self._get_details(limit=limit)

        data_normalize = pandas.json_normalize(prompts_details)
        prompts_data = data_normalize.reindex(columns=details)

        df_details = pandas.DataFrame(prompts_data, columns=details)

        df_details.rename(
            columns={
                "metadata.asset_id": "ID",
                "metadata.name": "NAME",
                "metadata.created_at": "CREATED",
                "metadata.usage.last_updated_at": "LAST MODIFIED",
            },
            inplace=True,
        )

        return df_details

    def store_prompt(
        self, prompt_template: PromptTemplate | langchain.prompts.PromptTemplate
    ) -> PromptTemplate:
        """Store a new prompt template.

        :param prompt_template: PromptTemplate to be stored.
        :type prompt_template: (PromptTemplate | langchain.prompts.PromptTemplate)

        :return: PromptTemplate object initialized with values provided in the server response object.
        :rtype: PromptTemplate
        """
        if isinstance(prompt_template, PromptTemplate):
            pass
        else:
            from langchain.prompts import PromptTemplate as LcPromptTemplate

            if isinstance(prompt_template, LcPromptTemplate):

                def get_metadata_value(
                    prompt_temp: LcPromptTemplate,
                    key: str,
                    default: ModelTypes | list | bool | str | None = None,
                    must_be_list: bool = False,
                    must_be_nested_list: bool = False,
                ) -> Any:
                    if (
                        hasattr(prompt_temp, "metadata")
                        and prompt_temp.metadata
                        and key in prompt_temp.metadata
                    ):
                        if must_be_list:
                            if isinstance(prompt_temp.metadata[key], str):
                                return [prompt_temp.metadata[key]]
                            return prompt_temp.metadata[key]
                        elif must_be_nested_list:
                            if isinstance(prompt_temp.metadata[key], str):
                                return [[prompt_temp.metadata[key]]]
                            elif isinstance(prompt_temp.metadata[key], list):
                                if isinstance(prompt_temp.metadata[key][0], str):
                                    return [prompt_temp.metadata[key]]
                                return prompt_temp.metadata[key]
                        else:
                            return prompt_temp.metadata[key]
                    else:
                        return default

                prompt_template = PromptTemplate(
                    name=get_metadata_value(prompt_template, "name", "My prompt"),
                    model_id=get_metadata_value(
                        prompt_template, "model_id", ModelTypes.FLAN_UL2
                    ),
                    model_params=get_metadata_value(
                        prompt_template, "model_params", None
                    ),
                    template_version=get_metadata_value(
                        prompt_template, "template_version", None
                    ),
                    task_ids=get_metadata_value(
                        prompt_template, "task_ids", None, must_be_list=True
                    ),
                    description=get_metadata_value(
                        prompt_template, "description", None
                    ),
                    input_text=get_metadata_value(
                        prompt_template, "input_text", prompt_template.template
                    ),
                    input_variables=get_metadata_value(
                        prompt_template,
                        "input_variables",
                        prompt_template.input_variables,
                    ),
                    instruction=get_metadata_value(
                        prompt_template, "instruction", None
                    ),
                    input_prefix=get_metadata_value(
                        prompt_template, "input_prefix", None
                    ),
                    output_prefix=get_metadata_value(
                        prompt_template, "output_prefix", None
                    ),
                    examples=get_metadata_value(
                        prompt_template, "examples", None, must_be_nested_list=True
                    ),
                    validate_template=get_metadata_value(
                        prompt_template, "validate_template", True
                    ),
                )
            else:
                raise WMLClientError(error_msg="Unsupported type for `prompt_template`")

        headers = self._client._get_headers()

        PromptTemplateManager._validate_type(
            prompt_template.name, "prompt_template.name", str, True
        )
        json_data: dict = {
            "name": prompt_template.name,
            "lock": {"locked": True},
            "prompt": dict(),
        }

        json_data.update(self._create_request_body(prompt_template))

        url = self._client.service_instance._href_definitions.get_prompts_href()
        response = requests.post(
            url=url, json=json_data, headers=headers, params=self.params
        )
        response = self._handle_response(201, "store_prompt", response)

        return self._from_json_to_prompt(response)

    def delete_prompt(self, prompt_id: str, *, force: bool = False) -> str:
        """Remove prompt template from project or space.

        :param prompt_id: Id of prompt template that will be delete.
        :type prompt_id: str

        :param force: If True then prompt template is unlocked and then delete, defaults to False.
        :type force: bool

        :return: Status 'SUCESS' if the prompt template is successfully deleted.
        :rtype: str

        **Example**

        .. code-block:: python

            prompt_mgr.delete_prompt(prompt_id)  # delete if asset is unclocked
        """
        if force:
            self.unlock(prompt_id)

        headers = self._client._get_headers()
        params = self.params | {"prompt_id": prompt_id}

        url = (
            self._client.service_instance._href_definitions.get_prompts_href()
            + f"/{prompt_id}"
        )
        response = requests.delete(url=url, headers=headers, params=params)

        return self._handle_response(204, "delete_prompt", response)  # type: ignore[return-value]

    def update_prompt(self, prompt_id: str, prompt_template: PromptTemplate) -> dict:
        """Update prompt template data.

        :param prompt_id: Id of the updated prompt template.
        :type prompt_id: str

        :param prompt: PromptTemplate with new data.
        :type prompt: PromptTemplate

        :return: metadata of updated deployment
        :rtype: dict

        **Example**

        .. code-block:: python

            updataed_prompt_template = PromptTemplate(name="New name")
            prompt_mgr.update_prompt(prompt_id, prompt_template)  # {'name': 'New name'} in metadata

        """
        headers = self._client._get_headers()
        params = self.params | {"prompt_id": prompt_id}

        new_body: dict = dict()
        current_prompt_template = self.load_prompt(prompt_id)

        current_prompt_template = cast(PromptTemplate, current_prompt_template)
        for attribute in prompt_template.__dict__:
            if getattr(
                prompt_template, attribute
            ) is not None and not attribute.startswith("_"):
                setattr(
                    current_prompt_template,
                    attribute,
                    getattr(prompt_template, attribute),
                )

        if current_prompt_template.name is not None:
            new_body.update({"name": current_prompt_template.name})

        new_body.update(self._create_request_body(current_prompt_template))

        url = (
            self._client.service_instance._href_definitions.get_prompts_href()
            + f"/{prompt_id}"
        )

        response = requests.patch(
            url=url, json=new_body, headers=headers, params=params
        )
        return self._handle_response(200, "update_prompt", response)

    def get_lock(self, prompt_id: str) -> dict:
        """Get the current locked state of a prompt template.

        :param prompt_id: Id of prompt template
        :type prompt_id: str

        :return: Information about locked state of prompt template asset.
        :rtype: dict

        **Example**

        .. code-block:: python

            print(prompt_mgr.get_lock(prompt_id))
        """
        headers = self._client._get_headers()
        params = self.params | {"prompt_id": prompt_id}
        url = (
            self._client.service_instance._href_definitions.get_prompts_href()
            + f"/{prompt_id}/lock"
        )

        response = requests.get(url=url, headers=headers, params=params)

        return self._handle_response(200, "get_lock", response)

    def lock(self, prompt_id: str, force: bool = False) -> dict:
        """Lock the prompt template if it is unlocked and user has permission to do that.

        :param promp_id: Id of prompt template.
        :type promp_id: str

        :param force: If True, method forcefully overwrite a lock.
        :type force: bool

        :return: Status 'SUCCESS' or response content after an attempt to lock prompt template.
        :rtype: dict

        **Example**

        .. code-block:: python

            prompt_mgr.lock(prompt_id)

        """
        return self._change_lock(prompt_id=prompt_id, locked=True, force=force)

    def unlock(self, prompt_id: str) -> dict:
        """Unlock the prompt template if it is locked and user has permission to do that.

        :param promp_id: Id of prompt template.
        :type promp_id: str

        :return: Response content after an attempt to unlock prompt template.
        :rtype: dict

        **Example**

        .. code-block:: python

            prompt_mgr.unlock(prompt_id)
        """
        # server returns status code 400 after trying to unlock unlocked prompt
        lock_state = self.get_lock(prompt_id)
        if lock_state["locked"]:
            return self._change_lock(prompt_id=prompt_id, locked=False, force=False)
        else:
            return lock_state
