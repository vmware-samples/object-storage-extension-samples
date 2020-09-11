from requests import Request, Session
import json
import boto3
import botocore
from framework import TestLog


class CloudianVendorClient:
    def __init__(self):
        self.logger = TestLog().getlog()
        self.admin_session = self.s3_client = None
        self.req_url = self.login_user = self.login_pwd = ''
        # self.endpoint = self.s3_access_key = self.s3_secret_key = ''
        pass

    def set_admin_session(self, endpoint, login_user, login_pwd, verify=False):
        self.req_url = endpoint
        self.login_user = login_user
        self.login_pwd = login_pwd
        s = Session()
        s.verify = False
        if verify:
            s.verify = True
        self.admin_session = s

    def set_s3_session(self, endpoint, s3_access_key, s3_secret_key, region=None, verify=False):

        region = region if region else 'region1'
        verify = verify if verify else False
        retries = 0

        config = botocore.config.Config(
            retries=dict(
                max_attempts=retries
            )
        )

        self.s3_client = boto3.client(
            service_name='s3',
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            endpoint_url=endpoint,
            region_name=region,
            verify=verify,
            config=config
        )

#########################################################################################
#                                     Action methods                                    #
#########################################################################################
    def get_user_details(self, group_id, user_id, req_header=None):
        print('---> GET User Info<---')
        url = '{0}/user'.format(self.req_url)
        auth = (self.login_user, self.login_pwd)
        headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        if dict and isinstance(req_header, dict):
            headers.update(req_header)
        query = {'groupId': group_id, 'userId': user_id}
        r = self.do_get(s=self.admin_session, req_url=url, auth=auth, req_header=headers, query_params=query)
        self.logger.debug(r.text)
        self.logger.debug(r.status_code)
        try:
            '''
            data = r.json()
            json_str = json.dumps(data)
            return json.loads(json_str)
            '''
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            return None

        # eg for json: print(r.json()['canonicalUserId'])
#########################################################################################
#                                         End                                           #
#########################################################################################

    def __basic_req(self, s, method, req_url, req_header=None, files=None,
                    req_data=None, query_params=None, auth=None):
        if query_params:
            if not isinstance(query_params, dict):
                raise Exception('Query supposed to be dict type.')
        elif req_data:
            if not isinstance(req_data, dict):
                raise Exception('Payload supposed to be dict type')
            req_data = json.dumps(req_data)
        elif files:
            if not isinstance(files, dict):
                raise Exception('Files supposed to be dict type')
        elif req_header:
            if not isinstance(req_header, dict):
                raise Exception('Headers supposed to be dict type')
        elif auth:
            if not isinstance(auth, tuple):
                raise Exception('Auth supposed to be tuple type')

        req = Request(method, req_url, data=req_data, headers=req_header, auth=auth, params=query_params, files=files)
        prepped = req.prepare()
        return s.send(prepped, timeout=60)

    def do_get(self, s, req_url, files=None, req_data=None, query_params=None, auth=None, req_header=None):
        return self.__basic_req(
            s=s,
            method="GET",
            req_url=req_url,
            files=files,
            req_header=req_header,
            auth=auth,
            query_params=query_params,
            req_data=req_data)

    def print_s3_response(self, r):
        try:
            # 1. extract actual response code/header/body
            if isinstance(r, dict):
                print(r)
            else:
                print(r.status_code)
                print(r.headers)
                try:
                    body = r.json()
                except json.decoder.JSONDecodeError:
                    body = r.text
                print(body)
        except AssertionError as e:
            raise e from None


if __name__ == '__main__':
    pass


