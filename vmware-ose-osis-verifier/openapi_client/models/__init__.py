# coding: utf-8

# flake8: noqa
"""
    Object Storage Interoperability Services API

    This is VMware Cloud Director Object Storage Interoperability Services API. Once storage platform vendor implements REST APIs complying with this specification, Object Storage Extension can integrate with the platform without coding effort.  # noqa: E501

    The version of the OpenAPI document: 1.0.0-oas3
    Contact: wachen@vmware.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from openapi_client.models.information import Information
from openapi_client.models.inline_response200 import InlineResponse200
from openapi_client.models.osis_bucket_meta import OsisBucketMeta
from openapi_client.models.osis_error import OsisError
from openapi_client.models.osis_s3_capabilities import OsisS3Capabilities
from openapi_client.models.osis_s3_capabilities_exclusions import OsisS3CapabilitiesExclusions
from openapi_client.models.osis_s3_credential import OsisS3Credential
from openapi_client.models.osis_tenant import OsisTenant
from openapi_client.models.osis_usage import OsisUsage
from openapi_client.models.osis_user import OsisUser
from openapi_client.models.page_info import PageInfo
from openapi_client.models.page_of_bucket_meta import PageOfBucketMeta
from openapi_client.models.page_of_s3_credentials import PageOfS3Credentials
from openapi_client.models.page_of_tenants import PageOfTenants
from openapi_client.models.page_of_users import PageOfUsers
from openapi_client.models.refresh_request import RefreshRequest
from openapi_client.models.refresh_response import RefreshResponse
