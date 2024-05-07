#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import unittest
from unittest.mock import Mock


from deployments import Deployments
from href_definitions import HrefDefinitions
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.repository import Repository
from service_instance import ServiceInstance


class TestDeploymentsCreateJobUnittests(unittest.TestCase):

    def setUp(self):
        client = Mock(spec=APIClient)
        client.credentials = {"url": "the-wml-url"}
        client.ICP_PLATFORM_SPACES = True
        client.CLOUD_PLATFORM_SPACES = None
        client.wml_ctoken = ''
        client.repository = Mock(spec=Repository)
        client.repository.get_details = Mock()
        client.repository.get_details.return_value = {'entity': {'type': 'do'}}
        client.service_instance = Mock(spec=ServiceInstance)
        client.service_instance._href_definitions = Mock(spec=HrefDefinitions)
        deployments = Deployments(client)
        deployments.get_details = Mock()
        deployments.get_details.return_value = {'entity': {'asset': {'href': 'foo/bar'}}}
        deployments._score_async = Mock()
        self.deployments = deployments

    def test_create_job_checks_deployment_type(self):
        self.deployments.create_job('deployment_id', {})
        self.deployments._client.repository.get_details.assert_called_once()
        self.deployments.get_details.assert_called_once()
        self.deployments._score_async.assert_called_once()

    def test_create_job_doesnt_check_deployment_type_if_given_asset_id(self):
        self.deployments.create_job('deployment_id', {}, _asset_id='asset-id')
        self.deployments.get_details.assert_not_called()
        self.deployments._client.repository.get_details.assert_called_once()
        self.deployments._score_async.assert_called_once()


if __name__ == '__main__':
    unittest.main()
