#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest

from ibm_watsonx_ai.helpers.connections import DataConnection, S3Location
from ibm_watsonx_ai.wml_client_error import WMLClientError
from ibm_watsonx_ai.tests.utils import bucket_exists, create_bucket, is_cp4d, save_data_to_cos_bucket
from ibm_watsonx_ai.tests.autoai.abstract_tests_classes import AbstractTestAutoAISync, \
    AbstractTestWebservice, AbstractTestBatch

from ibm_watsonx_ai.utils.autoai.enums import PredictionType, Metrics


class TestAutoAIRemote(AbstractTestAutoAISync, AbstractTestWebservice, AbstractTestBatch, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """

    cos_resource = None
    data_location = './autoai/data/CarPrice_Assignment.csv'
    sheet_name = 'price'
    sheet_number = 1

    data_cos_path = 'data/CarPrice_Assignment.csv'
    batch_payload_location = './autoai/data/scoring_payload/CarPrice_Assignment_scoring_payload.csv'
    batch_payload_cos_location = 'scoring_payload/CarPrice_Assignment_scoring_payload.csv'

    BATCH_DEPLOYMENT_WITH_CA = True
    BATCH_DEPLOYMENT_WITH_DF = True
    BATCH_DEPLOYMENT_WITH_CDA = False
    BATCH_DEPLOYMENT_WITH_DA = False

    SPACE_ONLY = True

    OPTIMIZER_NAME = "CarPrice test sdk"

    target_space_id = None

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        desc='test description',
        prediction_type=PredictionType.REGRESSION,
        prediction_column='price',
        scoring=Metrics.EXPLAINED_VARIANCE_SCORE,
        max_number_of_estimators=1,
        text_processing=False,
        drop_duplicates=False,
        daub_give_priority_to_runtime=2,
        train_sample_rows_test_size=0.8
    )

    def test_00b_prepare_COS_instance(self):
        TestAutoAIRemote.bucket_name = save_data_to_cos_bucket(self.data_location,
                                                               self.data_cos_path,
                                                               access_key_id=self.cos_credentials['cos_hmac_keys'][
                                                                   'access_key_id'],
                                                               secret_access_key=self.cos_credentials['cos_hmac_keys'][
                                                                   'secret_access_key'],
                                                               cos_endpoint=self.cos_endpoint,
                                                               bucket_name=self.bucket_name)

    def test_00c_prepare_connection_to_COS(self):
        connection_details = self.api_client.connections.create({
            'datasource_type': self.api_client.connections.get_datasource_type_uid_by_name('bluemixcloudobjectstorage'),
            'name': 'Connection to COS for tests',
            'properties': {
                'bucket': self.bucket_name,
                'access_key': self.cos_credentials['cos_hmac_keys']['access_key_id'],
                'secret_key': self.cos_credentials['cos_hmac_keys']['secret_access_key'],
                'iam_url': self.api_client.service_instance._href_definitions.get_iam_token_url(),
                'url': self.cos_endpoint
            }
        })

        TestAutoAIRemote.connection_id = self.api_client.connections.get_id(connection_details)
        self.assertIsInstance(self.connection_id, str)

    def test_02_data_reference_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(
            connection_asset_id=self.connection_id,
            location=S3Location(
                bucket=self.bucket_name,
                path=self.data_cos_path
            )
        )
        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        self.assertIsNone(obj=TestAutoAIRemote.results_connection)

    def test_99_delete_connection_and_connected_data_asset(self):
        if not self.SPACE_ONLY:
            self.api_client.set.default_project(self.project_id)
        self.api_client.connections.delete(self.connection_id)

        with self.assertRaises(WMLClientError):
            self.api_client.connections.get_details(self.connection_id)


if __name__ == '__main__':
    unittest.main()
