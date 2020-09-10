from framework.libs.clients.oss_api_client import OssAPIClient


class BaseOSSAPI:
    def __init__(self, login_util, oss_host):
        self.oss_api_client = OssAPIClient(login_status=True, login_util=login_util)
        token_header = {login_util.key: login_util.token}
        self.oss_api_client.headers.update(token_header)

        self.url = oss_host
        self.variables = {}

    def restore(self):
        self.oss_api_client.restore()
        # self.variables = {}

    '''
    tenant_id
    type_name
    
    user_name
    
    class_id
    
    
    '''
