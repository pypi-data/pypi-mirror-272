#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations
from typing import Any, TYPE_CHECKING, TypeAlias

from warnings import warn
import ibm_watsonx_ai._wrappers.requests as requests
from ibm_watsonx_ai.hpo import HPOParameter, HPOMethodParam
from ibm_watsonx_ai.messages.messages import Messages
from ibm_watsonx_ai.metanames import ExperimentMetaNames
from ibm_watsonx_ai.utils import EXPERIMENT_DETAILS_TYPE
from ibm_watsonx_ai.utils.utils import _get_id_from_deprecated_uid
from ibm_watsonx_ai.wml_client_error import WMLClientError
from ibm_watsonx_ai.wml_resource import WMLResource

_DEFAULT_LIST_LENGTH = 50
ListType: TypeAlias = list

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient
    from pandas import DataFrame


class Experiments(WMLResource):
    """Run new experiment."""

    ConfigurationMetaNames = ExperimentMetaNames()
    """MetaNames for experiments creation."""

    @staticmethod
    def _HPOParameter(
        name: str,
        values: ListType[str] | ListType[float] | None = None,
        max: float | None = None,
        min: float | None = None,
        step: float | None = None,
    ) -> dict:
        return HPOParameter(name, values, max, min, step)

    @staticmethod
    def _HPOMethodParam(
        name: str | None = None, value: str | float | None = None
    ) -> dict:
        return HPOMethodParam(name, value)

    def __init__(self, client: APIClient) -> None:
        WMLResource.__init__(self, __name__, client)

    def store(self, meta_props: dict) -> dict:
        """Create an experiment.

        :param meta_props: meta data of the experiment configuration. To see available meta names use:

            .. code-block:: python

                client.experiments.ConfigurationMetaNames.get()

        :type meta_props: dict

        :return: stored experiment metadata
        :rtype: dict

        **Example**

        .. code-block:: python

            metadata = {
                client.experiments.ConfigurationMetaNames.NAME: 'my_experiment',
                client.experiments.ConfigurationMetaNames.EVALUATION_METRICS: ['accuracy'],
                client.experiments.ConfigurationMetaNames.TRAINING_REFERENCES: [
                    {'pipeline': {'href': pipeline_href_1}},
                    {'pipeline': {'href':pipeline_href_2}}
                ]
            }
            experiment_details = client.experiments.store(meta_props=metadata)
            experiment_href = client.experiments.get_href(experiment_details)

        """
        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        metaProps = self.ConfigurationMetaNames._generate_resource_metadata(meta_props)
        # Check if default space is set

        if self._client.default_space_id is not None:
            metaProps["space_id"] = self._client.default_space_id
        elif self._client.default_project_id is not None:
            metaProps["project_id"] = self._client.default_project_id
        else:
            raise WMLClientError(
                Messages.get_message(
                    message_id="it_is_mandatory_to_set_the_space_project_id"
                )
            )
        self._validate_meta_prop(
            meta_props, self.ConfigurationMetaNames.NAME, str, True
        )

        response_experiment_post = requests.post(
            self._client.service_instance._href_definitions.get_experiments_href(),
            params=self._client._params(skip_for_create=True),
            json=metaProps,
            headers=self._client._get_headers(),
        )
        return self._handle_response(201, "saving experiment", response_experiment_post)

    def update(
        self,
        experiment_id: str | None = None,
        changes: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        """Updates existing experiment metadata.

        :param experiment_id: ID of experiment which definition should be updated
        :type experiment_id: str
        :param changes: elements which should be changed, where keys are ConfigurationMetaNames
        :type changes: dict

        :return: metadata of updated experiment
        :rtype: dict

        **Example**

        .. code-block:: python

            metadata = {
                client.experiments.ConfigurationMetaNames.NAME: "updated_exp"
            }
            exp_details = client.experiments.update(experiment_id, changes=metadata)

        """
        if changes is None:
            raise TypeError(
                "update() missing 1 required positional argument: 'changes'"
            )

        experiment_id = _get_id_from_deprecated_uid(
            kwargs, experiment_id, "experiment", can_be_none=False
        )

        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        self._validate_type(experiment_id, "experiment_id", str, True)
        self._validate_type(changes, "changes", dict, True)

        details = self._client.repository.get_details(experiment_id)

        patch_payload = self.ConfigurationMetaNames._generate_patch_payload(
            details["entity"], changes, with_validation=True
        )

        url = self._client.service_instance._href_definitions.get_experiment_href(
            experiment_id
        )
        response = requests.patch(
            url,
            json=patch_payload,
            params=self._client._params(),
            headers=self._client._get_headers(),
        )
        updated_details = self._handle_response(200, "experiment patch", response)

        return updated_details

    def get_details(
        self,
        experiment_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool | None = False,
        get_all: bool | None = False,
        **kwargs: Any,
    ) -> dict:
        """Get metadata of experiment(s). If no experiment ID is specified all experiments metadata is returned.

        :param experiment_id:  ID of experiment
        :type experiment_id: str, optional
        :param limit: limit number of fetched records
        :type limit: int, optional
        :param asynchronous: if `True`, it will work as a generator
        :type asynchronous: bool, optional
        :param get_all: if `True`, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: experiment(s) metadata
        :rtype: dict (if ID is not None) or {"resources": [dict]} (if ID is None)

        **Example**

        .. code-block:: python

            experiment_details = client.experiments.get_details(experiment_id)
            experiment_details = client.experiments.get_details()
            experiment_details = client.experiments.get_details(limit=100)
            experiment_details = client.experiments.get_details(limit=100, get_all=True)
            experiment_details = []
            for entry in client.experiments.get_details(limit=100, asynchronous=True, get_all=True):
                experiment_details.extend(entry)

        """
        experiment_id = _get_id_from_deprecated_uid(
            kwargs, experiment_id, "experiment", can_be_none=True
        )

        Experiments._validate_type(experiment_id, "experiment_id", str, False)
        Experiments._validate_type(limit, "limit", int, False)
        Experiments._validate_type(asynchronous, "asynchronous", bool, False)
        Experiments._validate_type(get_all, "get_all", bool, False)

        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        url = self._client.service_instance._href_definitions.get_experiments_href()

        if experiment_id is None:
            return self._get_artifact_details(
                url,
                experiment_id,
                limit,
                "experiment",
                _async=asynchronous,
                _all=get_all,
            )

        else:
            return self._get_artifact_details(url, experiment_id, limit, "experiment")

    @staticmethod
    def get_uid(experiment_details: dict) -> str:
        """Get Unique Id of stored experiment.

        *Deprecated:* Use ``get_id(experiment_details)`` instead.

        :param experiment_details: metadata of the stored experiment
        :type experiment_details: dict

        :return: Unique Id of stored experiment
        :rtype: str

        **Example**

        .. code-block:: python

            experiment_details = client.experiments.get_details(experiment_id)
            experiment_uid = client.experiments.get_uid(experiment_details)

        """
        warn("This method is deprecated, please use get_id()")

        return Experiments.get_id(experiment_details)

    @staticmethod
    def get_id(experiment_details: dict) -> str:
        """Get Unique Id of stored experiment.

        :param experiment_details: metadata of the stored experiment
        :type experiment_details: dict

        :return: Unique Id of stored experiment
        :rtype: str

        **Example**

        .. code-block:: python

            experiment_details = client.experiments.get_details(experiment_id)
            experiment_id = client.experiments.get_id(experiment_details)

        """
        Experiments._validate_type(
            experiment_details, "experiment_details", object, True
        )
        if "id" not in experiment_details["metadata"]:
            Experiments._validate_type_of_details(
                experiment_details, EXPERIMENT_DETAILS_TYPE
            )

        return WMLResource._get_required_element_from_dict(
            experiment_details, "experiment_details", ["metadata", "id"]
        )

    @staticmethod
    def get_href(experiment_details: dict) -> str:
        """Get href of stored experiment.

        :param experiment_details: metadata of the stored experiment
        :type experiment_details: dict

        :return: href of stored experiment
        :rtype: str

        **Example**

        .. code-block:: python

            experiment_details = client.experiments.get_details(experiment_id)
            experiment_href = client.experiments.get_href(experiment_details)

        """
        Experiments._validate_type(
            experiment_details, "experiment_details", object, True
        )
        if "href" in experiment_details["metadata"]:
            Experiments._validate_type_of_details(
                experiment_details, EXPERIMENT_DETAILS_TYPE
            )

            return WMLResource._get_required_element_from_dict(
                experiment_details, "experiment_details", ["metadata", "href"]
            )
        else:
            experiment_id = WMLResource._get_required_element_from_dict(
                experiment_details, "experiment_details", ["metadata", "id"]
            )
            return "/ml/v4/experiments/" + experiment_id

    def delete(self, experiment_id: str | None = None, **kwargs: Any) -> str:
        """Delete a stored experiment.

        :param experiment_id: Unique Id of the stored experiment
        :type experiment_id: str

        :return: status ("SUCCESS" or "FAILED")
        :rtype: str

        **Example**

        .. code-block:: python

            client.experiments.delete(experiment_id)

        """
        experiment_id = _get_id_from_deprecated_uid(
            kwargs, experiment_id, "experiment", can_be_none=False
        )

        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        Experiments._validate_type(experiment_id, "experiment_id", str, True)

        url = self._client.service_instance._href_definitions.get_experiment_href(
            experiment_id
        )
        response = requests.delete(
            url, params=self._client._params(), headers=self._client._get_headers()
        )

        return self._handle_response(204, "experiment deletion", response, False)

    def list(self, limit: int | None = None) -> DataFrame:
        """Lists stored experiments in a table format.
        If limit is set to None there will be only first 50 records shown.

        :param limit: limit number of fetched records
        :type limit: int, optional

        :return: pandas.DataFrame with listed experiments
        :rtype: pandas.DataFrame

        **Example**

        .. code-block:: python

            client.experiments.list()

        """
        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        experiment_resources = self.get_details(limit=limit)["resources"]
        experiment_values = [
            (m["metadata"]["id"], m["metadata"]["name"], m["metadata"]["created_at"])
            for m in experiment_resources
        ]
        header_list = ["ID", "NAME", "CREATED"]

        table = self._list(experiment_values, header_list, limit, _DEFAULT_LIST_LENGTH)

        return table

    def create_revision(self, experiment_id: str | None) -> dict:
        """Create a new experiment revision.

        :param experiment_id: Unique Id of the stored experiment
        :type experiment_id: str

        :return: stored experiment new revision details
        :rtype: dict

        **Example**

        .. code-block:: python

            experiment_revision_artifact = client.experiments.create_revision(experiment_id)

        """
        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        Experiments._validate_type(experiment_id, "experiment_id", str, True)

        url = self._client.service_instance._href_definitions.get_experiments_href()
        return self._create_revision_artifact(url, experiment_id, "experiments")

    def get_revision_details(
        self,
        experiment_id: str | None = None,
        rev_id: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Get metadata of stored experiments revisions.

        :param experiment_id: stored experiment ID
        :type experiment_id: str

        :param rev_id: rev_id number of experiment
        :type rev_id: str

        :return: stored experiment revision metadata
        :rtype: dict

        Example:

        .. code-block:: python

            experiment_details = client.experiments.get_revision_details(experiment_id, rev_id)

        """
        experiment_id = _get_id_from_deprecated_uid(
            kwargs, experiment_id, "experiment", can_be_none=False
        )
        rev_id = _get_id_from_deprecated_uid(kwargs, rev_id, "rev", can_be_none=False)

        # Backward compatibility in past `rev_id` was an int.
        if isinstance(rev_id, int):
            warn(
                f"`rev_id` parameter type as int is deprecated, please convert to str instead",
                category=DeprecationWarning,
            )
            rev_id = str(rev_id)

        self._client._check_if_either_is_set()
        Experiments._validate_type(experiment_id, "experiment_id", str, True)
        Experiments._validate_type(rev_id, "rev_id", str, True)

        url = self._client.service_instance._href_definitions.get_experiment_href(
            experiment_id
        )
        return self._get_with_or_without_limit(
            url,
            limit=None,
            op_name="experiments",
            summary=None,
            pre_defined=None,
            revision=rev_id,
        )

    def list_revisions(
        self,
        experiment_id: str | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> DataFrame:
        """Print all revision for the given experiment id in a table format.

        :param experiment_id: Unique id of stored experiment
        :type experiment_id: str

        :param limit: limit number of fetched records
        :type limit: int, optional

        :return: pandas.DataFrame with listed revisions
        :rtype: pandas.DataFrame

        **Example**

        .. code-block:: python

            client.experiments.list_revisions(experiment_id)

        """
        experiment_id = _get_id_from_deprecated_uid(
            kwargs, experiment_id, "experiment", can_be_none=False
        )

        # For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        Experiments._validate_type(experiment_id, "experiment_id", str, True)

        url = self._client.service_instance._href_definitions.get_experiment_href(
            experiment_id
        )
        experiment_resources = self._get_artifact_details(
            url, "revisions", limit, "model revisions"
        )["resources"]
        experiment_values = [
            (m["metadata"]["rev"], m["metadata"]["name"], m["metadata"]["created_at"])
            for m in experiment_resources
        ]

        table = self._list(
            experiment_values, ["REV", "NAME", "CREATED"], limit, _DEFAULT_LIST_LENGTH
        )
        return table
