#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations

import json
import os
from typing import Generator, TYPE_CHECKING

from requests import Response

from ibm_watsonx_ai._wrappers import requests

from ibm_watsonx_ai.metanames import PkgExtnMetaNames
from ibm_watsonx_ai.utils import PKG_EXTN_DETAILS_TYPE
from ibm_watsonx_ai.wml_client_error import WMLClientError, ApiRequestFailure
from ibm_watsonx_ai.wml_resource import WMLResource

if TYPE_CHECKING:
    from pandas import DataFrame
    from ibm_watsonx_ai import APIClient

_DEFAULT_LIST_LENGTH = 50


class PkgExtn(WMLResource):
    """Store and manage software Packages Extension specs."""

    ConfigurationMetaNames = PkgExtnMetaNames()
    """MetaNames for Package Extensions creation."""

    def __init__(self, client: APIClient):
        WMLResource.__init__(self, __name__, client)

    def get_details(self, pkg_extn_id: str) -> dict:
        """Get package extensions details.

        :param pkg_extn_id: Unique Id of package extension
        :type pkg_extn_id: str

        :return: details of the package extensions
        :rtype: dict

        **Example**

        .. code-block:: python

            pkg_extn_details = client.pkg_extn.get_details(pkg_extn_id)

        """
        PkgExtn._validate_type(pkg_extn_id, "pkg_extn_id", str, True)

        response = requests.get(
            self._client.service_instance._href_definitions.get_pkg_extn_href(
                pkg_extn_id
            ),
            params=self._client._params(),
            headers=self._client._get_headers(),
        )

        if response.status_code == 200:
            return self._get_required_element_from_response(
                self._handle_response(200, "get hw spec details", response)
            )
        else:
            return self._handle_response(200, "get hw spec details", response)

    def store(self, meta_props: dict, file_path: str) -> dict:
        """Create a package extensions.

        :param meta_props: meta data of the package extension. To see available meta names use:

            .. code-block:: python

                client.package_extensions.ConfigurationMetaNames.get()

        :type meta_props: dict

        :param file_path:  path to file which will be uploaded as package extension
        :type file_path: str

        :return: metadata of the package extensions
        :rtype: dict

        **Example**

        .. code-block:: python

            meta_props = {
                client.package_extensions.ConfigurationMetaNames.NAME: "skl_pipeline_heart_problem_prediction",
                client.package_extensions.ConfigurationMetaNames.DESCRIPTION: "description scikit-learn_0.20",
                client.package_extensions.ConfigurationMetaNames.TYPE: "conda_yml"
            }

            pkg_extn_details = client.package_extensions.store(meta_props=meta_props, file_path="/path/to/file")

        """
        # quick support for COS credentials instead of local path
        # TODO add error handling and cleaning (remove the file)
        PkgExtn._validate_type(meta_props, "meta_props", dict, True)
        pkg_extn_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props, with_validation=True, client=self._client
        )

        pkg_extn_meta_json = json.dumps(pkg_extn_meta)

        PkgExtn._validate_type(file_path, "file_path", str, True)
        # Step1  : Create an asset
        print("Creating package extensions")
        href = self._client.service_instance._href_definitions.get_pkg_extns_href()

        creation_response = requests.post(
            href,
            params=self._client._params(),
            headers=self._client._get_headers(),
            data=pkg_extn_meta_json,
        )

        pkg_extn_details = self._handle_response(
            201, "creating new package_extensions", creation_response
        )

        # Step2: upload pkg extension file to presigned url
        if creation_response.status_code == 201:
            pkg_extn_asset_id = pkg_extn_details["metadata"]["asset_id"]
            pkg_extn_presigned_url = pkg_extn_details["entity"]["package_extension"][
                "href"
            ]

            FILE_SIZE_LIMIT = int(0.3 * 1073741824)

            def read_in_chunks(
                chunk_size: int | None = FILE_SIZE_LIMIT,
            ) -> Generator[bytes, None, None]:
                with open(file_path, "rb") as file_object:
                    while True:
                        data = file_object.read(chunk_size)
                        if not data:
                            break
                        yield data

            def send_multipart_request(file: str, url: str) -> Response:
                content_path = os.path.abspath(file)
                content_size = os.stat(content_path).st_size

                index = 0
                headers = {}

                try:
                    for chunk in read_in_chunks(FILE_SIZE_LIMIT):
                        offset = index + len(chunk)
                        headers["Content-Range"] = "bytes %s-%s/%s" % (
                            index,
                            offset - 1,
                            content_size,
                        )
                        index = offset

                        response = requests.put(
                            url,
                            files={"file": (file, chunk, "application/octet-stream")},
                        )
                except Exception as e:
                    deletion_response = requests.delete(
                        self._client.service_instance._href_definitions.get_pkg_extn_href(
                            pkg_extn_asset_id
                        ),
                        params=self._client._params(),
                        headers=self._client._get_headers(),
                    )
                    print(deletion_response.status_code)
                    raise WMLClientError("Failed while reading a file.", e)

                return response

            # chunking, when finally it will work on service side. to confirm it's working, the downloaded file needs to be the same as 400MB+ upladed file
            #
            # put_response = send_multipart_request(file_path,
            #   (self._client.service_instance._wml_credentials.url if self._client.ICP_PLATFORM_SPACES else "") + pkg_extn_presigned_url)

            href = (
                self._client.service_instance._credentials.url
                if self._client.ICP_PLATFORM_SPACES
                else ""
            ) + pkg_extn_presigned_url

            try:
                if os.stat(file_path).st_size == 0:
                    raise WMLClientError("Package extension file cannot be empty")

                with open(file_path, "rb") as file_object:
                    if not self._client.ICP_PLATFORM_SPACES:
                        put_response = requests.put(href, data=file_object.read())
                    else:
                        put_response = requests.put(
                            href,
                            files={
                                "file": (
                                    file_path,
                                    file_object.read(),
                                    "application/octet-stream",
                                )
                            },
                        )
            except Exception as e:
                deletion_response = requests.delete(
                    self._client.service_instance._href_definitions.get_pkg_extn_href(
                        pkg_extn_asset_id
                    ),
                    params=self._client._params(),
                    headers=self._client._get_headers(),
                )
                print(deletion_response.status_code)
                raise WMLClientError("Failed while reading a file.", e)

            if put_response.status_code == 201 or put_response.status_code == 200:
                # Step3: Mark the upload complete
                complete_response = requests.post(
                    self._client.service_instance._href_definitions.get_pkg_extn_href(
                        pkg_extn_asset_id
                    )
                    + "/upload_complete",
                    headers=self._client._get_headers(),
                    params=self._client._params(),
                )
                if complete_response.status_code == 204:
                    print("SUCCESS")
                    return self._get_required_element_from_response(pkg_extn_details)
                else:
                    try:
                        self.delete(pkg_extn_asset_id)
                    except:
                        pass
                    raise WMLClientError(
                        "Failed while creating a package extensions "
                        + complete_response.text
                    )
            else:
                try:
                    self.delete(pkg_extn_asset_id)
                except:
                    pass
                raise WMLClientError(
                    "Failed while creating a package extensions " + put_response.text
                )
        else:
            raise WMLClientError(
                "Failed while creating a package extensions " + creation_response.text
            )

    def list(self) -> DataFrame:
        """Lists package extensions in a table format.

        :return: pandas.DataFrame with listed package extensions
        :rtype: pandas.DataFrame

        .. code-block:: python

            client.package_extensions.list()

        """

        href = self._client.service_instance._href_definitions.get_pkg_extns_href()

        response = requests.get(
            href, params=self._client._params(), headers=self._client._get_headers()
        )

        self._handle_response(200, "list pkg_extn", response)
        asset_details = self._handle_response(200, "list assets", response)["resources"]
        pkg_extn_values = [
            (
                m["metadata"]["name"],
                m["metadata"]["asset_id"],
                m["entity"]["package_extension"]["type"],
                m["metadata"]["created_at"],
            )
            for m in asset_details
        ]

        table = self._list(
            pkg_extn_values,
            ["NAME", "ASSET_ID", "TYPE", "CREATED_AT"],
            None,
            _DEFAULT_LIST_LENGTH,
        )
        return table

    @staticmethod
    def get_id(pkg_extn_details: dict) -> str:
        """Get Unique Id of package extensions.

        :param pkg_extn_details: details of the package extensions
        :type pkg_extn_details: dict

        :return: Unique Id of package extension
        :rtype: str

        **Example**

        .. code-block:: python

            asset_id = client.package_extensions.get_id(pkg_extn_details)

        """
        PkgExtn._validate_type(pkg_extn_details, "pkg_extn_details", object, True)
        PkgExtn._validate_type_of_details(pkg_extn_details, PKG_EXTN_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(
            pkg_extn_details, "pkg_extn_details", ["metadata", "asset_id"]
        )

    def get_id_by_name(self, pkg_extn_name: str) -> str:
        """Get ID of package extensions.

        :param pkg_extn_name:  name of the package extension
        :type pkg_extn_name: str

        :return: Unique Id of package extension
        :rtype: str

        **Example**

        .. code-block:: python

            asset_id = client.package_extensions.get_id_by_name(pkg_extn_name)

        """
        PkgExtn._validate_type(pkg_extn_name, "pkg_extn_name", str, True)

        parameters = self._client._params()
        parameters.update(name=pkg_extn_name)

        response = requests.get(
            self._client.service_instance._href_definitions.get_pkg_extns_href(),
            params=parameters,
            headers=self._client._get_headers(),
        )

        total_values = self._handle_response(200, "get pkg extn", response)[
            "total_results"
        ]
        if total_values != 0:
            pkg_extn_details = self._handle_response(200, "get pkg extn", response)[
                "resources"
            ]
            return pkg_extn_details[0]["metadata"]["asset_id"]
        else:
            return "Not Found"

    @staticmethod
    def get_href(pkg_extn_details: dict) -> str:
        """Get url of stored package extensions.

        :param pkg_extn_details: details of the package extensions
        :type pkg_extn_details: dict

        :return: href of package extension
        :rtype: str

        **Example**

        .. code-block:: python

            pkg_extn_details = client.package_extensions.get_details(pkg_extn_id)
            pkg_extn_href = client.package_extensions.get_href(pkg_extn_details)

        """
        PkgExtn._validate_type(pkg_extn_details, "pkg_extn_details", object, True)
        PkgExtn._validate_type_of_details(pkg_extn_details, PKG_EXTN_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(
            pkg_extn_details,
            "pkg_extn_details",
            ["entity", "package_extension", "href"],
        )

    def delete(self, pkg_extn_id: str) -> dict | str:
        """Delete a package extension.

        :param pkg_extn_id: Unique Id of package extension
        :type pkg_extn_id: str

        :return: status ("SUCCESS" or "FAILED") if deleted synchronously or dictionary with response
        :rtype: str or dict

        **Example**

        .. code-block:: python

            client.package_extensions.delete(pkg_extn_id)

        """
        PkgExtn._validate_type(pkg_extn_id, "pkg_extn_id", str, True)

        response = requests.delete(
            self._client.service_instance._href_definitions.get_pkg_extn_href(
                pkg_extn_id
            ),
            params=self._client._params(),
            headers=self._client._get_headers(),
        )

        if response.status_code == 200:
            return self._get_required_element_from_response(response.json())
        else:
            return self._handle_response(204, "delete pkg extn specification", response)

    def _get_required_element_from_response(self, response_data: dict) -> dict:

        WMLResource._validate_type(response_data, "pkg_extn_response", dict)

        if self._client.default_space_id is not None:
            new_el = {
                "metadata": {
                    "space_id": response_data["metadata"]["space_id"],
                    "name": response_data["metadata"]["name"],
                    "asset_id": response_data["metadata"]["asset_id"],
                    "asset_type": response_data["metadata"]["asset_type"],
                    "created_at": response_data["metadata"]["created_at"]
                    #'updated_at': response_data['metadata']['updated_at']
                },
                "entity": response_data["entity"],
            }
        elif self._client.default_project_id is not None:
            new_el = {
                "metadata": {
                    "project_id": response_data["metadata"]["project_id"],
                    "name": response_data["metadata"]["name"],
                    "asset_id": response_data["metadata"]["asset_id"],
                    "asset_type": response_data["metadata"]["asset_type"],
                    "created_at": response_data["metadata"]["created_at"],
                },
                "entity": response_data["entity"],
            }

        if "href" in response_data["metadata"]:
            href_without_host = response_data["metadata"]["href"].split(".com")[-1]
            new_el["metadata"].update({"href": href_without_host})

        return new_el

    def download(self, pkg_extn_id: str, filename: str) -> str:
        """Download a package extension.

        :param pkg_extn_id: Unique Id of the package extension to be downloaded
        :type pkg_extn_id: str

        :param filename:  filename to be used for the downloaded file
        :type filename: str

        :return: path to the downloaded package extension content
        :rtype: str

        **Example**

        .. code-block:: python

            client.package_extensions.download(pkg_extn_id,"sample_conda.yml/custom_library.zip")

        """

        PkgExtn._validate_type(pkg_extn_id, "pkg_extn_id", str, True)

        pkg_extn_response = requests.get(
            self._client.service_instance._href_definitions.get_pkg_extn_href(
                pkg_extn_id
            ),
            params=self._client._params(),
            headers=self._client._get_headers(),
        )

        pkg_extn_details = self._handle_response(200, "get assets", pkg_extn_response)

        artifact_content_url = pkg_extn_details["entity"]["package_extension"]["href"]

        if pkg_extn_response.status_code == 200:
            if self._client.CLOUD_PLATFORM_SPACES:
                att_response = requests.get(artifact_content_url)
            else:
                att_response = requests.get(
                    self._credentials.url + artifact_content_url
                )

            if att_response.status_code != 200:
                raise ApiRequestFailure(
                    "Failure during {}.".format("downloading package extension"),
                    att_response,
                )

            downloaded_asset = att_response.content
            try:
                with open(filename, "wb") as f:
                    f.write(downloaded_asset)
                print(
                    "Successfully saved package extension content to file: '{}'".format(
                        filename
                    )
                )
                return os.getcwd() + "/" + filename
            except IOError as e:
                raise WMLClientError(
                    "Saving asset with artifact_url: '{}' failed.".format(filename),
                    e,
                )
        else:
            raise WMLClientError(
                "Failed while downloading the package extension " + pkg_extn_id
            )
