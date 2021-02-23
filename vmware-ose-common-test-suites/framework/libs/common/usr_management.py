
import urllib.parse as parse

from framework.libs.clients.base_oss import BaseOSSAPI


class UsrMgmt(BaseOSSAPI):

    def __init__(self, login_util, oss_host):
        super(UsrMgmt, self).__init__(login_util, oss_host)
        pass

    def get_current_user(self):
        url = self.url + '/current-user'

        try:

            r = self.oss_api_client.do_get(req_url=url).json()
            self.variables.update({'tenant_id': r['tenant']['id'],
                                   'tenant_name': r['tenant']['name'],
                                   'role': r['role'],
                                   'user_id': r['id'],
                                   'user_name': r['name']})

            return True
        except KeyError as e:
            print('Exception happens ... %s' % e)
            return False

    def get_user_credentials(self):
        url = self.url + '/tenants/' + self.variables.get('tenant_id') + \
              '/users/' + self.variables.get('user_name') + '/credentials'
        try:
            r = self.oss_api_client.do_get(req_url=url).json()
            for item in r['items']:
                if item['immutable']:
                    self.variables.update({'access_key': item['accessKey'],
                                           'secret_key': item['secretKey']})
                    break
            return True
        except KeyError as e:
            print('Exception happens ... %s' % e)
            return False

    def get_canonical_id(self):
        url = self.url + '/tenants/' + self.variables.get('tenant_id') + \
              '/users/' + self.variables.get('user_name') + '/canonical-id'
        try:
            code = self.oss_api_client.do_get(req_url=url).status_code
            if 200 != code:
                return False
            r = self.oss_api_client.do_get(req_url=url).text

            self.variables.update({'canonical_id': r})
            return True

        except KeyError as e:
            print('Exception happens ... %s' % e)
            return False


if __name__ == "__main__":
    pass
