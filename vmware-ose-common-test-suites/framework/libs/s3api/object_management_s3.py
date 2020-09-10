from framework.libs.clients.s3_api_client import S3APIClient


class ObjectMgrS3API(object):
    def __init__(self, oss_host, auth_info, **params):
        endpoint = "%sapi/v1/s3/" % oss_host
        self.__s3_api_client = S3APIClient(endpoint, auth_info, **params).client
        pass

    @property
    def s3_api_client(self):
        return self.__s3_api_client

    def delete_objects(self, **req_data):
        """
        :param Bucket, Delete{Objects[{Key}]}
        :return: Deleted[{Key}]
        """
        return self.s3_api_client.delete_objects(**req_data)

    # def post_add_object(self, **req_data):

    def get_object(self, **req_data):
        """
        :param Bucket, Key, ResponseContentType
        :return: AcceptRanges, Body, CacheControl, ContentDisposition, ContentLength, ContentType, Expires, Metadata
        """
        return self.s3_api_client.get_object(**req_data)

    def head_object(self, **req_data):
        """
        :param Bucket, Key
        :return: CacheControl, ContentLength, Expires, Metadata
        """
        return self.s3_api_client.head_object(**req_data)

    def add_object(self, **req_data):
        """
        :param Bucket, Key, Body, ACL, ContentDisposition, ContentLength, ContentType, Metadata
        :return:
        """
        return self.s3_api_client.put_object(**req_data)

    def copy_object(self, **req_data):
        """
        :param Bucket, Key, CopySource, ACL, Metadata
        :return:
        """
        return self.s3_api_client.copy_object(**req_data)

    def delete_object(self, **req_data):
        """
        :param Bucket, Key
        :return:
        """
        return self.s3_api_client.delete_object(**req_data)

    def get_object_acl(self, **req_data):
        """
        :param Bucket, Key
        :return: Grants[{Grantee{DisplayName, ID, Type}, Permission}], Owner{DisplayName, ID}
        """
        return self.s3_api_client.get_object_acl(**req_data)

    def put_object_acl(self, **req_data):
        """
        :param Bucket, AccessControlPolicy{Grants[{Grantee{DisplayName, ID, Type}, Permission}], Owner{DisplayName, ID}}
        :return:
        """
        return self.s3_api_client.get_object_acl(**req_data)


if __name__ == "__main__":
    key = ''
    token = ''
    obj_mgr = ObjectMgrS3API(key, token)
    pass

