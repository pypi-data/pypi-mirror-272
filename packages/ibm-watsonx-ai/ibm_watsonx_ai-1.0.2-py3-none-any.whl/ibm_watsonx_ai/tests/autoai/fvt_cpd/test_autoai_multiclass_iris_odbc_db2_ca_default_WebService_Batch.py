#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest
import json
from configparser import ConfigParser

from ibm_watsonx_ai.experiment.autoai.optimizers import RemoteAutoPipelines
from ibm_watsonx_ai.helpers.connections import DataConnection, DatabaseLocation
from ibm_watsonx_ai.tests.utils import is_cp4d, get_env
from ibm_watsonx_ai.tests.autoai.abstract_tests_classes import (
    AbstractTestAutoAIRemote)

from ibm_watsonx_ai.wml_client_error import WMLClientError

configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


@unittest.skipIf(True, "ODBC not working yet")
@unittest.skipIf(not is_cp4d(), "ODBC is not tested on cloud yet.")
class TestAutoAIRemote(AbstractTestAutoAIRemote, unittest.TestCase):
    """
    The test can be run on CPD
    The test covers:
    - ODBC DB2 connection set-up
    - downloading training data from connection
    - downloading all generated pipelines to lale pipeline
    - deployment with lale pipeline
    - deployment deletion
    Connection used in test:
     - input: Database connection pointing to DB2.
     - output: null
    """
    prediction_column = 'SPECIES'
    connection_asset_details = json.loads(config.get(get_env(), 'odbc_db2_connection_asset_details'))

    def test_00c_prepare_connection_to_db2(self):
        connection_details = self.api_client.connections.create({
            'datasource_type': self.api_client.connections.get_datasource_type_uid_by_name(
                self.connection_asset_details['datasource_type_name']
            ),
            'name': 'Connection to DB2 for tests',
            'properties': self.connection_asset_details['properties']
        })

        TestAutoAIRemote.connection_id = self.api_client.connections.get_id(connection_details)
        self.assertIsInstance(self.connection_id, str)

    def test_02_DataConnection_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(
            connection_asset_id=self.connection_id,
            location=DatabaseLocation(
                table_name=self.connection_asset_details['table_name']
            )
        )
        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        #self.assertIsNotNone(obj=TestAutoAIRemote.results_connection)

    def test_02a_read_saved_remote_data_before_fit(self):
        TestAutoAIRemote.data = self.data_connection.read()
        print("Data sample:")
        print(self.data.head())
        self.assertGreater(len(self.data), 0)

    def test_03_initialize_optimizer(self):
        AbstractTestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name='Iris - AutoAI',
            prediction_type=self.experiment.PredictionType.MULTICLASS,
            prediction_column=self.prediction_column,
            scoring=self.experiment.Metrics.ACCURACY_SCORE,
            drop_duplicates=False,
            enable_all_data_sources=True,

        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_29_delete_connection_and_connected_data_asset(self):
        self.api_client.connections.delete(self.connection_id)

        with self.assertRaises(WMLClientError):
            self.api_client.connections.get_details(self.connection_id)


if __name__ == '__main__':
    unittest.main()
