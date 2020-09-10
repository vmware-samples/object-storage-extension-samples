# from libs.clients.oss_api_client import OssAPIClient
from framework.libs.clients.s3_api_client import S3APIClient
import botocore


class BuckMgrS3API(object):
    def __init__(self, oss_host, auth_info, **params):
        endpoint = "%sapi/v1/s3/" % oss_host
        self.__s3_api_client = S3APIClient(endpoint, auth_info, **params).client
        pass

    @property
    def s3_api_client(self):
        return self.__s3_api_client

    def get_buckets(self):
        """
        :return: Buckets{CreateDate,Name}, Owner{DisplayName,ID}
        """
        return self.s3_api_client.list_buckets()

    def head_bucket(self, **req_data):
        """
        :param Bucket
        :return:
        """
        return self.s3_api_client.head_bucket(**req_data)

    def add_bucket(self, **req_data):
        """
        :param Bucket, ACL
        :return:
        """
        return self.s3_api_client.create_bucket(**req_data)

    def delete_bucket(self, **req_data):
        """
        :param Bucket
        :return:
        """
        return self.s3_api_client.delete_bucket(**req_data)

    def get_bucket(self, **req_data):
        """
        :param Bucket, Delimiter, EncodingType, MaxKeys, Prefix
        :return: CommonPrefixes[{Prefix}], Contents[{Key, LastModified, Owner{DisplayName, ID}, Size, StorageClass}],
        ContinuationToken, Delimiter, IsTruncated, KeyCount, MaxKeys, Name, NextContinuationToken, Preifx, Encoding-Type
        """
        return self.s3_api_client.list_objects_v2(**req_data)  # list-type=2

    def get_bucket_deprecated(self, **req_data):
        """
        :param Bucket, ContinuationToken, Delimiter, EncodingType, FetchOwner, MaxKeys, Prefix
        :return: CommonPrefixes[{Prefix}], Contents[{Key, LastModified, Owner{DisplayName, ID}, Size, StorageClass}],
        ContinuationToken, Delimiter, IsTruncated, KeyCount, MaxKeys, Name, NextContinuationToken, Preifx
        """
        return self.s3_api_client.list_objects(**req_data)

    def get_bucket_acl(self, **req_data):
        """
        :param Bucket
        :return: Grants[{Grantee{DisplayName, ID, Type}, Permission}], Owner{DisplayName, ID}
        """
        return self.s3_api_client.get_bucket_acl(**req_data)

    def put_bucket_acl(self, **req_data):
        """
        :param Bucket, AccessControlPolicy{Grants[{Grantee{DisplayName, ID, Type}, Permission}], Owner{DisplayName, ID}}
        :return:
        """
        return self.s3_api_client.put_bucket_acl(**req_data)

    def empty_bucket(self, **req_data):
        try:
            list_objects_actual_response = self.get_bucket(**req_data)
        except botocore.exceptions.ClientError as e:
            list_objects_actual_response = e.response
        list_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
            [200, 404])
        contents = list_objects_actual_response.get("Contents")
        if list_objects_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200 and isinstance(contents, list):
            all_keys_to_delete = list(map(lambda x: {'Key': x['Key']}, contents))
            total_keys = len(all_keys_to_delete)
            end = 0
            step = 1000
            while total_keys > end:
                start = end
                end = end + step if total_keys - end > step else total_keys
                try:
                    delete_objects_actual_response = self.s3_api_client.delete_objects(
                        Delete={"Objects": all_keys_to_delete[start:end]}, **req_data)
                except botocore.exceptions.ClientError as e:
                    delete_objects_actual_response = e.response
                delete_objects_actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
                    [200, 404])
                if delete_objects_actual_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    delete_objects_actual_response.shouldnt.have.key('Error')
            return delete_objects_actual_response
        else:
            return list_objects_actual_response

    def force_delete_bucket(self, **req_data):
        former_response = self.empty_bucket(**req_data)
        if former_response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            return former_response
        else:
            return self.delete_bucket(**req_data)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')

    authn = {
        'username': 'elsay',
        'password': 'vmware',
        'tenant': 'oss-qe'
    }
    buck_mgr = BuckMgrS3API('https://10.110.126.113:8443', authn)
    response = buck_mgr.get_buckets()

    import pprint
    pprint.pprint(response)
    pass

