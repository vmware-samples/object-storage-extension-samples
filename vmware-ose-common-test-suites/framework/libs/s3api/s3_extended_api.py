import xmltodict
import time
from botocore.handlers import *
from framework.libs.s3api.s3_compatible_api import S3CompatibleAPI


def parse_xml_body_to_json(model, params, **kwargs):
    json_body = parse_xml_to_json(params['body'])
    params['body'] = json_body


def parse_xml_to_json(str_to_parse):
    if isinstance(str_to_parse, (str, bytes)) and str_to_parse:
        try:
            xml_dict = xmltodict.parse(str_to_parse, xml_attribs=False)
            return json.dumps(xml_dict)
        except:
            return str_to_parse
    elif isinstance(str_to_parse, dict):
        return json.dumps(str_to_parse)
    else:
        return str_to_parse


CUSTOM_XML_BOTO_S3_MODEL_API_VERSION = 'custom-xml'
EXTENDED_JSON_BOTO_S3_MODEL_API_VERSION = 'extended-json'


class S3ExtendedAPI(S3CompatibleAPI):
    def __init__(self, auth_method='s3v4', refresh_token=True, **kw):
        self.auth_method = auth_method
        self.login_util = None
        if 'api_version' not in kw:
            kw['api_version'] = CUSTOM_XML_BOTO_S3_MODEL_API_VERSION
        if self.auth_method.startswith('s3'):
            kw.update({"config": {"signature_version": self.auth_method}})
            super().__init__(**kw)
        else:
            kw.update({"config": {"signature_version": botocore.UNSIGNED}})
            if 'login_util' in kw:
                self.login_util = kw.pop('login_util')
                super().__init__(**kw)

                def add_auth_headers(model, params, **kwargs):
                    if refresh_token:
                        self.login_util.get_token(token_type=self.auth_method, force_refresh=False)
                    params['headers'].update(self.login_util.auth_headers)

                self.client.meta.events.register('before-call.s3', add_auth_headers)
            else:
                super().__init__(**kw)

        # sd_xml = os.path.join(os.getcwd(), 'libs/oss_core/s3api/s3xml.json')
        # service_description = json.load(open(sd_xml))
        # model = botocore.model.ServiceModel(service_description)
        # self.client.meta._service_model = model
        '''
        Unregister following handlers for testing purpose
        '''
        # disable sse md5 key auto generation to test access object with only key or md5
        self.client.meta.events.unregister('before-parameter-build.s3.HeadObject', sse_md5)
        self.client.meta.events.unregister('before-parameter-build.s3.GetObject', sse_md5)
        self.client.meta.events.unregister('before-parameter-build.s3.PutObject', sse_md5)
        self.client.meta.events.unregister('before-parameter-build.s3.CopyObject', sse_md5)
        self.client.meta.events.unregister('before-parameter-build.s3.CopyObject', copy_source_sse_md5)

    # def __getattr__(self, item):
    #     orig_attr = self.client.__getattribute__(item)
    #     if callable(orig_attr):
    #         def hooked(*args, **kw):
    #             if "Extensions" in kw:
    #                 ext = kw.pop('Extensions')
    #
    #                 def inject_extensions(model, params, **kwargs):
    #                     if "headers" in ext:
    #                         # add extended header (overwrite if exists)
    #                         params['headers'].update(ext['headers'])
    #                     if "queries" in ext:
    #                         # add extended query (overwrite if exists)
    #                         params['query_string'].update(ext['queries'])
    #                         scheme, netloc, path, query_string, fragment = urlsplit(params['url'])
    #                         new_query_string = urlencode(params['query_string'])
    #                         params['url'] = urlunsplit((scheme, netloc, path, new_query_string, fragment))
    #                         # TODO: url parameter extended (Object Name)
    #                     if "body" in ext:
    #                         # replace the old body with the extended body
    #                         params['body'] = ext['body']
    #
    #                 self.client.meta.events.register('before-call.s3', inject_extensions)
    #                 try:
    #                     result = orig_attr(*args, **kw)
    #                 finally:
    #                     self.client.meta.events.unregister('before-call.s3', inject_extensions)
    #             else:
    #                 result = orig_attr(*args, **kw)
    #             return result
    #         return hooked
    #     else:
    #         return orig_attr


'''
custom handlers
'''


def add_accept_json_header(model, params, **kwargs):
    has_accept = False
    for header_k, header_v in params['headers'].items():
        if header_k.lower() == 'accept':
            has_accept = True
            if header_v == 'ignore':
                params['headers'].pop(header_k)
            break
    if not has_accept:
        params['headers']['Accept'] = 'application/json'


def add_content_type_json_header(model, params, **kwargs):
    has_accept = False
    for header_k, header_v in params['headers'].items():
        if header_k.lower() == 'content-type':
            has_accept = True
            if header_v == 'ignore':
                params['headers'].pop(header_k)
            break
    if not has_accept:
        params['headers']['Content-Type'] = 'application/json'


def inject_raw_body(**kwargs):
    try:
        kwargs['parsed_response']['ResponseBody'] = json.loads(kwargs['response_dict']['body'])
    except Exception as e:
        try:
            kwargs['parsed_response']['ResponseBody'] = kwargs['response_dict'].get('body')
        except:
            kwargs['parsed_response']['ResponseBody'] = "test"


class S3ExtendedJsonAPI(S3ExtendedAPI):
    def __init__(self, **kw):
        if 'api_version' not in kw:
            kw['api_version'] = EXTENDED_JSON_BOTO_S3_MODEL_API_VERSION

        super().__init__(**kw)

        # sd_json = os.path.join(os.getcwd(), 'libs/oss_core/s3api/s3json.json')
        # service_description = json.load(open(sd_json))
        # model = botocore.model.ServiceModel(service_description)
        # self.client.meta._service_model = model

        self.client.meta.events.register_last('before-call.s3.PutBucketAcl', add_content_type_json_header)
        self.client.meta.events.register_last('before-call.s3.PutObjectAcl', add_content_type_json_header)
        self.client.meta.events.register_last('before-call.s3.PutBucketTagging', add_content_type_json_header)
        self.client.meta.events.register_last('before-call.s3.PutObjectTagging', add_content_type_json_header)
        self.client.meta.events.register_last('before-call.s3', add_accept_json_header)
        # self.client.meta.events.register_last('before-call.s3', parse_xml_body_to_json)
        self.client.meta.events.register('response-received.s3', inject_raw_body)

    def empty_bucket(self, **req_data):
        try:
            actual_response = self.delete_objects(Delete=json.dumps({"removeAll": True}), **req_data)
        except botocore.exceptions.ClientError as e:
            actual_response = e.response

        return actual_response

    def force_delete_bucket(self, **req_data):
        former_response = self.empty_bucket(**req_data)
        time.sleep(5)
        if former_response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            return former_response
        else:
            return self.delete_bucket(**req_data)


if __name__ == "__main__":
    pass

