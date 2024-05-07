#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import unittest

import numpy as np

from ibm_watsonx_ai.tests.base.abstract.abstract_online_deployment_test import AbstractOnlineDeploymentTest


class TestPyTorchDeployment(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying PyTorch model
    using compressed file.
    """
    JENKINS_RUNTIME = os.getenv('JENKINS_RUNTIME')

    if JENKINS_RUNTIME == "rt23.1":
        software_specification_name = "runtime-23.1-py3.10"
        deployment_type = "pytorch-onnx_rt23.1"
    elif JENKINS_RUNTIME == "rt24.1":
        software_specification_name = "runtime-24.1-py3.11"
        deployment_type = "pytorch-onnx_rt24.1"
    else:
        print("No runtime specification was chose!")

    model_name = deployment_name = "pytorch_model_from_gz"
    file_name = "mnist_pytorch.tar.gz"
    IS_MODEL = True

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'pytorch', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.ModelMetaNames.NAME: self.model_name,
            self.wml_client.repository.ModelMetaNames.TYPE: self.deployment_type,
            self.wml_client.repository.ModelMetaNames.SOFTWARE_SPEC_ID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name)
        }

    def create_scoring_payload(self):
        dataset = np.load(os.path.join(os.getcwd(), 'base', 'datasets', 'pytorch', 'mnist.npz'))
        X = dataset['x_test']

        score_0 = [X[0].tolist()]
        score_1 = [X[1].tolist()]

        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                'values': [score_0, score_1]
            }]
        }


if __name__ == "__main__":
    unittest.main()
