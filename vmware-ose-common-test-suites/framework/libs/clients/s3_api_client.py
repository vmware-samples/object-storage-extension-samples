import boto3
import botocore


class S3APIClient(object):
    '''
    auth_info{source, type, username, password, tenant, token, app_id, api_key}
    type=basic: user, password, tenant
    type=token: token
    type=api_key: app_id, api_key
    '''
    def __init__(self,
                 endpoint,
                 auth_info,
                 verify=False,
                 retries=0,
                 region=None,
                 other_configs=None):
        if isinstance(other_configs, dict):
            config = botocore.config.Config(
                retries=dict(
                    max_attempts=retries
                ),
                **other_configs
            )
        else:
            config = botocore.config.Config(
                retries=dict(
                    max_attempts=retries
                )
            )
        key = self.gen_key(auth_info)
        access_key = auth_info.get('access_key', key)
        secret_key = auth_info.get('secret_key', key)
        self.__client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
            region_name=region,
            verify=verify,
            config=config
        )

    @property
    def client(self):
        return self.__client

    @staticmethod
    def gen_key(auth_info):
        if isinstance(auth_info, dict):
            auth_type = auth_info.get('type', 'basic')
            auth_source = auth_info.get('source', 'API_KEY' if auth_type == 'api_key' else 'VCD')
            if auth_type == 'basic':
                key = "%s/%s@%s:%s" % (auth_source, auth_info['username'], auth_info['tenant'], auth_info['password'])
            elif auth_type == 'token':
                key = "%s/%s" % (auth_source, auth_info['token'])
            elif auth_type == 'api_key':
                key = "%s/%s %s" % (auth_source, auth_info['app_id'], auth_info['api_key'])
            else:
                raise Exception("Auth type %s not supported!" % auth_type)
        else:
            raise Exception("Wrong auth_info: %s" % auth_info)
        return key
