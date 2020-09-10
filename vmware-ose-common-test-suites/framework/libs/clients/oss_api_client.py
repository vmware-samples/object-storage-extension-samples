from requests import Request, Session
import json
import urllib.parse as parse
# from framework.addons.Logger import TestLog


def refresh_token(origin_func):
    def wrapper(self, *args, **kwargs):
        # logger = TestLog().getlog()

        r = origin_func(self, *args, **kwargs)

        if hasattr(self.login_util, 'TestScenario'):
            # logger.debug("This is a test scenario, would not retry.")
            return

        if self.login_status and r.status_code == 401 and\
                r.json().get('code') == 'VCLOUD_TOKEN_AUTH_ERROR' and\
                not hasattr(self.login_util, 'TestScenario'):
            # "TestScenario", "TestInvalidCredential")
            # logger.debug("Re-fresh Token")
            self.login_util.get_token()
            self.headers[self.login_util.key] = self.login_util.token
            r = origin_func(self, *args, **kwargs)
        return r
    return wrapper


class OssAPIClient:
    def __init__(self, oss_host=None, login_util=None, login_status=False):
        self.s = Session()
        self.s.verify = False
        # self.login_status is used in wrapper to update token if token expired
        #
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.login_status = login_status
        self.login_util = login_util

        self.url = oss_host if oss_host else ''

        if not self.login_status:
            if self.login_util:
                self.headers.update({login_util.key: login_util.token})
                self.login_status = True

    def restore(self):
        # Restore headers if previous case updates the 'Content-Type' or 'Accept'
        #
        self.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def remove_auth(self):
        if 'x-vcloud-authorization' in self.headers:
            del(self.headers['x-vcloud-authorization'])

    def __basic_req(self, method=None, req_url=None, req_header=None, files=None,
                    req_data=None, query_params=None, auth=None):
        # logger = TestLog().getlog()

        if query_params:
            if not isinstance(query_params, dict):
                raise Exception('Query supposed to be dict type.')
        if req_data:
            # if not isinstance(req_data, dict):
            #     raise Exception('Payload supposed to be dict type')
            if isinstance(req_data, dict):
                req_data = json.dumps(req_data)
        if files:
            if not isinstance(files, dict):
                raise Exception('Files supposed to be dict type')
        # if hasattr(self, 'login_util'):
        #     if hasattr(self.login_util, 'usr'):
                # logger.debug("user: " + self.login_util.usr)
        # logger.info("method: " + method)
        # logger.info("request_url: " + req_url)
        # logger.info("req_header: " + str(req_header))
        # logger.info("auth: " + str(auth))
        # logger.info("req_data: " + str(req_data))
        # logger.info("query_params: " + str(query_params))
        # logger.info("files: " + str(files))
        import urllib3
        urllib3.disable_warnings()

        req = Request(method, req_url, data=req_data, headers=req_header, auth=auth, params=query_params, files=files)
        prepped = req.prepare()
        return self.s.send(prepped, timeout=60)  #

    # self, method = None, req_url = None, req_header = None, files = None, req_data = None,
    # query_params = None, auth = None

    @refresh_token
    def do_get(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="GET",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    @refresh_token
    def do_head(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="HEAD",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    @refresh_token
    def do_post(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="POST",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    @refresh_token
    def do_put(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="PUT",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    @refresh_token
    def do_patch(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="PATCH",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    @refresh_token
    def do_delete(self, req_url=None, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        if req_header:
            self.headers.update(req_header)
        return self.__basic_req(
            method="DELETE",
            req_url=req_url,
            files=files,
            req_header=self.headers,
            auth=auth,
            query_params=query_params,
            req_data=req_data)


if __name__ == '__main__':
    usr = "oss-man-ta1@ossman1"
    pwd = "vmware"
    url = "https://oss-vcd-site2.eng.vmware.com/api/sessions"
    oss_host = "https://10.110.124.123/"

    from framework.libs.common.login_util import LoginUtil
    login_util = LoginUtil(url=url, usr=usr, pwd=pwd)
    login_util.get_token()
    # print(login_util.token)
    # print(login_util.user_id)
    # login_util.get_token(token_type='jwt')
    # print(login_util.auth_headers)
    # print(login_util.user_id)


    # login_util = LoginUtil(url, TA_usr, TA_pwd)
    # login_util = LoginUtil(url, PA_usr, PA_pwd)
    # login_util.get_token()
    oss_api_client = OssAPIClient(oss_host=oss_host, login_util=login_util)

    print(oss_api_client.get_current_user())

    '''
    
    headers = {'x-vcloud-authorization': 'rachelw@acme:vmware'}
    client = OssAPIClient()
    client.headers = {}
    client.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    client.headers.update(headers)

    oss_base = "https://10.110.126.113:8443/api/v1"
    bkt_n = "rachel.bkt.test001"

    print('---> verify GET with query<---')
    url = '{0}/buckets'.format(oss_base)
    query = {'limit': 10, 'offset': 4}
    r = client.do_get(req_url=url, query_params=query)
    print(r.json()['limit'])
    print(r.json()['offset'])

    print('---> verify POST with bucket<---')
    url = '{0}/buckets'.format(oss_base)

    bkt_payload = {"name": bkt_n}
    r = client.do_post(req_url=url, req_data=bkt_payload)
    print(r.status_code)
    print(r.text)

    print('---> verify PUT with bucket<---')
    url = '{0}/buckets/'.format(oss_base) + bkt_n
    bkt_payload = {
                   "customMetadata": {
                       "k1": "v1", "k2": "v2"
                   }
                   }
    r = client.do_put(req_url=url, req_data=bkt_payload)
    print(r.status_code)
    print(r.text)

    print('---> verify POST object into bucket<---')
    url = '{0}/buckets/{1}/objects'.format(oss_base, bkt_n)
    client.headers.pop('Content-Type')

    files = {'file': ('cat1.jpg', open('/Users/elvisy/Downloads/cat1.jpg', 'rb'))}
    r = client.do_post(req_url=url, files=files)
    print(r.status_code)
    print(r.text)

    print('---> verify DELETE object from bucket<---')
    url = '{0}/buckets/{1}/objects/{2}'.format(oss_base, bkt_n, 'cat1.jpg')
    client.headers.update({'Content-Type': 'application/json'})

    r = client.do_delete(req_url=url)
    print(r.status_code)
    print(r.text)

    print('---> verify DELETE with bucket<---')
    url = '{0}/buckets/'.format(oss_base) + bkt_n
    bkt_payload = {}
    r = client.do_delete(req_url=url, req_data=bkt_payload)
    print(r.status_code)
    print(r.text)
    
    '''
