#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import unittest

from ibm_watsonx_ai.tests.base.abstract.abstract_deep_learning_test import \
    AbstractDeepLearningTest


class TestPyTorchTraining(AbstractDeepLearningTest, unittest.TestCase):
    """
    Test case checking the scenario of training an PyTorch model
    using model_definition only.
    """

    model_definition_name = "pytorch_model_definition"
    training_name = "test_pytorch_training"
    training_description = "torch-test-experiment"
    software_specification_name = "pytorch-onnx_rt23.1-py3.10"
    execution_command = "python torch_mnist.py --epochs 1"

    data_location = os.path.join(os.getcwd(), "base", "datasets", "tensorflow", "mnist.npz")
    data_cos_path = "mnist.npz"
    model_paths = [
        os.path.join(os.getcwd(), "base", "artifacts", "pytorch", "pytorch-model.zip")
    ]
    model_definition_ids = []
