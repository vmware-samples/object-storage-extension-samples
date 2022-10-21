
# OSIS CEPH Reference Implementation
* [Abstract](#abstract)
* [Preliminaries](#preliminaries)
* [Quick Start Guide](#quick-start-guide)
   * [Prepare Building Environment](#prepare-building-environment)
   * [Configure the project](#configure-the-project)
   * [Build the project](#build-the-project)
   * [Run the project](#run-the-project)
   * [Test accessing APIs](#test-accessing-apis)
* [Design](#design)
   * [Models](#models)
      * [OSIS TENANT and CEPH USER](#osis-tenant-and-ceph-user)
      * [OSIS USER and CEPH USER](#osis-user-and-ceph-user)
      * [OSIS S3CREDENTIAL and CEPH USER](#osis-s3credential-and-ceph-user)
* [API Documentation](#api-documentation)
      * [Info API](#info-api)
      * [S3 Capabilities API](#s3-capabilities-api)
* [Troubleshooting](#troubleshooting)
* [Limitation](#limitation)
* [VMware Resouces](#vmware-resouces)


## Abstract

VMware Cloud Director Object Storage Extension (for short, OSE) is a standalone middleware service installed in private data center or public cloud to provide object storage capabilities to the users of VMware Cloud Director.
OSE supports three object storage platforms out of box: Cloudian, Dell EMC ECS and Amazon S3. 

OSIS (Object Storage Interoperability Service) is proposed to extend OSE to support other object storage platforms by defining unified administrative interfaces for storage platforms.

For the platforms integrated with OSE via OSIS, the data channel is between OSE and the platform, but the control channel is between OSE and OSIS implementation (REST services implementing OSIS).
This project is a reference project for OSIS which integrates [CEPH](https://ceph.io/) with OSE. 

## Preliminaries

- Java 1.8
- Gradle 6.5.1+ 
- VMware Cloud Director (10.0+) and Object Storage Extension(2.0+)
- CEPH (15.2+)
- Keep clock of OSE server, OSIS server and CEPH cluster synchronized

## Quick Start Guide

### Prepare Building Environment

- [Install Java 1.8](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)
- [Install Gradle](https://gradle.org/install/)

### Configure the project

Edit `src/main/resources/application.yml` to fill in the CEPH RGW endpoint, S3 endpoint and dashboard access information.
Also edit `src/main/resources/s3capabilities.json` if necessary, which defines the S3 capabilities of the integrated storage platform. The current S3 capabilities are for CEPH 15.2.3 release.

### Build the project

`./gradlew clean build`

### Run the project

`java -jar build/libs/osis.ceph-1.0.0.jar`

### Test accessing APIs

Info API is anonymous accessible.
`curl --request GET 'http://localhost:8080/api/info`

S3 capabilities resource requires basic authentication. The username and password is the credential of RGW endpoint configured in `appication.yml`.

```
curl --request GET 'http://localhost:8080/api/v1/s3capabilities' \
--header 'Authorization: Basic TVBHMFJWQ0RDRERUU1JKSk9OSks6YzVYTVVSYTNFdTNLR1B2SERtd1R3OEdRU096RHVqZm1OQTk0dGxQaA=='
```

## Design

### Models

OSIS CEPH RI works as broker between OSE and CEPH.

It provides unified administrative interfaces for OSE to consume CEPH functionality like user management, credential management and so on.
Also It maps OSIS data model with CEPH data model. As a reference project for OSIS, there is no database included; 
instead we leverage native CEPH model to persist data of OSIS model.

In other words, OSE is only aware of OSIS data models, but not storage platform data models.

#### OSIS TENANT and CEPH USER

CEPH has no dedicted model fro tenant. OSIS combines Cloud Director tenant name and ID with double underscores as OSIS tenant ID. Then use `OSIS_TENANT.tenant_id` as both `CEPH_USER.tenant` and `CEPH_USER.user_id`. Such CEPH user represents a storage platform "tenant" which can be mapped with Cloud Director Org.

| OSIS TENANT | CEPH USER |
| ------ | ------ |
| tenant_id | tenant<br />user_id |
| active | suspended |
| cd_tenant_ids | display_name.cdtids |

Here is the explanation of creating tenant via the OSIS RI project.

1. OSIS RI gets request from OSE to create tenant; `uuid-1` is uuid of Cloud Director tenant.
   Here, the request from OSE is of OSIS tenant model. 

`POST /api/v1/tenants`
```json
{
  "name": "ACME",
  "active": true,
  "cd_tenant_ids": [
    "uuid-1"
  ]
}
```

2. OSIS RI generates tenant ID of OSIS tenant model as below. It combines Cloud Director tenant name and ID with double underscores.

```json
{
  "name": "ACME",
  "active": true,
  "tenant_id": "ACME__uuid-1",
  "cd_tenant_ids": [
    "uuid-1"
  ]
}
```

3. OSIS RI converts OSIS tenant model to CEPH user model. `display_name` is the property used to persist additional tenant data.

   `cdtids` is the key and `uuid-1` is the value; they save the Cloud Director tenant ID in CEPH model.

```json
{
  "tenant": "ACME__uuid-1",
  "user_id": "ACME__uuid-1",
  "suspended": false,
  "display_name": "cdtids::uuid-1" 
}
```

4. OSIS RI sends the CEPH user model to CEPH platform to create user (this is because CEPH has no independent API for tenant operations)


`PUT /admin/user?uid=ACME__uuid-1$ACME__uuid-1&suspended=false&display-name=cdtids::uuid-1`

5. Eventually OSE gets response of tenant creation. OSE doesn't care how `tenant_id` is generated - it sends ID of Cloud Director tenant to OSIS RI and receives ID of new created platform tenant  

```json
{
  "name": "ACME",
  "active": true,
  "tenant_id": "ACME__uuid-1",
  "cd_tenant_ids": [
    "uuid-1"
  ]
}
```

##### Impacts on Tenant Onboard 

Now that CEPH user is used to represent a storage tenant, it is worth explaining how it works in two kinds of tenant onboard.

**Tenant Default Onboard**

In this style of tenant onboard, OSE is responsible to create a special user in CEPH RGW via OSIS adaptor.

For example, there is a Cloud Director Org: `name = ACME` and `ID = 9bce3e30622a42ec8580b62e49116586`.

By default, the OSIS RI project will construct OSIS tenant model then create a special user in CEPH RGW according to the mapping rule above.

| OSIS TENANT                                        | CEPH USER                                                    |
| -------------------------------------------------- | ------------------------------------------------------------ |
| tenant_id = ACME__9bce3e30622a42ec8580b62e49116586 | tenant = ACME\_\_9bce3e30622a42ec8580b62e49116586 <br />user_id = ACME\_\_9bce3e30622a42ec8580b62e49116586 |
| active = true                                      | suspended = false                                            |
| cd_tenant_ids = [9bce3e30622a42ec8580b62e49116586] | display_name = cdtids::9bce3e30622a42ec8580b62e49116586      |

**Tenant Onboard with Custom Storage Tenant**

Compared with default onboard, it requires an existing tenant in storage platform, like CEPH. Instead of OSE, administrator should create such CEPH tenant (special user) in advance on CEPH Dashboard. Here are the steps to create OSIS tenant in CEPH 16.2.7.

1. Login CEPH Dashboard
2. Click `Object Gateway` item in left-side navigator 
3. Click `Users` sub-item
4. Click `Create` button
5. In the page for user properties, specify the values:
   1. User ID: `custom_tenant_1`
   2. Tenant: `custom_tenant_1`
   3. Full name: `cdtids::`
6. Click `Create User` button to complete the creation

With the special CEPH user created, Cloud Director provider administrator can find a new storage tenant `custom_tenant_1` in the dropdown list of Active Tenant page.


#### OSIS USER and CEPH USER
| OSIS USER | CEPH USER |
| ------ | ------ |
| user_id | user_id |
| canonical_user_id | uid | 
| tenant_id | tenant | 
| cd_user_id | display_name.cduid | 
| cd_tenant_id | display_name.cdtid | 
| username | display_name.un | 
| active | suspended | 
| email | email | 
| role | caps | 


An example of creating user as below.

1. OSIS RI gets request from OSE to create user.


`POST /api/v1/tenants/ACME__uuid-1/users`
```json
{
  "active": true,
  "username": "rachelw",
  "email": "rachelw@acme.com",
  "role": "PROVIDER_ADMIN",
  "cd_user_id": "uuid-a",
  "cd_tenant_id": "uuid-1"
}
```

2. OSIS RI uses ID of Cloud Director user as ID of OSIS user model, and generates the complete OSIS user

```json
{
    "user_id": "uuid-a",
    "canonical_user_id": "ACME__uuid-1$uuid-a",
    "tenant_id": "ACME__uuid-1",
    "active": true,
    "cd_user_id": "uuid-a",
    "cd_tenant_id": "uuid-1",
    "username": "rachelw",
    "email": "rachelw@acme.com",
    "role": "TENANT_ADMIN"
}
```

3. OSIS RI converts OSIS user model to CEPH user model. 
   User name, Cloud Director tenant ID and user ID are persisted in CEPH user's display_name.
   OSIS user role is mapped to CEPH user caps - TENANT_ADMIN has permissions for users/buckets/metadata/usage.

```json
{
    "display_name": "dn::rachelw;;cdtid::uuid-1;;cduid::uuid-a",
    "email": "rachelw@acme.com",
    "tenant": "ACME__uuid-1",
    "user_id": "uuid-a",
    "suspended": 0,
    "caps": [
        "users=*",
        "buckets=*",
        "metadata=*",
        "usage=read"
    ]
}
```

4. OSIS RI sends CEPH user model to CEPH to create new user and converts the CEPH result to OSIS model

`PUT /admin/user?uid=ACME__uuid-1$uuid-a&tenant=ACME_uuid-1&suspended=false&email=rachelw@acme.com&caps=users=*; buckets=*; metadata=*; usage=read&display-name=un::rachelw;;cdtid::uuid-1;;cduid::uuid-a`

5. Eventually OSE gets response of user creation. OSE doesn't care how `user_id` is generated - it sends ID of Cloud Director user to OSIS RI and receives ID of new created platform user  

```json
{
    "user_id": "uuid-a",
    "canonical_user_id": "ACME__uuid-1$uuid-a",
    "tenant_id": "ACME__uuid-1",
    "active": true,
    "cd_user_id": "uuid-a",
    "cd_tenant_id": "uuid-1",
    "username": "rachelw",
    "email": "rachelw@acme.com",
    "role": "TENANT_ADMIN"
} 
```

#### OSIS S3CREDENTIAL and CEPH USER

CEPH has no dedicated model for S3 credential, which only exists as part of CEPH user model.
| OSIS S3CREDENTIAL | CEPH USER |
| ------ | ------ |
| access_key | keys |
| secret_key | keys | 
| active | suspended | 
| creation_date | not available for CEPH | 
| tenant_id | tenant_id | 
| user_id | user_id | 
| username | display_name.un | 
| cd_user_id | display_name.cduid | 
| cd_tenant_id | display_name.cdtid | 

Here is an example for S3 credential creation

1. OSIS implementation gets request from OSE to create S3 credential

`POST /api/v1/tenants/uuid-1/users/uuid-a/s3credentials`

2. OSIS implementation constructs CEPH uid and sends request to CEPH for S3 credential creation

`PUT /admin/user?key&uid=uuid-1$uuid-a&generate-key=true`

3. OSIS implementation converts CEPH result to OSIS S3 credential model and returns to OSE

```json
{
  "access_key": "access-key",
  "secret_key": "secret-key",
  "active": true,
  "tenant_id": "ACME__uuid-1",
  "user_id": "uuid-a",
  "username": "rachelw",
  "cd_user_id": "uuid-a",
  "cd_tenant_id": "uuid-1"
}
```

## API Documentation
[OSIS Specification in OpenAPI](https://code.vmware.com/apis/1034)

The API documentation provides details for each OSIS API. 
Two of them need highlighting as they handle the difference of OSIS implementation and the storage platforms.

#### Info API

Info API gives metadata of the OSIS implementation, like storage platform's name and version, OSIS API version, logo URI and so on.
Pay attention to the property `not_implemented`, which tells OSE which optional OSIS APIs are not implemented. Thus OSE can show the UI components adaptively.

#### S3 Capabilities API

Different object storage platforms have roughly compatible S3 APIs. However, each platform always has its own customization which is not compatible with Amazon S3.
To deal with the gap, S3 capabilities API specifies which S3 APIs are not supported on current platform. Typically there are 4 kinds of unsupported capabilities:

1. the S3 API is not supported at all
2. specific URL parameter is not supported
3. specific HTTP header is not supported
4. specific options in HTTP payload is not supported 

Here is an example showing 4 kinds of capability exclusion.
```json
{
    "exclusions": {
        "get_bucket_lifecycle": {},
        "create_bucket": {
            "by_headers": [
                "x-amz-grant-full-control"
            ]
        },
        "get_object": {
            "by_params": [
                "responseExpires"
            ]
        },
        "put_bucket_versioning": {
            "by_payload": [
                "mfaDelete"
            ]
        }
    }
}
```

## Troubleshooting

## Limitation
CEPH doesn't accept "-" in tenant name. In this project, it will normalize the tenant name by removing "-", which may results in conflict for two tenants have names "tenant-name" and "tenantname".


## VMware Resouces
[VMware Cloud Director Object Storage Extension Documentation](https://docs.vmware.com/en/VMware-Cloud-Director-Object-Storage-Extension/index.html)
