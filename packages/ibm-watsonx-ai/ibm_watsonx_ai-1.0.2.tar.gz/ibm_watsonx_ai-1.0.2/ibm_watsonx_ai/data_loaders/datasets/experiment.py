#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from __future__ import annotations

__all__ = ["ExperimentIterableDataset"]

import os
import pandas as pd

from typing import TYPE_CHECKING, Iterator, Any, cast
from warnings import warn
from ibm_watsonx_ai.helpers.connections.local import LocalBatchReader
from ibm_watsonx_ai.utils.autoai.enums import SamplingTypes
from ibm_watsonx_ai.utils.autoai.errors import InvalidSizeLimit

if TYPE_CHECKING:
    from ibm_watsonx_ai.helpers.connections.flight_service import FlightConnection
    from ibm_watsonx_ai.helpers.connections import DataConnection
    from ibm_watsonx_ai import APIClient

# Note: try to import torch lib if available, this fallback is done based on
# torch dependency removal request
try:
    from torch.utils.data import IterableDataset

except ImportError:
    IterableDataset: type = object  # type: ignore[no-redef]
# --- end note

DEFAULT_SAMPLE_SIZE_LIMIT = (
    1073741824  # 1GB in Bytes is verified later by _set_sample_size_limit
)
DEFAULT_REDUCED_SAMPLE_SIZE_LIMIT = 104857600  # 100MB in bytes
DEFAULT_SAMPLING_TYPE = SamplingTypes.FIRST_VALUES


class ExperimentIterableDataset(IterableDataset):
    """
    This dataset is intended to be an Iterable stream from Flight Service.
    It should iterate over flight logical batches and manages by Connection class
    how batches are downloaded and created. It should take into consideration only 2 batches at a time.
    If we have 2 batches already downloaded, it should block further download
    and wait for first batch to be consumed.

    Example
    -------
    >>> experiment_metadata = {
    >>>     "prediction_column": 'species',
    >>>     "prediction_type": "classification",
    >>>     "project_id": os.environ.get('PROJECT_ID'),
    >>>     'credentials': credentials
    >>> }

    >>> connection = DataConnection(data_asset_id='5d99c11a-2060-4ef6-83d5-dc593c6455e2')


    >>># default sampling - read first 1GB of data
    >>> iterable_dataset = ExperimentIterableDataset(connection=connection,
    >>>                                              enable_sampling=True,
    >>>                                              sampling_type='first_n_records',
    >>>                                              sample_size_limit = 1GB,
    >>>                                              experiment_metadata=experiment_metadata)

    >>># read all data records in batches / no subsampling
    >>> iterable_dataset = ExperimentIterableDataset(connection=connection,
    >>>                                              enable_sampling=False,
    >>>                                               experiment_metadata=experiment_metadata)

    >>># stratified/random sampling
    >>> iterable_dataset = ExperimentIterableDataset(connection=connection,
    >>>                                              enable_sampling=True,
    >>>                                              sampling_type='stratified',
    >>>                                              sample_size_limit = 1GB,
    >>>                                              experiment_metadata=experiment_metadata)

    """

    connection: FlightConnection | LocalBatchReader | None = None

    def __init__(
        self,
        connection: DataConnection,
        experiment_metadata: dict | None = None,
        enable_sampling: bool = True,
        sample_size_limit: int = DEFAULT_SAMPLE_SIZE_LIMIT,
        sampling_type: str = DEFAULT_SAMPLING_TYPE,
        binary_data: bool = False,
        number_of_batch_rows: int | None = None,
        stop_after_first_batch: bool = False,
        total_size_limit: int = DEFAULT_SAMPLE_SIZE_LIMIT,
        total_nrows_limit: int | None = None,
        total_percentage_limit: float = 1.0,
        **kwargs: Any,
    ):
        super().__init__()
        self.enable_sampling = enable_sampling
        self.sample_size_limit = sample_size_limit
        self.experiment_metadata = experiment_metadata
        self._api_client = getattr(connection, "_api_client", None)
        if self._api_client is None:
            self._api_client = kwargs.get("_api_client", None) or kwargs.get(
                "_wml_client", None
            )
        self.binary_data = binary_data
        self.sampling_type = sampling_type
        self.read_to_file = kwargs.get("read_to_file")
        self.authorized = self._check_authorization()
        self._set_size_limit(total_size_limit)
        self.total_nrows_limit = total_nrows_limit
        self.total_percentage_limit = total_percentage_limit

        # Note: convert to dictionary if we have object from API client
        if not isinstance(connection, dict):
            dict_connection = connection._to_dict()

        else:
            dict_connection = connection
        # --- end note

        self.experiment_metadata = cast(dict[str, Any], self.experiment_metadata)
        # Note: backward compatibility after sampling refactoring #27255
        if kwargs.get("with_sampling") or kwargs.get("normal_read"):
            warn(
                "The parameters with_sampling and normal_read in ExperimentIterableDataset are deprecated. "
                "Use enable_sampling and sampling_type instead."
            )
            if kwargs.get("normal_read"):
                self.enable_sampling = False
            if kwargs.get("with_sampling"):
                from ibm_watsonx_ai.utils.autoai.enums import PredictionType

                self.enable_sampling = True

                if self.experiment_metadata.get("prediction_type") in [
                    PredictionType.REGRESSION
                ]:
                    self.sampling_type = SamplingTypes.RANDOM
                elif self.experiment_metadata.get("prediction_type") in [
                    PredictionType.CLASSIFICATION,
                    PredictionType.BINARY,
                    PredictionType.MULTICLASS,
                ]:
                    self.sampling_type = SamplingTypes.STRATIFIED
        # --- end note

        # if number_of_batch_rows is provided, batch_size does not matter anymore
        if self.authorized:
            is_cos_asset = bool(
                kwargs.get("flight_parameters", {})
                .get("datasource_type", {})
                .get("entity", {})
                .get("name", "")
                == "bluemixcloudobjectstorage"
            )
            # first used headers from experiment metadata if they were set.
            headers_: dict | None = None
            if self.experiment_metadata.get("headers"):
                headers_ = self.experiment_metadata.get("headers")
            elif self._api_client is not None:
                headers_ = self._api_client._get_headers()

            from ibm_watsonx_ai.helpers.connections.flight_service import (
                FlightConnection,
            )

            headers_ = cast(dict, headers_)
            number_of_batch_rows = cast(int, number_of_batch_rows)
            self.connection = FlightConnection(
                headers=headers_,
                sampling_type=self.sampling_type,
                label=self.experiment_metadata["prediction_column"],
                learning_type=self.experiment_metadata["prediction_type"],
                params=self.experiment_metadata,
                project_id=self.experiment_metadata.get(
                    "project_id", getattr(self._api_client, "default_project_id", None)
                ),
                space_id=self.experiment_metadata.get(
                    "space_id", getattr(self._api_client, "default_space_id", None)
                ),
                asset_id=(
                    None
                    if is_cos_asset
                    else dict_connection.get("location", {}).get("id")
                ),  # do not pass asset id for data assets located on COS
                connection_id=dict_connection.get("connection", {}).get("id"),
                data_location=dict_connection,
                data_batch_size_limit=self.sample_size_limit,
                flight_parameters=kwargs.get("flight_parameters", {}),
                extra_interaction_properties=kwargs.get(
                    "extra_interaction_properties", {}
                ),
                fallback_to_one_connection=kwargs.get(
                    "fallback_to_one_connection", True
                ),
                number_of_batch_rows=number_of_batch_rows,
                stop_after_first_batch=stop_after_first_batch,
                _api_client=self._api_client,
                return_subsampling_stats=kwargs.get("_return_subsampling_stats", False),
                total_size_limit=self.total_size_limit,
                total_nrows_limit=self.total_nrows_limit,
                total_percentage_limit=self.total_percentage_limit,
            )

        else:

            if (
                dict_connection.get("type") == "fs"
                and "location" in dict_connection
                and "path" in dict_connection["location"]
            ):
                self.connection = LocalBatchReader(
                    file_path=dict_connection["location"]["path"],
                    batch_size=sample_size_limit,
                )

            else:
                raise NotImplementedError(
                    "For local data read please use 'fs' (file system) connection type."
                    "To use remote data read please provide 'experiment_metadata'."
                )

    @property
    def _wml_client(self) -> APIClient:
        # note: backward compatibility
        warn(
            (
                "`_wml_client` is deprecated and will be removed in future. "
                "Instead, please use `_api_client`."
            ),
            category=DeprecationWarning,
        )
        # --- end note
        return self._api_client  # type: ignore[return-value]

    @_wml_client.setter
    def _wml_client(self, var: APIClient) -> None:
        # note: backward compatibility
        warn(
            (
                "`_wml_client` is deprecated and will be removed in future. "
                "Instead, please use `_api_client`."
            ),
            category=DeprecationWarning,
        )
        # --- end note
        self._api_client = var

    def _check_authorization(self) -> bool:
        """
        Check if we can authorize with Service.
        If the connection have api_client initialized use it as an attribute.
        Otherwise, credentials should be provided in the experiment_metadata dictionary.
        If the client is properly initialized True will be returned.
        """
        if self._api_client is not None:
            return True

        if self.experiment_metadata is None:
            return False
        credentials = (
            creds
            if (creds := self.experiment_metadata.get("credentials")) is not None
            else self.experiment_metadata.get("wml_credentials")
        )
        if credentials is not None:
            from ibm_watsonx_ai import APIClient

            self._api_client = APIClient(credentials=credentials)
            return True

        elif self.experiment_metadata.get("headers") is not None:
            return True

        else:
            return False

    def _set_size_limit(self, size_limit: int) -> None:
        """If non-default value of total_size_limit was not passed,
        set Sample Size Limit based on T-Shirt size if code is run on training pod:
        For memory < 16 (T-Shirts: XS,S) default is 10MB,
        For memory < 32 & >= 16 (T-Shirts: M) default is 100MB,
        For memory = 32 (T-Shirt L) default is 0.7GB,
        For memory > 32 (T-Shirt XL) or runs outside pod default is 1GB.
        """
        self.total_size_limit: int | None
        from ibm_watsonx_ai.utils.autoai.connection import get_max_sample_size_limit

        max_tshirt_size_limit = (
            get_max_sample_size_limit() if os.getenv("MEM", False) else None
        )  # limit manual setting of sample size limit on autoai clusters #31527

        if self.enable_sampling:
            if max_tshirt_size_limit:
                if (
                    size_limit > max_tshirt_size_limit
                    and size_limit != DEFAULT_SAMPLE_SIZE_LIMIT
                ):
                    raise InvalidSizeLimit(size_limit, max_tshirt_size_limit)
                else:
                    self.total_size_limit = min(size_limit, max_tshirt_size_limit)
            else:
                self.total_size_limit = size_limit
        else:
            if size_limit == DEFAULT_SAMPLE_SIZE_LIMIT:
                self.total_size_limit = None  # do not limit reading if sampling is disabled, we want read all data
            else:
                self.total_size_limit = size_limit

    def write(
        self, data: pd.DataFrame | None = None, file_path: str | None = None
    ) -> None:
        """
        Writes data into data source connection.

        Parameters
        ----------
        data: pandas DataFrame, optional
            Structured data to be saved in dat source connection. (Either 'data' or 'file_path' need to be provided)

        file_path: str, optional
            Path to the local file to be saved in source data connection (binary transfer).
            (Either 'data' or 'file_path' need to be provided)
        """
        if (data is None and file_path is None) or (
            data is not None and file_path is not None
        ):
            raise ValueError("Either 'data' or 'file_path' need to be provided.")

        if data is not None and not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"'data' need to be a pandas DataFrame, you provided: '{type(data)}'."
            )

        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(
                f"'file_path' need to be a string, you provided: '{type(file_path)}'."
            )

        if data is not None:
            self.connection.write_data(data)

        else:
            file_path = cast(str, file_path)
            self.connection.write_binary_data(file_path)

    def __iter__(self) -> Iterator:
        """Iterate over Flight Dataset."""
        if self.authorized:
            if self.enable_sampling:
                if self.sampling_type == SamplingTypes.FIRST_VALUES:
                    return self.connection.iterable_read()
                else:
                    self.connection.enable_subsampling = True
                    return self.connection.iterable_read()
            else:
                if self.binary_data:
                    return self.connection.read_binary_data(read_to_file=self.read_to_file)  # type: ignore[return-value]

                else:
                    self.total_size_limit = None
                    return self.connection.iterable_read()
        else:
            self.connection = cast(LocalBatchReader, self.connection)
            return (batch for batch in self.connection)
