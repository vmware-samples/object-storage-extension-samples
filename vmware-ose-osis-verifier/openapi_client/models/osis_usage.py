# coding: utf-8

"""
    Object Storage Interoperability Services API

    This is VMware Cloud Director Object Storage Interoperability Services API. Once storage platform vendor implements REST APIs complying with this specification, Object Storage Extension can integrate with the platform without coding effort.  # noqa: E501

    The version of the OpenAPI document: 1.0.0-oas3
    Contact: wachen@vmware.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class OsisUsage(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'bucket_count': 'int',
        'object_count': 'int',
        'total_bytes': 'int',
        'available_bytes': 'int',
        'used_bytes': 'int'
    }

    attribute_map = {
        'bucket_count': 'bucket_count',
        'object_count': 'object_count',
        'total_bytes': 'total_bytes',
        'available_bytes': 'available_bytes',
        'used_bytes': 'used_bytes'
    }

    def __init__(self, bucket_count=None, object_count=None, total_bytes=None, available_bytes=None, used_bytes=None, local_vars_configuration=None):  # noqa: E501
        """OsisUsage - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._bucket_count = None
        self._object_count = None
        self._total_bytes = None
        self._available_bytes = None
        self._used_bytes = None
        self.discriminator = None

        self.bucket_count = bucket_count
        self.object_count = object_count
        self.total_bytes = total_bytes
        if available_bytes is not None:
            self.available_bytes = available_bytes
        self.used_bytes = used_bytes

    @property
    def bucket_count(self):
        """Gets the bucket_count of this OsisUsage.  # noqa: E501

        bucket count of tenant or user  # noqa: E501

        :return: The bucket_count of this OsisUsage.  # noqa: E501
        :rtype: int
        """
        return self._bucket_count

    @bucket_count.setter
    def bucket_count(self, bucket_count):
        """Sets the bucket_count of this OsisUsage.

        bucket count of tenant or user  # noqa: E501

        :param bucket_count: The bucket_count of this OsisUsage.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and bucket_count is None:  # noqa: E501
            raise ValueError("Invalid value for `bucket_count`, must not be `None`")  # noqa: E501

        self._bucket_count = bucket_count

    @property
    def object_count(self):
        """Gets the object_count of this OsisUsage.  # noqa: E501

        object count of tenant or user  # noqa: E501

        :return: The object_count of this OsisUsage.  # noqa: E501
        :rtype: int
        """
        return self._object_count

    @object_count.setter
    def object_count(self, object_count):
        """Sets the object_count of this OsisUsage.

        object count of tenant or user  # noqa: E501

        :param object_count: The object_count of this OsisUsage.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and object_count is None:  # noqa: E501
            raise ValueError("Invalid value for `object_count`, must not be `None`")  # noqa: E501

        self._object_count = object_count

    @property
    def total_bytes(self):
        """Gets the total_bytes of this OsisUsage.  # noqa: E501

        total storage bytes of tenant or user  # noqa: E501

        :return: The total_bytes of this OsisUsage.  # noqa: E501
        :rtype: int
        """
        return self._total_bytes

    @total_bytes.setter
    def total_bytes(self, total_bytes):
        """Sets the total_bytes of this OsisUsage.

        total storage bytes of tenant or user  # noqa: E501

        :param total_bytes: The total_bytes of this OsisUsage.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and total_bytes is None:  # noqa: E501
            raise ValueError("Invalid value for `total_bytes`, must not be `None`")  # noqa: E501

        self._total_bytes = total_bytes

    @property
    def available_bytes(self):
        """Gets the available_bytes of this OsisUsage.  # noqa: E501

        available storage bytes of tenant or user  # noqa: E501

        :return: The available_bytes of this OsisUsage.  # noqa: E501
        :rtype: int
        """
        return self._available_bytes

    @available_bytes.setter
    def available_bytes(self, available_bytes):
        """Sets the available_bytes of this OsisUsage.

        available storage bytes of tenant or user  # noqa: E501

        :param available_bytes: The available_bytes of this OsisUsage.  # noqa: E501
        :type: int
        """

        self._available_bytes = available_bytes

    @property
    def used_bytes(self):
        """Gets the used_bytes of this OsisUsage.  # noqa: E501

        used storage bytes of tenant or user  # noqa: E501

        :return: The used_bytes of this OsisUsage.  # noqa: E501
        :rtype: int
        """
        return self._used_bytes

    @used_bytes.setter
    def used_bytes(self, used_bytes):
        """Sets the used_bytes of this OsisUsage.

        used storage bytes of tenant or user  # noqa: E501

        :param used_bytes: The used_bytes of this OsisUsage.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and used_bytes is None:  # noqa: E501
            raise ValueError("Invalid value for `used_bytes`, must not be `None`")  # noqa: E501

        self._used_bytes = used_bytes

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OsisUsage):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OsisUsage):
            return True

        return self.to_dict() != other.to_dict()