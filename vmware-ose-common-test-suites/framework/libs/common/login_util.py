from framework.libs.clients.oss_api_client import OssAPIClient

import jwt
import xmltodict
import datetime
# from framework.addons.Logger import TestLog


class LoginUtil:
    """
    get token: url, usr, pwd
    return token
    """
    def __init__(self, url, usr, pwd, access_type="vcd"):
        self.url = url
        self.usr = usr
        self.pwd = pwd
        self.token = ""  # keep it for backward compatible, recommended use auth_headers
        self.auth_headers = {}
        self.expires = None
        self.location_id = None
        self.org_id = None
        self.user_id = None

        if access_type == "vcd":
            self.headers = {'Accept': 'application/*;version=30.0'}
            self.key = "x-vcloud-authorization"
        else:  # vC
            self.headers = {'Accept': 'application/*;version=30.0'}
            self.key = "x-vcloud-authorization"

        # self.logger = TestLog().getlog()

    def get_token(self, token_type=None, force_refresh=True, site_name=None, org_name=None):
        if (not force_refresh) and isinstance(self.expires, datetime.datetime):
            if self.expires - datetime.datetime.now() > datetime.timedelta(seconds=60):
                # not expired, remain the same
                return

        oss_client = OssAPIClient()
        oss_client.headers = self.headers

        basic_auth = (self.usr, self.pwd)
        # payload = '{{"username": {0}, "password": {1}}}'.format(self.usr, self.pwd)
        r = oss_client.do_post(req_url=self.url, auth=basic_auth)
        # assert r.status_code == 200, 'Response code {0} does not equal to 200'.format(r.status_code)
        if r.status_code == 200:
            try:
                xml_dict = xmltodict.parse(r.content, xml_attribs=True)
                self.user_id = xml_dict['Session']['@userId'].split(':')[-1]
                if token_type == 'jwt':
                    # vcd, TODO: vC or other platform
                    jwt_token = r.headers['X-VMWARE-VCLOUD-ACCESS-TOKEN']
                    authrization = "%s %s" % (r.headers['X-VMWARE-VCLOUD-TOKEN-TYPE'], jwt_token)
                    locations = xml_dict["Session"]["AuthorizedLocations"]["Location"]
                    location = None
                    if isinstance(locations, list):
                        if not site_name and not org_name:
                            location = locations[0]
                        elif site_name and not org_name:
                            for loc in locations:
                                if site_name == loc['SiteName']:
                                    location = loc
                                    break
                        elif not site_name and org_name:
                            for loc in locations:
                                if org_name == loc['OrgName']:
                                    location = loc
                                    break
                        else:
                            for loc in locations:
                                if site_name == loc['SiteName'] and org_name == loc['OrgName']:
                                    location = loc
                                    break
                    else:
                        location = locations

                    self.location_id = location['LocationId']
                    self.org_id = self.location_id.split("@")[0]
                    auth_context = location["AuthContext"]
                    tenant_context = location["LocationId"].split("@")[0]
                    self.auth_headers = {"authorization": authrization,
                                         "x-vmware-vcloud-auth-context": auth_context,
                                         "x-vmware-vcloud-tenant-context": tenant_context}
                    try:
                        decoded_jwt = jwt.decode(jwt_token, verify=False)
                        self.expires = datetime.datetime.fromtimestamp(decoded_jwt.get('exp'))
                    except:
                        self.expires = datetime.datetime.now() + datetime.timedelta(seconds=600)
                else:
                    oss_token = r.headers[self.key]

                    # self.logger.info('Request succeeded with token: {0}'.format(oss_token))
                    self.token = oss_token
                    self.auth_headers = {"x-vcloud-authorization": oss_token}
                    self.expires = datetime.datetime.now() + datetime.timedelta(seconds=600)

            except (AttributeError, KeyError):
                # self.logger.error('Failed to extract token from response header')
                raise

        else:
            pass


if __name__ == '__main__':
    # url, usr, pwd, vcd=True
    url = "https://oss-vcd.eng.vmware.com/api/sessions"
    usr = "tuc@quc"
    pwd = "vmware"
    login_util = LoginUtil(url=url, usr=usr, pwd=pwd)
    login_util.get_token()
    print(login_util.token)
    print(login_util.user_id)
    login_util.get_token(token_type='jwt')
    print(login_util.auth_headers)
    print(login_util.user_id)
