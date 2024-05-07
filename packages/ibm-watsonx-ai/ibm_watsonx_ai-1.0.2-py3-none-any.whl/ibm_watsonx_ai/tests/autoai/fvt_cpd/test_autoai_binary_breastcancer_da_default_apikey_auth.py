#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest

import ibm_boto3
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.helpers.connections import DataConnection, S3Location
from ibm_watsonx_ai.wml_client_error import WMLClientError
from ibm_watsonx_ai.tests.utils import bucket_exists, create_bucket, is_cp4d
from ibm_watsonx_ai.tests.autoai.abstract_tests_classes import (
    AbstractTestAutoAIAsync,
    AbstractTestWebservice,
)

from ibm_watsonx_ai.tests.utils import get_wml_credentials, is_cp4d

from ibm_watsonx_ai.utils.autoai.enums import (
    PredictionType,
    Metrics,
    ClassificationAlgorithms,
)


@unittest.skipIf(not is_cp4d(), "Not supported on cloud")
class TestAutoAIRemote(AbstractTestAutoAIAsync, unittest.TestCase):
    """
    The test can be run on CPD only
    """

    cos_resource = None
    data_location = "./autoai/data/breast_cancer.csv"

    data_cos_path = "data/breast_cancer.csv"

    SPACE_ONLY = False

    OPTIMIZER_NAME = "breast_cancer test sdk"

    target_space_id = None

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        prediction_type=PredictionType.BINARY,
        prediction_column="diagnosis",
        positive_label="M",
        scoring=Metrics.AVERAGE_PRECISION_SCORE,
        max_number_of_estimators=1,
        include_only_estimators=[ClassificationAlgorithms.LR],
    )

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.credentials = get_wml_credentials()
        try:
            cls.credentials.password = None
        except:
            pass
        try:
            cls.credentials.bedrock_url = None
        except:
            pass

        assert cls.credentials.username is not None
        assert cls.credentials.password is None
        assert cls.credentials.bedrock_url is None
        assert cls.credentials.api_key is not None
        cls.api_client = APIClient(credentials=cls.credentials)

        cls.project_id = cls.credentials.__dict__.get("project_id")

    def test_00d_prepare_data_asset(self):
        asset_details = self.api_client.data_assets.create(
            name=self.data_location.split("/")[-1], file_path=self.data_location
        )

        TestAutoAIRemote.asset_id = self.api_client.data_assets.get_id(asset_details)
        self.assertIsInstance(self.asset_id, str)

    def test_02_data_reference_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(data_asset_id=self.asset_id)
        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        self.assertIsNone(obj=TestAutoAIRemote.results_connection)

    def test_99_delete_data_asset(self):
        self.api_client.data_assets.delete(self.asset_id)

        with self.assertRaises(WMLClientError):
            self.api_client.data_assets.get_details(self.asset_id)


if __name__ == "__main__":
    unittest.main()
