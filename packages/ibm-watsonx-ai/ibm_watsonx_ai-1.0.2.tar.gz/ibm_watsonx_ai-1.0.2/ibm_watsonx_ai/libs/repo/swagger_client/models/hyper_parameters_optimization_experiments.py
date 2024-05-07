# coding: utf-8

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from pprint import pformat
from six import iteritems
import re


class HyperParametersOptimizationExperiments(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, method=None, hyper_parameters=None):
        """
        HyperParametersOptimizationExperiments - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'method': 'HyperParametersOptimizationExperimentsMethod',
            'hyper_parameters': 'list[HyperParametersExperiments]'
        }

        self.attribute_map = {
            'method': 'method',
            'hyper_parameters': 'hyper_parameters'
        }

        self._method = method
        self._hyper_parameters = hyper_parameters

    @property
    def method(self):
        """
        Gets the method of this HyperParametersOptimizationExperiments.


        :return: The method of this HyperParametersOptimizationExperiments.
        :rtype: HyperParametersOptimizationExperimentsMethod
        """
        return self._method

    @method.setter
    def method(self, method):
        """
        Sets the method of this HyperParametersOptimizationExperiments.


        :param method: The method of this HyperParametersOptimizationExperiments.
        :type: HyperParametersOptimizationExperimentsMethod
        """

        self._method = method

    @property
    def hyper_parameters(self):
        """
        Gets the hyper_parameters of this HyperParametersOptimizationExperiments.


        :return: The hyper_parameters of this HyperParametersOptimizationExperiments.
        :rtype: HyperParametersExperiments
        """
        return self._hyper_parameters

    @hyper_parameters.setter
    def hyper_parameters(self, hyper_parameters):
        """
        Sets the hyper_parameters of this HyperParametersOptimizationExperiments.


        :param hyper_parameters: The hyper_parameters of this HyperParametersOptimizationExperiments.
        :type: HyperParametersExperiments
        """

        self._hyper_parameters = hyper_parameters

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
