# OSIS Verifier

This is a verifier for implementation of VMware Cloud Director Object Storage Interoperability Services. 

Before integrating with VMware Cloud Director Object Storage Extension and object storage platform, it is recommended to run this tool to verify the OSIS implementation, which would find issues with less effort.



## Requirements.

Python 3.4+

## Installation & Usage

### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install -r requirements.txt
```

(you may need to run `pip` with root permission: `sudo pip install -r requirements.txt`)

## Getting Started

Please execute the command `python osis_verify.py` to verify OSIS required APIs:

```python
python osis_verifier.py 
  ___  ____ ___ ____   __     __        _  __ _           
 / _ \/ ___|_ _/ ___|  \ \   / /__ _ __(_)/ _(_) ___ _ __ 
| | | \___ \| |\___ \   \ \ / / _ \ '__| | |_| |/ _ \ '__|
| |_| |___) | | ___) |   \ V /  __/ |  | |  _| |  __/ |   
 \___/|____/___|____/     \_/ \___|_|  |_|_| |_|\___|_|   
                                                          

Input OSIS Endpoint: [example - https://localhost:8443]https://localhost:9443
Input OSIS Username: MPG0RVCDCDDTSRJJONJK
Input OSIS Password :c5XMURa3Eu3KGPvHDmwTw8GQSOzDujfmNA94tlPh
Input OSIS S3 Endpoint: [example - http://ceph.osis.ose.vmware.com:31383]http://ceph.osis.ose.vmware.com:31383
************************************************************
* The verification items                                   *
************************************************************
0. Quit the verifier
1. Verify S3 Capabilities API
2. Verify S3 Credential APIs
3. Verify Info API
4. Verify Tenant APIs
5. Verify User APIs
6. Verify tenant/user onboard and S3 request

What's your choice?

```

Once there is any error during verifying, check the log file `osis-verifier.log` for details. 

## Author

wachen@vmware.com