# coding: utf-8

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from pprint import pformat
from six import iteritems
import re


class ModelSchemas(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, input=None, output=None):
        """
        ModelContentLocation - location of model content defined in Swagger

        :param dict swaggerTypes: The key is attribute input_output
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute input_output
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'input': 'list[dict(str, str)]',
            'output': 'list[dict(str, str)]'
        }

        self.attribute_map = {
            'input' : 'input',
            'output':'output'
        }

        self._input = input
        self._output = output

    @property
    def input(self):
        """
        Gets the temp cos url of this ModelContentLocation.

        :return: The url of this ModelContentLocation.
        :rtype: dict(str, str)
        """
        return self._input

    @input.setter
    def input(self, input):
        """
        Sets the source of this ModelContentLocation.
        Details of the resource in the content data source

        :param source: The source of this ModelContentLocation.
        :type: dict(str, str)
        """

        self._input = input

    @property
    def output(self):
        """
        Gets the source of this ModelContentLocation.
        Details of the resource in the content source

        :return: The source of this ModelContentLocation.
        :rtype: dict(str, str)
        """
        return self._output

    @output.setter
    def output(self, output):
        """
        Sets the source of this ModelContentLocation.
        Details of the resource in the content data source

        :param source: The source of this ModelContentLocation.
        :type: dict(str, str)
        """

        self._output = output

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
