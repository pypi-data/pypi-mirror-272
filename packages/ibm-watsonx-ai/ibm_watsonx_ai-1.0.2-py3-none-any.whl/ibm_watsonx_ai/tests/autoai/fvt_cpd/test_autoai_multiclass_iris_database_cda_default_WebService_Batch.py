"""
**Warning**
In order to execute those tests correctly please make sure data is already placed
under the specified location /schema_name/table_name.
(You can easily do this by running the `test_autoai_project_iris_using_database_connection.py` before those tests).
"""

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest
from os import getenv
from ibm_watsonx_ai.tests.utils import is_cp4d
from ibm_watsonx_ai.tests.autoai.abstract_tests_classes import \
    AbstractTestAutoAIConnectedAsset


@unittest.skipIf(getenv('FIPS', 'false').lower() == 'true', "SQL Server not supported on FIPS clusters")
@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIMSSQLServer(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "sqlserver"
    schema_name = "tm_wml_kb"
    max_connection_nb = None


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIDB2(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "db2cloud"
    schema_name = "LWH10123"
    table_name = "IRIS"
    prediction_column = "SPECIES"
    max_connection_nb = 1


@unittest.skipIf(getenv('FIPS', 'false').lower() == 'true', "Postgres SQL not supported on FIPS clusters")
@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIPostgresSQL(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "postgresql"
    schema_name = "public"
    max_connection_nb = 4


@unittest.skipIf(getenv('FIPS', 'false').lower() == 'true', "MySQL not supported on FIPS clusters")
@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
@unittest.skip("The writing of training data is broken for now.")
class TestAutoAIMySQL(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "mysql"  # prefix for credentials section of DB creds in confing.ini
    schema_name = "TM_WML_KB_DB_1"


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIExasol(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "exasol"  # not in Datasource portal
    schema_name = "EXA_SVT"
    table_name = "IRIS"
    prediction_column = "species"
    max_connection_nb = 2

    def test_00c_prepare_connection_to_DATABASE(self):
        from tests.utils import get_db_credentials
        import os

        TestAutoAIExasol.db_credentials = get_db_credentials(self.database_name)

        driver_file_path = os.path.join(os.getcwd(), "autoai", "db_driver_jars", "exajdbc-7.1.4.jar")
        driver_file_name = driver_file_path.split('/')[-1]

        self.api_client.connections.upload_db_driver(driver_file_path)
        self.api_client.connections.list_uploaded_db_drivers()

        TestAutoAIExasol.db_credentials['jar_uris'] = self.api_client.connections.sign_db_driver_url(driver_file_name)

        connection_details = self.api_client.connections.create({
            'datasource_type': self.api_client.connections.get_datasource_type_uid_by_name(self.database_name),
            'name': 'Connection to DB for python API tests',
            'properties': self.db_credentials
        })

        TestAutoAIExasol.connection_id = self.api_client.connections.get_id(connection_details)
        self.assertIsInstance(self.connection_id, str)


@unittest.skipIf(getenv('FIPS', 'false').lower() == 'true', "DataStax not supported on FIPS clusters")
@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
@unittest.skip("Not ready - missing valid credentials details")
class TestAutoAIDataStax(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = 'datastax-ibmcloud'
    schema_name = "conndb"  # keyspace
    table_name = "IRIS4"
    prediction_column = "species"
    data_location = './autoai/data/iris_dataset_index.csv'
    max_connection_nb = 2


@unittest.skipIf(getenv('FIPS', 'false').lower() == 'true', "Oracle not supported on FIPS clusters")
class TestAutoAIOracle(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "oracle"  # Amazon RDS for Oracle
    schema_name = "TESTUSER"
    table_name = "IRIS"
    max_connection_nb = None


@unittest.skip("Teradata instance is not available")
class TestAutoAITeradata(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "teradata"  # Not supported, Not in Datasource Portal
    schema_name = "conndb"
    table_name = "IRIS"
    max_connection_nb = None


class TestAutoAIGenericS3(AbstractTestAutoAIConnectedAsset, unittest.TestCase):
    database_name = "generics3"  # not in Datasource Portal
    bucket_name = 'dnd-tests-s3-connection-2023-11-28-8vcd83bi'
    data_cos_path = 'iris_dataset_train.csv'

    max_connection_nb = None

    def test_00d_prepare_connected_data_asset(self):
        asset_details = self.api_client.data_assets.store({
            "connection_id": self.connection_id,
            "name": "Data asset for tests",
            "data_content_name": f"/{self.bucket_name}/{self.data_cos_path}"
        })

        AbstractTestAutoAIConnectedAsset.asset_id = self.api_client.data_assets.get_id(asset_details)
        self.assertIsInstance(self.asset_id, str)


#
if __name__ == "__main__":
    unittest.main()
