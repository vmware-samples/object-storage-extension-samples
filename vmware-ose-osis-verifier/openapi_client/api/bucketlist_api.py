# coding: utf-8

"""
    Object Storage Interoperability Services API

    This is VMware Cloud Director Object Storage Interoperability Services API. Once storage platform vendor implements REST APIs complying with this specification, Object Storage Extension can integrate with the platform without coding effort.  # noqa: E501

    The version of the OpenAPI document: 1.0.0-oas3
    Contact: wachen@vmware.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from openapi_client.api_client import ApiClient
from openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class BucketlistApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_bucket_list(self, tenant_id, **kwargs):  # noqa: E501
        """Get the bucket list of the platform tenant  # noqa: E501

        Operation ID: getBucketList<br> Get the bucket list of the platform tenant   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_bucket_list(tenant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str tenant_id: The ID of the tenant to get its bueckt list (required)
        :param int offset: The start index of buckets to return
        :param int limit: The maximum number of buckets to return
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PageOfBucketMeta
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_bucket_list_with_http_info(tenant_id, **kwargs)  # noqa: E501

    def get_bucket_list_with_http_info(self, tenant_id, **kwargs):  # noqa: E501
        """Get the bucket list of the platform tenant  # noqa: E501

        Operation ID: getBucketList<br> Get the bucket list of the platform tenant   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_bucket_list_with_http_info(tenant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str tenant_id: The ID of the tenant to get its bueckt list (required)
        :param int offset: The start index of buckets to return
        :param int limit: The maximum number of buckets to return
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PageOfBucketMeta, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'tenant_id',
            'offset',
            'limit'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_bucket_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'tenant_id' is set
        if self.api_client.client_side_validation and ('tenant_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['tenant_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `tenant_id` when calling `get_bucket_list`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'tenant_id' in local_var_params and local_var_params['tenant_id'] is not None:  # noqa: E501
            query_params.append(('tenant_id', local_var_params['tenant_id']))  # noqa: E501
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/api/v1/bucket-list', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PageOfBucketMeta',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
