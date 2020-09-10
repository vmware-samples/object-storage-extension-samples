# OSIS Stub Project



## Abstract

VMware Cloud Director Object Storage Extension (for short, OSE) is a standalone middleware service installed in private data center or public cloud to provide object storage capabilities to the users of VMware Cloud Director.
OSE supports three object storage platforms out of box: Cloudian, Dell EMC ECS and Amazon S3. 

OSIS (Object Storage Interoperability Service) is proposed to extend OSE to support other object storage platforms by defining unified administrative interfaces for storage platforms.

For the platforms integrated with OSE via OSIS, the data channel is between OSE and the platform, but the control channel is between OSE and OSIS implementation (REST services implementing OSIS).

This is a stub project for OSIS, which provides the skeleton for developer to start their work.

## Usage
The project has stub and default implementation. Add or modify anything necessary to make it work for new storage platform support.

Module `platform-admin-client` is for platform administrative client.

Module `osis-core` has the project implementation.
- package `com.vmware.osis.model` contains OSIS models
- package `com.vmware.osis.security` contains default implementation of two authentication schema: Basic and API token
- interface `com.vmware.osis.service.OsisService` provides the methods OSIS models manipulation, which should be implemented by `com.vmware.osis.platform.service.impl.PlatformOsisService`
- any required beans can be declared in `com.vmware.osis.platform.configuration.PlatformConfig`
- package `com.vmware.osis.platform.security` contains default implementation for platform specific user data
- class `com.vmware.osis.platform.utils.ModelConverter` should provides the methods to convert OSIS and platform models
- class `com.vmware.osis.platform.AppEnv` holds any application properties
- class `com.vmware.osis.resource.OsisCapsManager` gives default implementation to collect the APIs annotated with `@NotImplemented` 

Module `osis-app` has the REST interfaces of OSIS services
class `com.vmware.osis.resource.OsisController` has default implementation of the OSIS REST controller

## Reference
Please also refer the OSIS development guide to get more information about how to implement OSIS services for the object storage platform.


