# coding: utf-8

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from pprint import pformat
from six import iteritems


class MlAssetsCreateLibrariesOutputArray(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, first=None, next=None, limit=None, resources=None):
        """
        MlAssetsCreateLibrariesOutputArray - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'first': 'MlAssetsCreateLibrariesOutputArrayFirst',
            'next': 'MlAssetsCreateLibrariesOutputArrayFirst',
            'limit': 'float',
            'resources': 'list[MlAssetsCreateLibrariesOutput]'
        }

        self.attribute_map = {
            'first': 'first',
            'next': 'next',
            'limit': 'limit',
            'resources': 'resources'
        }

        self._first = first
        self._next = next
        self._limit = limit
        self._resources = resources

    @property
    def first(self):
        """
        Gets the first of this MlAssetsCreateLibrariesOutputArray.


        :return: The first of this MlAssetsCreateLibrariesOutputArray.
        :rtype: MlAssetsCreateLibrariesOutputArrayFirst
        """
        return self._first

    @first.setter
    def first(self, first):
        """
        Sets the first of this MlAssetsCreateLibrariesOutputArray.


        :param first: The first of this MlAssetsCreateLibrariesOutputArray.
        :type: MlAssetsCreateLibrariesOutputArrayFirst
        """
        self._first = first

    @property
    def next(self):
        """
        Gets the next of this MlAssetsCreateLibrariesOutputArray.


        :return: The next of this MlAssetsCreateLibrariesOutputArray.
        :rtype: MlAssetsCreateLibrariesOutputArrayFirst
        """
        return self._next

    @next.setter
    def next(self, next):
        """
        Sets the next of this MlAssetsCreateLibrariesOutputArray.


        :param next: The next of this MlAssetsCreateLibrariesOutputArray.
        :type: MlAssetsCreateLibrariesOutputArrayFirst
        """
        self._next = next

    @property
    def limit(self):
        """
        Gets the limit of this MlAssetsCreateLibrariesOutputArray.


        :return: The limit of this MlAssetsCreateLibrariesOutputArray.
        :rtype: float
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this MlAssetsCreateLibrariesOutputArray.


        :param limit: The limit of this MlAssetsCreateLibrariesOutputArray.
        :type: float
        """
        self._limit = limit

    @property
    def resources(self):
        """
        Gets the resources of this MlAssetsCreateLibrariesOutputArray.


        :return: The resources of this MlAssetsCreateLibrariesOutputArray.
        :rtype: list[MlAssetsCreateLibrariesOutput]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """
        Sets the resources of this MlAssetsCreateLibrariesOutputArray.


        :param resources: The resources of this MlAssetsCreateLibrariesOutputArray.
        :type: list[MlAssetsCreateLibrariesOutput]
        """
        self._resources = resources

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

