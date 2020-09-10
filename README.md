
Oject Storage Extension Samples

## Overview
[VMware Cloud Director Object Storage Extension](https://docs.vmware.com/en/VMware-Cloud-Director-Object-Storage-Extension/index.html) (OSE) is a midware which provides the capability of consuming object storage services for Cloud Director users.

Since version 2.0, OSE opens the extensibility framework for vendor and community to integrate third-party S3 compliant object storage platforms with Cloud Director. The extensibility framework offers a set of REST APIs for the vendor to implement upon the third-party object storage platform, called Object Storage Interoperability Services (OSIS). Below diagram gives the overview of OSE architecture and OSIS' position in the system.

![OSE Architecture](ose-architecture-2-0.png?raw=true)

This open source project includes sample implentation of extensively integrated object storage platforms for OSE, but not limited to these.

## Samples
* [OSIS CEPH Reference Implementation](vmware-ose-ceph-ref-impl/) is an implementation of OSIS for CEPH.
* [OSIS Stub](vmware-ose-osis-stub/) is a Java REST client stub of OSIS specification.
* [OSIS Verifier](vmware-ose-osis-verifier/) is a tool to verify the readiness and compatibiity of the OSIS implementation.

## Contributing

The object-storage-extension-samples project team welcomes contributions from the community. If you wish to contribute code and you have not signed our contributor license agreement (CLA), our bot will update the issue when you open a Pull Request. For any questions about the CLA process, please refer to our [FAQ](https://cla.vmware.com/faq).

All contributions to this repository must be signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md](CONTRIBUTING.md).
