#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations

import os
from typing import Any


class Credentials:
    """This class encapsulate passed credentials and additional params.

    :param url: service url
    :type url: str

    :param api_key: service API key, used in API key authentication
    :type api_key: str, optional

    :param name: service name, used during space creation for Cloud environment
    :type name: str, optional

    :param iam_serviceid_crn: service CRN, used during space creation for Cloud environment
    :type iam_serviceid_crn: str, optional

    :param token: service token, used in token authentication
    :type token: str, optional

    :param projects_token: service projects token, used in token authentication
    :type projects_token: str, optional

    :param username: username, used in username/password or username/api_key authentication, applicable for ICP only
    :type username: str, optional

    :param password: password, used in username/password authentication, applicable for ICP only
    :type password: str, optional

    :param instance_id: instance ID, mandatory for ICP
    :type instance_id: str, optional

    :param version: ICP version, mandatory for ICP
    :type version: str, optional

    :param bedrock_url: Bedrock url, applicable for ICP only
    :type bedrock_url: str, optional

    :param proxies: dictionary of proxies, containing protocol and url mapping (example: `{ "https": "https://example.url.com" }`)
    :type proxies: dict, optional

    :param verify: certificate verification flag
    :type verify: bool, optional
    """

    def __init__(
        self,
        *,
        url: str | None = None,
        api_key: str | None = None,
        name: str | None = None,
        iam_serviceid_crn: str | None = None,
        token: str | None = None,
        projects_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        instance_id: str | None = None,
        version: str | None = None,
        bedrock_url: str | None = None,
        proxies: dict | None = None,
        verify: str | bool | None = None,
    ) -> None:
        env_credentials = Credentials._get_values_from_env_vars()

        self.url = url
        self.api_key = api_key
        self.name = name
        self.iam_serviceid_crn = iam_serviceid_crn
        self.token = token
        self.projects_token = projects_token
        self.username = username
        self.password = password
        self.instance_id = instance_id
        self.version = version
        self.bedrock_url = bedrock_url
        self.proxies = proxies
        self.verify = verify

        for k, v in env_credentials.items():
            if self.__dict__.get(k) is None:
                self.__dict__[k] = v

    @staticmethod
    def _get_values_from_env_vars() -> dict[str, Any]:
        def get_value_from_file(filename: str) -> str:
            with open(filename, "r") as f:
                return f.read()

        def get_verify_value(x: str) -> bool | str:
            if x in ["True", "False"]:
                return x == "True"
            else:
                return x

        env_vars_mapping = {
            "FLIGHT_SERVICE_LOCATION": lambda x: ("flight_service_location", x),
            "FLIGHT_SERVICE_PORT": lambda x: ("flight_service_port", int(x)),
            "WX_CLIENT_VERIFY_REQUESTS": lambda x: ("verify", get_verify_value(x)),
            "USER_ACCESS_TOKEN": lambda x: ("token", x.replace("Bearer ", "")),
            "RUNTIME_ENV_ACCESS_TOKEN_FILE": lambda x: (
                "token",
                get_value_from_file(x).replace("Bearer ", ""),
            ),
            "PROJECT_ID": lambda x: ("project_id", x),
            "SPACE_ID": lambda x: ("space_id", x),
            "RUNTIME_ENV_APSX_URL": lambda x: ("url", x),
        }

        return dict(
            [
                f(os.environ[k])
                for k, f in env_vars_mapping.items()
                if os.environ.get(k) is not None and os.environ.get(k) != ""
            ]
        )

    def _set_env_vars_from_credentials(self) -> None:

        env_vars_mapping = {
            "FLIGHT_SERVICE_LOCATION": "flight_service_location",
            "FLIGHT_SERVICE_PORT": "flight_service_port",
            "WX_CLIENT_VERIFY_REQUESTS": "verify",
        }

        for env_key, property_key in env_vars_mapping.items():
            if (
                os.environ.get(env_key) is None or os.environ.get(env_key) == ""
            ) and self.__dict__.get(property_key) is not None:
                os.environ[env_key] = str(self.__dict__[property_key])

    @staticmethod
    def from_dict(
        credentials: dict[str, Any], _verify: bool | None = None
    ) -> Credentials:
        """Create a Credentials object from dictionary.

        :param credentials: credentials in the dictionary
        :type credentials: dict

        :return: initialised Credentials object
        :rtype: Credentials

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai import Credentials

            credentials = Credentials.from_dict({
                'url': "<url>",
                'apikey': "<api_key>"
            })

        """
        hidden_options_list = [
            "flight_service_location",
            "flight_service_port",
            "development",
            "project_id",
            "space_id",
            "FLIGHT_SERVICE_LOCATION",
            "FLIGHT_SERVICE_PORT",
            "flight_url",
        ]

        creds = Credentials(
            url=credentials.get("url"),
            api_key=credentials.get("apikey", credentials.get("api_key")),
            name=credentials.get("name"),
            iam_serviceid_crn=credentials.get("iam_serviceid_crn"),
            token=credentials.get("token"),
            projects_token=credentials.get("projects_token"),
            username=credentials.get("username"),
            password=credentials.get("password"),
            instance_id=credentials.get("instance_id"),
            version=credentials.get("version"),
            bedrock_url=credentials.get("bedrock_url"),
            proxies=credentials.get("proxies"),
            verify=credentials.get("verify", _verify),
        )

        for hidden_option in hidden_options_list:
            if hidden_option in credentials:
                creds.__dict__[hidden_option] = credentials[hidden_option]

        return creds

    def to_dict(self) -> dict[str, Any]:
        """Get dictionary from the Credentials object.

        :return: dictionary with credentials
        :rtype: dict

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai import Credentials

            credentials = Credentials.from_dict({
                'url': "<url>",
                'apikey': "<api_key>"
            })

            credentials_dict = credentials.to_dict()

        """
        data = dict([(k, v) for k, v in self.__dict__.items() if v is not None])
        if "instance_id" in data and self.instance_id.lower() not in [
            "icp",
            "openshift",
        ]:
            data.pop("instance_id")
        return data

    def __getitem__(self, key: str) -> Any:
        if key == "apikey":  # backwards compatible
            return self.to_dict()["api_key"]
        return self.to_dict()[key]

    def get(self, key: str, default: Any | None = None) -> Any:
        if key == "apikey":  # backwards compatible
            return self.to_dict().get("api_key", default)
        return self.to_dict().get(key, default)
