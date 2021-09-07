# Overview

For a new OSE OSIS Adapter, you need to implement a set of OSIS APIs defined by [Object Storage Interoperability Service](https://code.vmware.com/apis/1034). Not all API endpoints are required as the beginning. You can find two API categories.
* [Required](https://code.vmware.com/apis/1034#/required)
* [Optional](https://code.vmware.com/apis/1034#/optional)

Required APIs are mandatory to make OSE work for the new Object Storage platform.

# Deveopment Kit

To faciliate for your OSIS Adapter development, we provide a number of resources on Github.
* [OSIS CEPH Reference Implementation](../vmware-ose-osis-ceph-ri/) is an implementation of OSIS for CEPH.
* [OSIS Stub](../vmware-ose-osis-stub/) is a Java REST client stub of OSIS specification.
* [OSIS Verifier](../vmware-ose-osis-verifier/) is a tool to verify the readiness and compatibiity of the OSIS implementation.

# System Requirement 

The OSIS Adapter needs to be developed as an API service available to VMware Cloud Director Object Storage Extension (OSE) server. You can implement the OSIS Adapter in any programming language and deployed to any server environment. The only requirement on the OSIS Adapter is the network connectivity. It should be deployed in an intranet that OSE server can connect to it, and it can connect to the storage platform.

![OSIS Topology](../assets/osis-topo.png?raw=true)

## Best Practice

If you install the OSIS Adapter in a standalone machine, below hardware configuration is recommended.

* **vCPU**: 4 Core
* **Memory**: 8GB
* **Disk**: 100GB
* **OS**: Linux (CentOS 7+ is recommend)
* **Database**: PostgreSQL 10+

As a best practice, the OSIS Adapter can be installed to the same node as OSE server, and share same PostgreSQL database server that OSE uses. In this way, the additional maintenance effort can be mostly reduced. 

![OSIS Network](../assets/osis-network.png?raw=true)