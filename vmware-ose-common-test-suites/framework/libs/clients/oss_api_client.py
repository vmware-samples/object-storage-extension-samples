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
    pass
