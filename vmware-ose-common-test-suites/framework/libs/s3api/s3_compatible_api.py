import boto3
import requests
import xmltodict
import xml
import urllib
import os
import threading
import time
import hmac
import hashlib
import datetime
import io
from botocore.handlers import *
from framework.libs.common.s3_utils import random_string, calculate_md5

DEFAULT_BOTO_S3_MODEL_API_VERSION = 'custom-xml'  # 2006-03-01
DEFAULT_PART_SIZE = DEFAULT_MULTIPART_THRESHOLD = 1024*1024*5
DEFAULT_EXPIRATION = 3600

# def log_http_response(**kwargs):
#     http_response = kwargs.get('http_response',{})
#     request_url = http_response['url']
#     request_method = http_response['raw']['_original_response']['_method']
#     response_code = http_response['status_code']
#     print("%s %s %s" % (request_method, request_url, response_code))


class S3CompatibleAPI(object):
    def __init__(self, **params):
        # default not to verify SSL certificates
        if 'verify' not in params:
            params['verify'] = False

        if 'api_version' not in params:
            params['api_version'] = DEFAULT_BOTO_S3_MODEL_API_VERSION

        # default not to retry failures, use s3v4 signature version, won't validate request parameter
        default_config = botocore.config.Config(retries=dict(max_attempts=0),
                                                signature_version=os.environ.get('SIGN', 's3v4'),
                                                parameter_validation=False)
        config = params.get('config', None)
        if isinstance(config, botocore.config.Config):
            params['config'] = default_config.merge(config)
        elif isinstance(config, dict):
            # if 'signature_version' in config and config['signature_version'] == 's3v4':
            #     config['signature_version'] = os.environ.get('SIGN')
            params['config'] = default_config.merge(botocore.config.Config(**config))
        else:
            params['config'] = default_config

        self.__client = boto3.client('s3', **params)
        '''
        Unregister following handlers for testing purpose
        '''
        # remove the bucket name restriction to allow illegal bucket name
        self.client.meta.events.unregister('before-parameter-build.s3', validate_bucket_name)
        # not use 100-Continue as the default Expect when put/post object
        self.client.meta.events.unregister('before-call.s3', add_expect_header)
        # not use url encoding-type as default
        self.client.meta.events.unregister('before-parameter-build.s3.ListObjectsV2', set_list_objects_encoding_type_url)
        self.client.meta.events.unregister('before-parameter-build.s3.ListObjects', set_list_objects_encoding_type_url)
        # not to automatically parse the url encoded fields
        self.client.meta.events.unregister('after-call.s3.ListObjectsV2', decode_list_object_v2)
        self.client.meta.events.unregister('after-call.s3.ListObjects', decode_list_object)
        # not to automatically convert 200 error to 500 error
        self.client.meta.events.unregister('needs-retry.s3.CopyObject', check_for_200_error)
        # allow non ascii metadata
        self.client.meta.events.unregister('before-parameter-build.s3.PutObject', validate_ascii_metadata)
        self.client.meta.events.unregister('before-parameter-build.s3.CopyObject', validate_ascii_metadata)

        # self.client.meta.events.register('after-call.s3', log_http_response)

    @property
    def client(self):
        return self.__client

    def __getattr__(self, item):
        res = self.client.__getattribute__(item)
        return res

    def empty_bucket(self, **req_data):
        delete_objects_actual_response = None
        try:
            list_objects_versions_actual_response = self.list_object_versions(**req_data)
        except botocore.exceptions.ClientError as e:
            list_objects_versions_actual_response = e.response
        list_objects_versions_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
            [200, 404])
        while list_objects_versions_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            all_keys_to_delete = []
            if 'Versions' in list_objects_versions_actual_response and isinstance(
                    list_objects_versions_actual_response.get('Versions'), list):
                all_keys_to_delete += list(map(lambda x: {'Key': x['Key'], 'VersionId': x['VersionId']},
                                               list_objects_versions_actual_response.get('Versions')))

            if 'DeleteMarkers' in list_objects_versions_actual_response and isinstance(
                    list_objects_versions_actual_response.get('DeleteMarkers'), list):
                all_keys_to_delete += list(map(lambda x: {'Key': x['Key'], 'VersionId': x['VersionId']},
                                               list_objects_versions_actual_response.get('DeleteMarkers')))

            if not all_keys_to_delete:
                return list_objects_versions_actual_response

            try:
                delete_objects_actual_response = self.delete_objects(
                    Delete={"Objects": all_keys_to_delete}, **req_data)
            except botocore.exceptions.ClientError as e:
                delete_objects_actual_response = e.response
            delete_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                [200, 404])
            if delete_objects_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                delete_objects_actual_response.shouldnt.have.key('Error')

            try:
                list_objects_versions_actual_response = self.list_object_versions(**req_data)
                # list_objects_actual_response = self.list_objects_v2(**req_data)
            except botocore.exceptions.ClientError as e:
                list_objects_versions_actual_response = e.response
                list_objects_versions_actual_response.should.have.key("ResponseMetadata").have.key(
                    'HTTPStatusCode').within([200, 404])
            # contents = list_objects_versions_actual_response.get("Contents")
        return delete_objects_actual_response or list_objects_versions_actual_response

    def empty_bucket_degraded(self, **req_data):
        delete_objects_actual_response = None
        try:
            list_objects_actual_response = self.list_objects_v2(**req_data)
        except botocore.exceptions.ClientError as e:
            list_objects_actual_response = e.response
        list_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
            [200, 404])
        contents = list_objects_actual_response.get("Contents")
        while list_objects_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200 and isinstance(contents, list):
            truncated = list_objects_actual_response.get("IsTruncated")
            all_keys_to_delete = list(map(lambda x: {'Key': x['Key']}, contents))

            try:
                delete_objects_actual_response = self.delete_objects(
                    Delete={"Objects": all_keys_to_delete}, **req_data)
            except botocore.exceptions.ClientError as e:
                delete_objects_actual_response = e.response
            delete_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                [200, 404])
            if delete_objects_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                delete_objects_actual_response.shouldnt.have.key('Error')

            try:
                list_objects_actual_response = self.list_objects_v2(**req_data)
            except botocore.exceptions.ClientError as e:
                list_objects_actual_response = e.response
            list_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                [200, 404])
            contents = list_objects_actual_response.get("Contents")
        return delete_objects_actual_response or list_objects_actual_response

    def force_delete_bucket(self, **req_data):
        former_response = self.empty_bucket(**req_data)
        # if former_response["ResponseMetadata"]["HTTPStatusCode"] == 404:
        #     return former_response
        # else:
        return self.delete_bucket(**req_data)

    def empty_multipart_uploads(self, **req_data):
        abort_multipart_upload_actual_response = None
        try:
            list_multipart_uploads_actual_response = self.list_multipart_uploads(**req_data)
        except botocore.exceptions.ClientError as e:
            list_multipart_uploads_actual_response = e.response
        list_multipart_uploads_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
            [200, 404])
        uploads = list_multipart_uploads_actual_response.get("Uploads")
        while list_multipart_uploads_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200 and isinstance(uploads, list):
            for upload in uploads:
                try:
                    abort_multipart_upload_actual_response = self.abort_multipart_upload(Key=upload['Key'], UploadId=upload['UploadId'], **req_data)
                except botocore.exceptions.ClientError as e:
                    abort_multipart_upload_actual_response = e.response
                abort_multipart_upload_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                    [204, 404])

                try:
                    list_multipart_uploads_actual_response = self.list_multipart_uploads(**req_data)
                except botocore.exceptions.ClientError as e:
                    list_multipart_uploads_actual_response = e.response
                list_multipart_uploads_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                    [200, 404])
                uploads = list_multipart_uploads_actual_response.get("Uploads")
        return abort_multipart_upload_actual_response or list_multipart_uploads_actual_response

    def post_object(self, Bucket, Body, PolicyExipration=DEFAULT_EXPIRATION, **req_data):
        '''
        self.post_object(Bucket="test-post-object",Body="test",
            Conditions=[{"bucket": "test-post-object"}, ["starts-with", "$key", "testpost.txt"], ["starts-with", "$Content-Type", "text/"]],
            Payload=[("key" , "testpost.txt"), ("content-type" , "text/plain")])
        '''
        signature_version = self._client_config.signature_version
        if signature_version == 's3v4':
            datetime_now = datetime.datetime.utcnow()
            amzdate = datetime_now.strftime('%Y%m%dT%H%M%SZ')
            datestamp = datetime_now.strftime('%Y%m%d')
            aws_access_key_id = self._request_signer._credentials.access_key
            aws_secret_access_key = self._request_signer._credentials.secret_key
            if isinstance(PolicyExipration, int):
                policy_expiration = (datetime_now + datetime.timedelta(seconds=+PolicyExipration)).strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                policy_expiration = PolicyExipration
            region = self._client_config.region_name

            policy_dict = {"expiration": policy_expiration}
            conditions = req_data.get('Conditions', [])
            policy_dict['conditions'] = conditions
            conditions.append({"x-amz-credential": "%s/%s/%s/s3/aws4_request" % (aws_access_key_id, datestamp, region)})
            conditions.append({"x-amz-algorithm": 'AWS4-HMAC-SHA256'})
            conditions.append({"x-amz-date": amzdate})

            policy_json = json.dumps(policy_dict)
            print(policy_json)
            encoded_policy = base64.b64encode(policy_json.encode())

            def sign(key, msg):
                return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

            def get_signature_key(key, date_stamp, region_name):
                k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
                k_region = sign(k_date, region_name)
                k_service = sign(k_region, 's3')
                k_signing = sign(k_service, 'aws4_request')
                return k_signing

            signing_key = get_signature_key(aws_secret_access_key, datestamp, region)
            signature = hmac.new(signing_key, encoded_policy, hashlib.sha256).hexdigest()

            payload_tuples = req_data.get('Payload', [])
            payload_tuples.append(("x-amz-credential", "%s/%s/%s/s3/aws4_request" % (aws_access_key_id, datestamp, region)))
            payload_tuples.append(("x-amz-algorithm", 'AWS4-HMAC-SHA256'))
            payload_tuples.append(("x-amz-date", amzdate))
            payload_tuples.append(("policy", encoded_policy))
            payload_tuples.append(("X-Amz-Signature", signature))
            payload_tuples.append(('file', Body))
            print(payload_tuples)
            payload = OrderedDict(payload_tuples)

            url = "%s%s" % (self._endpoint.host, Bucket) if self._endpoint.host.endswith('/') else "%s/%s" % (self._endpoint.host, Bucket)
            r = requests.post(url, files=payload, verify=self._endpoint.http_session._verify)
            headers = dict(r.headers)
            for header_k, header_v in headers.items():
                headers[header_k.lower()] = urllib.parse.unquote(header_v)
                if header_k != header_k.lower():
                    del headers[header_k]

            boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": r.status_code, "HTTPHeaders": headers}}
            try:
                body = xmltodict.parse(r.text)
                postresponse = body.get("PostResponse")
                if isinstance(postresponse, OrderedDict):
                    body['PostResponse'] = dict(postresponse)
                error = body.get("Error")
                if isinstance(error, OrderedDict):
                    body['Error'] = dict(error)
                boto3_style_response.update(body)
            except xml.parsers.expat.ExpatError:
                body = r.text
                if body:
                    boto3_style_response["Body"] = body
            return boto3_style_response
        else:
            # TODO: s3, botocore.UNSIGNED
            pass

    def call_presigned_url(self, PresignedUrl, Method, **req_data):
        # TODO: custom header/parameter/body
        r = requests.request(Method, PresignedUrl,
                             headers=req_data.get('Headers', None),
                             data=req_data.get('Payload', None),
                             verify=self._endpoint.http_session._verify)
        headers = dict(r.headers)
        for header_k, header_v in headers.items():
            headers[header_k] = urllib.parse.unquote(header_v)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": r.status_code, "HTTPHeaders": headers}}
        try:
            body = xmltodict.parse(r.text)
            error = body.get("Error")
            if isinstance(error, OrderedDict):
                body['Error'] = dict(error)
            boto3_style_response.update(body)
        except xml.parsers.expat.ExpatError:
            body = r.text
            if body:
                boto3_style_response["Body"] = body
        return boto3_style_response

    def generate_presigned_url_as_boto3_style(self, **req_data):
        r = self.generate_presigned_url(**req_data)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": None}, "PresignedUrl": r}
        return boto3_style_response

    def call_presigned_post(self, PresignedUrl, **req_data):
        # TODO: custom header/parameter/body
        r = requests.post(PresignedUrl,
                          headers=req_data.get('Headers', None),
                          data=req_data.get('Payload', None),
                          verify=self._endpoint.http_session._verify)
        headers = dict(r.headers)
        for header_k, header_v in headers.items():
            headers[header_k] = urllib.parse.unquote(header_v)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": r.status_code, "HTTPHeaders": headers}}
        try:
            body = xmltodict.parse(r.text)
            error = body.get("Error")
            if isinstance(error, OrderedDict):
                body['Error'] = dict(error)
            boto3_style_response.update(body)
        except xml.parsers.expat.ExpatError:
            body = r.text
            if body:
                boto3_style_response["Body"] = body
        return boto3_style_response

    def options_object(self, Bucket, Key, Origin, AccessControlRequestMethod, AccessControlRequestHeaders=None):
        host = self._endpoint.host
        if host.endswith('/'):
            url = "%s%s/%s" % (host, Bucket, Key)
        else:
            url = "%s/%s/%s" % (host, Bucket, Key)
        headers = {"Origin": Origin, "Access-Control-Request-Method": AccessControlRequestMethod}
        if AccessControlRequestHeaders is not None:
            headers['Access-Control-Request-Headers'] = AccessControlRequestHeaders
        r = requests.options(url, headers=headers, verify=self._endpoint.http_session._verify)
        headers = dict(r.headers)
        for header_k, header_v in headers.items():
            headers[header_k] = urllib.parse.unquote(header_v)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": r.status_code, "HTTPHeaders": headers}}
        # boto3_style_response["ResponseMetadata"].setdefault("RequestId", headers.get("x-amz-request-id", ""))
        # boto3_style_response["ResponseMetadata"].setdefault("HostId", headers.get("x-amz-id-2", ""))
        try:
            body = xmltodict.parse(r.text)
            error = body.get("Error")
            if isinstance(error, OrderedDict):
                body['Error'] = dict(error)
            # if isinstance(error, dict):
            #     if error.get("RequestId") is not None:
            #         boto3_style_response["ResponseMetadata"]["RequestId"] = error["RequestId"]
            #         del error["RequestId"]
            #     if error.get("HostId") is not None:
            #         boto3_style_response["ResponseMetadata"]["HostId"] = error["HostId"]
            #         del error["HostId"]
            boto3_style_response.update(body)
        except xml.parsers.expat.ExpatError:
            body = r.text
            if body:
                boto3_style_response["Body"] = body
        return boto3_style_response

    def cors_request(self, Action, CORSHeaders, **req_data):
        def add_cors_headers(**kwargs):
            kwargs['params']['headers'].update(CORSHeaders)

        self.client.meta.events.register('before-call.s3', add_cors_headers)
        try:
            return getattr(self, Action)(**req_data)
        finally:
            self.client.meta.events.unregister('before-call.s3', add_cors_headers)

    def multipart_upload_file(self, Body=None, FilePath=None, PartSize=DEFAULT_PART_SIZE, Threshold=DEFAULT_MULTIPART_THRESHOLD, **req_data):
        default_config = boto3.s3.transfer.TransferConfig(multipart_chunksize=PartSize, multipart_threshold=Threshold)
        # default_config = boto3.s3.transfer.TransferConfig(multipart_chunksize=PartSize, multipart_threshold=Threshold,
        #                                                   max_concurrency=5, use_threads=True)
        config = req_data.get('Config', None)
        if isinstance(config, boto3.s3.transfer.TransferConfig):
            req_data['Config'] = default_config.merge(config)
        elif isinstance(config, dict):
            req_data['Config'] = default_config.merge(boto3.s3.transfer.TransferConfig(**config))
        else:
            req_data['Config'] = default_config
        if FilePath is not None:
            self.upload_file(FilePath, **req_data)
        else:
            if not isinstance(Body, (bytes, str)):
                Body = b''
            elif isinstance(Body, str):
                Body = bytes(Body, encoding="utf-8")
            with io.BytesIO(Body) as data:
                self.upload_fileobj(data, **req_data)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": None}}
        return boto3_style_response

    def multipart_copy_file(self, PartSize=DEFAULT_PART_SIZE, Threshold=DEFAULT_MULTIPART_THRESHOLD, **req_data):
        default_config = boto3.s3.transfer.TransferConfig(multipart_chunksize=PartSize, multipart_threshold=Threshold)
        config = req_data.get('Config', None)
        if isinstance(config, boto3.s3.transfer.TransferConfig):
            req_data['Config'] = default_config.merge(config)
        elif isinstance(config, dict):
            req_data['Config'] = default_config.merge(boto3.s3.transfer.TransferConfig(**config))
        else:
            req_data['Config'] = default_config
        self.copy(**req_data)
        boto3_style_response = {"ResponseMetadata": {"HTTPStatusCode": 200, "HTTPHeaders": None}}
        return boto3_style_response

    def put_multiple_objects(self, Bucket, Count=1, Size=1024,
                             Prefix=None, Suffix=None, Keys=None, Body=None,
                             Wait=None, BrokenOnFailure=True, Parallel=False, **kwargs):
        results = {}
        threads = []
        if not isinstance(Keys, list):
            Keys = []
        index = 0
        if Count > 0 and (isinstance(Prefix, str) or isinstance(Suffix, str)):
            while index < Count:
                if isinstance(Prefix, str) and isinstance(Suffix, str):
                    Keys.append("%s.%s.%s" % (Prefix, index, Suffix))
                elif isinstance(Prefix, str):
                    Keys.append("%s.%s" % (Prefix, index))
                elif isinstance(Suffix, str):
                    Keys.append("%s.%s" % (index, Suffix))
                index += 1
        if Parallel:
            def put_object_worker(bucket_name, object_name, object_body):
                try:
                    put_object_actual_response_parallel = self.put_object(Bucket=bucket_name, Key=object_name, Body=object_body, **kwargs)
                except botocore.exceptions.ClientError as e_parallel:
                    put_object_actual_response_parallel = e_parallel.response
                put_object_actual_response_parallel['request_body'] = object_body
                put_object_actual_response_parallel['request_body_etag'] = '"%s"' % calculate_md5(object_body)
                results[object_name] = put_object_actual_response_parallel

            for key in Keys:
                if Body is None:
                    body = random_string(Size)
                else:
                    body = Body
                threads.append(threading.Thread(target=put_object_worker, args=(Bucket, key, body)))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        else:
            for key in Keys:
                if Body is None:
                    body = random_string(Size)
                else:
                    body = Body
                if isinstance(Wait, int):
                    time.sleep(Wait)
                try:
                    put_object_actual_response = self.put_object(Bucket=Bucket, Key=key, Body=body, **kwargs)
                except botocore.exceptions.ClientError as e:
                    put_object_actual_response = e.response
                if BrokenOnFailure:
                    put_object_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                        [200])
                put_object_actual_response['request_body'] = body
                put_object_actual_response['request_body_size'] = len(body)
                put_object_actual_response['request_body_etag'] = '"%s"' % calculate_md5(body)
                results[key] = put_object_actual_response
        return results

    def create_multiple_buckets(self, Count=0,
                                Prefix=None, Suffix=None, Names=None,
                                BrokenOnFailure=True, Parallel=False, **kwargs):
        '''

        :param count:
        :param name_prefix:
        :param names:
        :param broken_on_failure: Only work when parallel = False
        :param parallel:
        :return:
        '''
        results = {}
        threads = []
        if not isinstance(Names, list):
            Names = []
        index = 0
        if Count > 0 and (isinstance(Prefix, str) or isinstance(Suffix, str)):
            while index < Count:
                if isinstance(Prefix, str) and isinstance(Suffix, str):
                    Names.append("%s.%s.%s" % (Prefix, index, Suffix))
                elif isinstance(Prefix, str):
                    Names.append("%s.%s" % (Prefix, index))
                elif isinstance(Suffix, str):
                    Names.append("%s.%s" % (index, Suffix))
                index += 1
        if Parallel:
            def create_bucket_worker(bucket_name):
                try:
                    create_bucket_actual_response_parallel = self.create_bucket(Bucket=bucket_name, **kwargs)
                except botocore.exceptions.ClientError as e_parallel:
                    create_bucket_actual_response_parallel = e_parallel.response
                results[bucket_name] = create_bucket_actual_response_parallel

            for name in Names:
                threads.append(threading.Thread(target=create_bucket_worker, args=(name,)))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        else:
            for name in Names:
                try:
                    create_bucket_actual_response = self.create_bucket(Bucket=name, **kwargs)
                except botocore.exceptions.ClientError as e:
                    create_bucket_actual_response = e.response
                if BrokenOnFailure:
                    create_bucket_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                        [200, 409])
                results[name] = create_bucket_actual_response
        return results


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')

    api_client = S3CompatibleAPI(
        endpoint_url="https://10.110.126.113:8443/api/v1/s3/",
        aws_access_key_id="72d20de769137509c3e9",
        aws_secret_access_key="Q7LGNmeb78+oka7FupqzAQGhDZ/0E2va8DO6fTfR",
        region_name='region-1'
    )
    # returns = api_client.put_multiple_objects(Count=2,
    #                                           Size=range(10, 1024),
    #                                           Bucket="test.create-buckets.0",
    #                                           Prefix="test",
    #                                           Keys=["test.key_a"],
    #                                           BrokenOnFailure=True,
    #                                           Parallel=True)
    # print(returns.keys())
    # returns = api_client.create_multiple_buckets(Count=100, Prefix="test.create-buckets")
    # print(returns.keys())
    for i in range(1,66):
        api_client.delete_bucket(Bucket="test.create-buckets.%s" % i)

    pass

