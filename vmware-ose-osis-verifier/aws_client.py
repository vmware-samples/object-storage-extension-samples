import logging
from pprint import pprint
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

import requests
import urllib3
from aws_requests_auth.aws_auth import AWSRequestsAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class AwsClient:
    
    def __init__(self, aws_s3, access_key, secret_key, host, region, service) -> None:
        super().__init__()
        self.aws_s3 = aws_s3
        self.auth = AWSRequestsAuth(aws_access_key=access_key,
                                    aws_secret_access_key=secret_key,
                                    aws_host=host,
                                    aws_region=region,
                                    aws_service=service)
    
    def get_buckets(self, params=None):
        rsp = self._ose_get(self._buckets_url(), params=params)
        assert rsp.status_code == 200
        return rsp
    
    @staticmethod
    def _dump_rsp(rsp):
        log.debug('===== RESPONSE DUMP =====')
        log.debug('status code {}'.format(rsp.status_code))
        for h in rsp.headers:
            log.debug('{}={}'.format(h, rsp.headers[h]))
        log.debug(rsp.text)
        log.debug('\n')
    
    def create_bucket(self, bkt):
        rsp = self._ose_put(self._bucket_url(bkt))
        assert rsp.status_code == 200
        return rsp
    
    def head_bucket(self, bkt):
        rsp = self._ose_head(self._bucket_url(bkt))
        return rsp
    
    def delete_bucket(self, bkt):
        rsp = self._ose_delete(self._bucket_url(bkt))
        assert rsp.status_code == 204
        return rsp
    
    def get_bucket_versioning(self, bkt):
        rsp = self._ose_get(self._bucket_url(bkt), params={'versioning': ''})
        assert rsp.status_code == 200
        return rsp
    
    def enable_bucket_versioning(self, bkt):
        rsp = self._ose_put(self._bucket_url(bkt), params={'versioning': ''},
                            data=self._enable_bucket_versioning_body())
        assert rsp.status_code == 200
        return rsp
    
    def suspend_bucket_versioning(self, bkt):
        rsp = self._ose_put(self._bucket_url(bkt), params={'versioning': ''},
                            data=self._suspend_bucket_versioning_body())
        assert rsp.status_code == 200
        return rsp
    
    def create_object(self, bkt, *objects, data=None):
        rsp = self._ose_put(self._object_url(bkt, *objects), data=data)
        assert rsp.status_code == 200
        return rsp
    
    def get_object(self, bkt, *objects, params=None):
        rsp = self._ose_get(self._object_url(bkt, *objects), params=params)
        return rsp
    
    def head_object(self, bkt, *objects, params=None):
        rsp = self._ose_head(self._object_url(bkt, *objects), params=params)
        return rsp
    
    def delete_object(self, bkt, *objects, params=None):
        rsp = self._ose_delete(self._object_url(bkt, *objects), params=params)
        assert rsp.status_code == 204
        return rsp
    
    def delete_version(self, bkt, obj, version):
        rsp = self._ose_delete(self._object_url(bkt, obj), params={'versionId': version})
        assert rsp.status_code == 204
        return rsp
    
    def delete_all_versions(self, bkt, obj):
        rsp = self.list_versions(bkt)
        assert rsp.status_code == 200
        
        for version in rsp.json()['versions']:
            rsp = self.delete_version(bkt, obj, version['versionId'])
            assert rsp.status_code == 204
    
    def list_objects(self, bkt, params=None):
        rsp = self._ose_get(self._bucket_url(bkt), params=params)
        assert rsp.status_code == 200
        return rsp
    
    def list_versions(self, bucket, params=None):
        rsp = self._ose_get(self._versions_url(bucket), params=params)
        assert rsp.status_code == 200
        return rsp
    
    def _buckets_url(self):
        return self.aws_s3
    
    def _bucket_url(self, bkt):
        return '{}/{}'.format(self.aws_s3, bkt)
    
    def _object_url(self, bkt, *objects):
        url = '{}/{}/'.format(self.aws_s3, bkt)
        for obj in objects:
            url += obj
        return url
    
    def _versions_url(self, bkt):
        return '{}/{}?versions'.format(self.aws_s3, bkt)
    
    def _ose_get(self, url, params=None):
        pprint('REQUEST GET =====> {} {}'.format(url, params))
        rsp = requests.get(url, params=params, auth=self.auth, verify=False)
        self._dump_rsp(rsp)
        return rsp
    
    def _ose_head(self, url, params=None):
        pprint('REQUEST HEAD =====> {} {}'.format(url, params))
        rsp = requests.head(url, params=params, auth=self.auth, verify=False)
        self._dump_rsp(rsp)
        return rsp
    
    def _ose_put(self, url, params=None, data=None):
        log.debug('REQUEST PUT =====> {} {}\n'.format(url, params))
        rsp = requests.put(url, params=params, data=data, auth=self.auth, verify=False)
        self._dump_rsp(rsp)
        return rsp
    
    def _ose_post(self, url, params=None, data=None):
        pprint('REQUEST POST =====> {} {}'.format(url, params))
        rsp = requests.post(url, params=params, data=data, auth=self.auth, verify=False)
        self._dump_rsp(rsp)
        return rsp
    
    def _ose_delete(self, url, params=None):
        pprint('REQUEST DELETE =====> {} {}'.format(url, params))
        rsp = requests.delete(url, params=params, auth=self.auth, verify=False)
        self._dump_rsp(rsp)
        return rsp
    
    def _enable_bucket_versioning_body(self):
        return self._dict_to_xml('VersioningConfiguration', {'Status': 'Enabled'})
    
    def _suspend_bucket_versioning_body(self):
        return self._dict_to_xml('VersioningConfiguration', {'Status': 'Suspended'})
    
    @staticmethod
    def _dict_to_xml(tag, d):
        elem = Element(tag)
        for key, val in d.items():
            child = Element(key)
            child.text = str(val)
            elem.append(child)
        return tostring(elem)
