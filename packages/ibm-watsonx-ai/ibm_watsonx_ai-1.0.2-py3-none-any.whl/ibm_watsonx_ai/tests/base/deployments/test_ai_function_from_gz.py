#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import unittest


from ibm_watsonx_ai.tests.base.abstract.abstract_online_deployment_test import AbstractOnlineDeploymentTest


class TestAIFunction(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying a Python function
    using compressed file.
    """
    JENKINS_RUNTIME = os.getenv('JENKINS_RUNTIME')

    if JENKINS_RUNTIME == "rt23.1":
        software_specification_name = "runtime-23.1-py3.10"
    elif JENKINS_RUNTIME == "rt24.1":
        software_specification_name = "runtime-24.1-py3.11"
    else:
        print("No runtime specification was chose!")

    model_name = deployment_name = "ai_function_from_gz_test"
    file_name = "ai_function.gz"
    IS_MODEL = False

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'python_function', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.FunctionMetaNames.NAME: self.model_name,
            self.wml_client.repository.FunctionMetaNames.SOFTWARE_SPEC_ID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name)
        }

    def create_scoring_payload(self):
        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                "fields": ["Gender", "Status", "Children", "Age", "Customer_Status"],
                "values": [
                    ["Male", "M", 2, 48, "Inactive"],
                    ["Female", "S", 0, 23, "Inactive"]
                ]
            }]
        }


if __name__ == "__main__":
    unittest.main()
