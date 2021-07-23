import botocore
import json
import sure
import datetimerange
import datetime
import re
import random
import string
import hashlib
import base64
import os
import pathlib
import urllib
from termcolor import colored
from dateutil import parser

import framework.libs.common.globalvar as gl
from framework.libs.common.globalvar import GlobalKeys

from framework.libs.clients.s3_api_client import S3APIClient
# from framework.libs.s3api import BuckMgrS3API
# from framework.libs.s3api import ObjectMgrS3API
# from libs.oss_core.ossapi.bucket_management import BuckMgrAPI


# def process_s3_resources(base, process_type="Precondition"):
#     '''
#     deprecated
#     '''
#     resources_to_process = parse_str_to_dict(base, base.testdata.get(process_type))
#
#     if isinstance(resources_to_process, dict):
#         for role, operations in resources_to_process.items():
#             auth_info = gen_auth_info(base, role, 'basic', {})
#             if 'bucket' in operations:
#                 bkt_mgr_s3_api = BuckMgrS3API(base.get_oss_url(), auth_info, verify=base.get_ssl_cert())
#                 bkt_mgr_api = BuckMgrAPI(login_util=base.basic_login(role=role), oss_host=base.get_oss_url())
#                 if 's3_add' in operations['bucket']:
#                     for bkt_to_add in operations['bucket']['s3_add']:
#                         try:
#                             actual_response = bkt_mgr_s3_api.add_bucket(**bkt_to_add)
#                         except botocore.exceptions.ClientError as e:
#                             actual_response = e.response
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                             [201, 409])
#                 if 'add' in operations['bucket']:
#                     for bkt_to_add in operations['bucket']['add']:
#                         bucket_name = bkt_to_add['Bucket']
#                         actual_response = bkt_mgr_api.add_bucket("{\"name\": \"%s\"}" % bucket_name)
#                         actual_response.should.have.property("status_code").within([201, 409])
#                 if 's3_delete' in operations['bucket']:
#                     for bkt_to_delete in operations['bucket']['s3_delete']:
#                         try:
#                             actual_response = bkt_mgr_s3_api.delete_bucket(**bkt_to_delete)
#                         except botocore.exceptions.ClientError as e:
#                             actual_response = e.response
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                             [204, 404])
#                 if 'delete' in operations['bucket']:
#                     for bkt_to_delete in operations['bucket']['delete']:
#                         bucket_name = bkt_to_delete['Bucket']
#                         actual_response = bkt_mgr_api.delete_bucket(bucket_name)
#                         actual_response.should.have.property("status_code").within([204, 404])
#                 if 's3_put_acl' in operations['bucket']:
#                     for acl_to_put in operations['bucket']['s3_put_acl']:
#                         try:
#                             actual_response = bkt_mgr_s3_api.put_bucket_acl(**acl_to_put)
#                         except botocore.exceptions.ClientError as e:
#                             actual_response = e.response
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').equal(200)
#
#             if 'object' in operations:
#                 obj_mgr_s3_api = ObjectMgrS3API(base.get_oss_url(), auth_info, verify=base.get_ssl_cert())
#                 if 's3_add' in operations['object']:
#                     for obj_to_add in operations['object']['s3_add']:
#                         body = obj_to_add.get('Body')
#                         if isinstance(body, dict):
#                             content = body.get('content')
#                             filename = body.get('filename')
#                             filepath = generate_tmp_file(filename, content)
#                             with open(filepath, 'r') as fr:
#                                 try:
#                                     obj_to_add_updated = {i: obj_to_add[i] for i in obj_to_add if i != 'Body'}
#                                     actual_response = obj_mgr_s3_api.add_object(Body=fr, **obj_to_add_updated)
#                                     obj_to_add['md5'] = calculate_md5(content)
#                                 except botocore.exceptions.ClientError as e:
#                                     actual_response = e.response
#                         elif isinstance(body, str):
#                             try:
#                                 actual_response = obj_mgr_s3_api.add_object(**obj_to_add)
#                                 obj_to_add['md5'] = calculate_md5(body)
#                             except botocore.exceptions.ClientError as e:
#                                 actual_response = e.response
#                         else:
#                             raise Exception("Such body not supported: %s" % body)
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                             [201, 409])
#                 if 's3_delete' in operations['object']:
#                     for obj_to_delete in operations['object']['s3_delete']:
#                         try:
#                             actual_response = obj_mgr_s3_api.delete_object(**obj_to_delete)
#                         except botocore.exceptions.ClientError as e:
#                             actual_response = e.response
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                             [204, 404])
#                 if 's3_put_acl' in operations['object']:
#                     for acl_to_put in operations['object']['s3_put_acl']:
#                         try:
#                             actual_response = obj_mgr_s3_api.put_object_acl(**acl_to_put)
#                         except botocore.exceptions.ClientError as e:
#                             actual_response = e.response
#                         actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').equal(200)
#     return resources_to_process
#
#
# def process_s3_resources_v2(base, process_type="Precondition"):
#     '''
#     deprecated
#     '''
#     '''
#     {"r1": [{"action": "s3_add_bucket", "parameters": {"Bucket": "abc"}},
#             {"action": "s3_add_object", "parameters": {"Bucket": "abc", "Key": "a.txt", "Body": "test"}}], "r2": []}
#     '''
#     resources = parse_str_to_dict(base, base.testdata.get(process_type))
#     if isinstance(resources, dict):
#         for role, operations in resources.items():
#             auth_info = gen_auth_info(base, role, 'basic', {})
#             bkt_mgr_s3_api = BuckMgrS3API(base.get_oss_url(), auth_info, verify=base.get_ssl_cert())
#             bkt_mgr_api = BuckMgrAPI(login_util=base.basic_login(role=role), oss_host=base.get_oss_url())
#             obj_mgr_s3_api = ObjectMgrS3API(base.get_oss_url(), auth_info, verify=base.get_ssl_cert())
#             for operation in operations:
#                 action = operation.get('action')
#                 parameters = operation.get('parameters')
#                 if action == 's3_add_bucket':
#                     try:
#                         actual_response = bkt_mgr_s3_api.add_bucket(**parameters)
#                     except botocore.exceptions.ClientError as e:
#                         actual_response = e.response
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                         [200, 409])
#                 elif action == 's3_delete_bucket':
#                     try:
#                         actual_response = bkt_mgr_s3_api.force_delete_bucket(**parameters)
#                     except botocore.exceptions.ClientError as e:
#                         actual_response = e.response
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                         [204, 404])
#                 elif action == 's3_empty_bucket':
#                     bkt_mgr_s3_api.empty_bucket(**parameters)
#                 elif action == 's3_put_bucket_acl':
#                     try:
#                         actual_response = bkt_mgr_s3_api.put_bucket_acl(**parameters)
#                     except botocore.exceptions.ClientError as e:
#                         actual_response = e.response
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').equal(200)
#                 elif action == 'add_bucket':
#                     actual_response = bkt_mgr_api.add_bucket(json.dumps(parameters))
#                     actual_response.should.have.property("status_code").within([201, 409])
#                 elif action == 's3_add_object':
#                     actual_response = s3_add_object_with_body(obj_mgr_s3_api, parameters)
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                         [200, 409])
#                 elif action == 's3_delete_object':
#                     try:
#                         actual_response = obj_mgr_s3_api.delete_object(**parameters)
#                     except botocore.exceptions.ClientError as e:
#                         actual_response = e.response
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').within(
#                         [204, 404])
#                 elif action == 's3_put_object_acl':
#                     try:
#                         actual_response = obj_mgr_s3_api.put_object_acl(**parameters)
#                     except botocore.exceptions.ClientError as e:
#                         actual_response = e.response
#                     actual_response.should.have.key("ResponseMetadata").have.key('HTTPStatusCode').equal(200)
#     return resources
#     # return process_resources(base, resources)


# def s3_validate_response(self, actual_response, expected_status_code,
#                          expected_header, expected_body,
#                          body_validation_schema=None, excluded_keys=None):
#     if expected_status_code:
#         pass
#     if expected_header:
#         pass
#     if expected_body:
#         pass
#
#     return True


def s3_add_object_with_body(object_client, parameters):
    body = parameters.get('Body')
    if isinstance(body, dict):
        content = body.get('content')
        filename = body.get('filename')
        filepath = generate_tmp_file(filename, content)
        with open(filepath, 'r') as fr:
            try:
                parameters_updated = {i: parameters[i] for i in parameters if i != 'Body'}
                actual_response = object_client.add_object(Body=fr, **parameters_updated)
                parameters['md5'] = calculate_md5(content)
            except botocore.exceptions.ClientError as e:
                actual_response = e.response
    elif isinstance(body, str):
        try:
            actual_response = object_client.add_object(**parameters)
            parameters['md5'] = calculate_md5(body)
        except botocore.exceptions.ClientError as e:
            actual_response = e.response
    else:
        raise Exception("Such body not supported: %s" % body)
    return actual_response


def gen_auth_info(base, role=None, auth_type=None, auth_settings=None):
    '''
    deprecated
    '''
    role = base.testdata.setdefault("Role") if role is None else role
    auth_type = base.testdata.get("AuthType") if auth_type is None else auth_type
    auth_settings = base.testdata.get("AuthSettings") if auth_settings is None else auth_settings
    if not isinstance(auth_settings, dict):
        auth_settings = parse_str_to_dict(base, auth_settings, default_when_failure={})

    auth_info = dict(type=auth_type)
    api_key_type = auth_settings.get('api_key_type', {} if auth_type == 'api_key' else None)
    if isinstance(api_key_type, dict):
        api_key_permissions_str = api_key_buckets_str = 'all'
        api_key_permissions = api_key_type.get('permission')
        if isinstance(api_key_permissions, list):
            api_key_permissions_str = "__".join(api_key_permissions)
        api_key_buckets = api_key_type.get('accessible_buckets')
        if isinstance(api_key_buckets, list):
            api_key_buckets_str = "__".join(api_key_buckets)
        api_key_type = "%s:%s" % (api_key_permissions_str, api_key_buckets_str)
    auth_info.update(base.get_user_info(role, api_key_type, auth_type == 'token'))

    invalid_credentials = auth_settings.get('invalid_credentials')
    if isinstance(invalid_credentials, dict):
        for field in ['access_key', 'secret_key']:
            if invalid_credentials.get(field) == 'swapcase':
                invalid_credentials[field] = S3APIClient.gen_key(auth_info).swapcase()
            elif invalid_credentials.get(field) == 'leading_trailing_space':
                invalid_credentials[field] = "  %s  " % S3APIClient.gen_key(auth_info)
            elif invalid_credentials.get(field) == 'leading_space':
                invalid_credentials[field] = "  %s" % S3APIClient.gen_key(auth_info)
            elif invalid_credentials.get(field) == 'trailing_space':
                invalid_credentials[field] = "%s  " % S3APIClient.gen_key(auth_info)
        for field in ['source', 'username', 'password', 'tenant', 'token', 'api_key', 'app_id']:
            if invalid_credentials.get(field) == 'swapcase':
                invalid_credentials[field] = auth_info[field].swapcase()
            elif invalid_credentials.get(field) == 'leading_trailing_space':
                invalid_credentials[field] = "  %s  " % auth_info[field]
            elif invalid_credentials.get(field) == 'leading_space':
                invalid_credentials[field] = "  %s" % auth_info[field]
            elif invalid_credentials.get(field) == 'trailing_space':
                invalid_credentials[field] = "%s  " % auth_info[field]
        if invalid_credentials.get('token') == 'expired_token':
            pass  # TODO: get an expired token from pre-provision
        if invalid_credentials.get('api_key') == 'revoked_api_key':
            pass  # TODO: get a revoked api_key from pre-provision
        elif invalid_credentials.get('api_key') == 'expired_api_key':
            pass  # TODO: get an expired api_key from pre-provision
        auth_info.update(invalid_credentials)
    return auth_info


ISO8601_REGEX = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9])[:]{0,1}[0-5][0-9])?$'


def validate(actual, expected, dict_match='full', list_match='include', validation_schema=None):
    '''
    dict_match: equal, full, partial
    list_match: equal, unordered_equal, include, type_check-include, check_for_all
    validation_schema:
        expected - {'Buckets':[{'Name':'abc','CreationDate':datetime.datetime},{'Name':'efg','CreationDate':datetime.datetime}...]}
        {
            "properties": {
                "Buckets": {
                    "items": {
                        "schema": {
                            "match": "full"
                        }
                    },
                    "schema": {
                        "match": "include",
                        "excludes": [{"Name":"exclude_name"}],
                        "order": {
                            "key": lambda var: var.get('Name'),
                            "reverse": True
                        }
                    }
                },
                "Owner": {
                    "schema": {
                        "match": "full"
                    }
                }
            },
            "schema": {
                "match": "partial",
                "excludes": ["nonexistent_key"]
            }
        }
    '''

    type_validation_fail_msg = 'Type validation fail'
    if isinstance(expected, type):
        with sure.ensure("{0}, actual: {1}, expected: {2}", type_validation_fail_msg, type(actual), expected):
            if expected == datetime.datetime and isinstance(actual, str):
                # with sure.ensure('{0} should be a valid iso8601 timestamp', actual):
                #     actual.should.match(ISO8601_REGEX)
                parser.parse(actual).should.be.a(expected)
            else:
                actual.should.be.a(expected)
    elif isinstance(expected, range):
        with sure.ensure("{0}, actual: {1}, expected: int", type_validation_fail_msg, actual):
            actual.should.be.a(int)
        (actual).should.be.within(expected)
    elif isinstance(expected, datetimerange.DateTimeRange):
        with sure.ensure("{0}, actual: {1}, expected: datetime", type_validation_fail_msg, actual):
            actual.should.be.a((datetime.datetime, str))
            if isinstance(actual, str):
                # with sure.ensure('{0} should be a valid iso8601 timestamp', actual):
                #     actual.should.match(ISO8601_REGEX)
                actual = parser.parse(actual)
        if os.environ.get('WORK_AROUND') != 'enabled':
            with sure.ensure('{0} should be in {1}', actual, expected):
                (actual in expected).should.be.ok
    elif isinstance(expected, type(re.compile(""))):  # re.Pattern
        with sure.ensure("{0}, actual: {1}, expected: str", type_validation_fail_msg, actual):
            actual.should.be.a((str, bytes))
        if isinstance(actual, bytes):
            actual.decode().should.match(expected)
        else:
            actual.should.match(expected)
    elif isinstance(expected, tuple):
        types = tuple(set([type(i) for i in expected]))
        with sure.ensure("{0}, actual: {1}, expected: {2}", type_validation_fail_msg, actual, types):
            actual.should.be.a(types)
        (actual).should.be.within(expected)
    elif isinstance(actual, botocore.response.StreamingBody):
        actual_value = actual.read()
        if isinstance(actual_value, bytes):
            actual_value = actual_value.decode("utf-8")
        actual_value.should.be.equal(expected)

    elif isinstance(expected, str):
        if isinstance(actual, bytes):
            actual.decode("utf-8").should.be.equal(expected)
        elif isinstance(actual, dict):
            str(actual).should.match(expected, re.I)
        elif isinstance(actual, str):
            actual.should.be.equal(expected)
        # else:
        #     raise AssertionError("%s has No such match: %s" % (str(actual), expected))
    else:
        with sure.ensure("{0}, actual: {1}, expected: {2}", type_validation_fail_msg, actual, type(expected)):
            actual.should.be.a(type(expected))
        if isinstance(expected, dict):
            match = excludes = properties = None
            if isinstance(validation_schema, dict):
                schema = validation_schema.get('schema')
                properties = validation_schema.get('properties')
                if isinstance(schema, dict):
                    match = schema.get('match')
                    excludes = schema.get('excludes')
            if isinstance(excludes, list):
                for item in excludes:
                    actual.shouldnt.have.key(item)
            if (match or dict_match) == 'equal':
                actual.should.be.equal(expected)
            else:
                if (match or dict_match) in ('full', 'partial'):
                    if (match or dict_match) == 'full':
                        sorted(actual.keys()).should.be.equal(sorted(expected.keys()))
                    for key, value in expected.items():
                        actual.should.have.key(key)
                        validate(actual[key], value, dict_match, list_match, (properties or {}).get(key))
                else:
                    raise AssertionError("No such dict_match: %s" % dict_match)
        elif isinstance(expected, list):
            match = excludes = order = items = sort = count = None
            if isinstance(validation_schema, dict):
                schema = validation_schema.get('schema')
                items = validation_schema.get('items')
                if isinstance(schema, dict):
                    match = schema.get('match')
                    excludes = schema.get('excludes')
                    order = schema.get('order')
                    sort = schema.get('sort')
                    count = schema.get('count')
            if count is not None:
                if isinstance(count, range):
                    len(actual).should.be.within(count)
                elif isinstance(count, int):
                    len(actual).should.be.equal(count)
            if isinstance(order, dict):
                key = order.get('key')
                reverse = order.get('reverse', False)
                comp = order.get('comp', None)
                with sure.ensure('{0} should be ordered (reverse: {1})', actual, reverse):
                    sorted_actual = sorted(actual, key=key, reverse=reverse)
                    print("sorted list:",sorted_actual)
                    if comp is None:
                        sorted_actual.should.be.equal(actual)
                    else:
                        [comp(ele) for ele in sorted_actual].should.be.equal([comp(ele) for ele in actual])
            if isinstance(excludes, list):
                for item in excludes:
                    unexpected_found = False
                    for item_a in actual:
                        try:
                            validate(item_a, item, "partial", list_match, items)
                            unexpected_found = True
                            break
                        except AssertionError:
                            pass
                    with sure.ensure('{0} should not contain {1}', actual, item):
                        unexpected_found.shouldnt.be.ok
            if (match or list_match) in ('equal', 'unordered_equal'):
                actual.should.have.length_of(len(expected))
                if (match or list_match) == 'equal':
                    for item_a, item_e in zip(actual, expected):
                        validate(item_a, item_e, dict_match, list_match, items)
                else:
                    for item_e in expected:
                        expected_found = False
                        for item_a in actual:
                            try:
                                validate(item_a, item_e, dict_match, list_match, items)
                                expected_found = True
                                break
                            except AssertionError as e:
                                pass
                        with sure.ensure('{0} should contain {1}', actual, item_e):
                            expected_found.should.be.ok

                    for item_a in actual:
                        actual_found = False
                        for item_e in expected:
                            try:
                                validate(item_a, item_e, dict_match, list_match, items)
                                actual_found = True
                                break
                            except AssertionError as e:
                                pass
                        with sure.ensure('{0} should contain {1}', expected, item_a):
                            actual_found.should.be.ok

                    # all(i in actual for i in expected).should.be.ok
                    # all(i in expected for i in actual).should.be.ok
            elif (match or list_match) in ('include', 'type_check-include', 'check_for_all'):
                if (match or list_match) == 'check_for_all' and actual == []:
                    pass
                else:
                    for item in expected:
                        expected_found = False
                        for item_a in actual:
                            try:
                                validate(item_a, item, dict_match, list_match, items)
                                expected_found = True
                                if (match or list_match) == 'include':
                                    break
                            except AssertionError as e:
                                if (match or list_match) == 'type_check-include' and type_validation_fail_msg in str(e):
                                    raise e from None
                                elif (match or list_match) == 'check_for_all':
                                    raise e from None
                        with sure.ensure('{0} should contain {1}', actual, item):
                            expected_found.should.be.ok
            else:
                raise AssertionError("No such list_match: %s" % list_match)
        else:
            if os.environ.get('WORK_AROUND') == 'enabled' and isinstance(actual, str) and actual.startswith('@@'):
                #  vip enabled
                actual = actual.strip('@')
            actual.should.be.equal(expected)


def get_res_code(self, res_code=None):
    # 200#204
    res = []
    for item in res_code.split('#'):
        res.append(int(item))
    return res


def ansi_pass(msg):
    return colored(msg, color="green", attrs=["bold"])


def ansi_fail(msg):
    return colored(msg, color="red", attrs=["bold"])


def ansi_title(msg):
    return colored(msg, on_color="on_cyan", attrs=["bold"])


def ansi_info(msg):
    return colored(msg, attrs=["bold"])


def ansi_description(msg):
    return colored(msg, attrs=["underline"])


def random_bucket_name():
    bkt_prefix = gl.get_value(GlobalKeys.OSE_PROFILE_ARGS.value)[
        'test_bucket_prefix']
    import time
    ts = time.time()
    dt = time.strftime("%d%H%M%S", time.localtime(int(ts)))
    return '{0}{1}{2}'.format(bkt_prefix, str(dt), str(ts)[-5:]).replace('.-', '')


def timestamp(time=datetime.datetime.utcnow(), format="%Y-%m-%dT%H-%M-%S.%fZ"):

    return time.strftime(format)


def random_string(length=1024, acceptable_string=string.ascii_letters + string.digits):
    if isinstance(length, range):
        length = random.randrange(length.start, length.stop, length.step)
    elif isinstance(length, int):
        pass
    else:
        length = 1024

    return ''.join(random.choice(acceptable_string) for i in range(length))


def unicode_chars():
    unicode_ranges = [
        # (0x0021, 0x0021),
        # (0x0023, 0x0026),
        # (0x0028, 0x007E),
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
        (0x0100, 0x017F),
        (0x0180, 0x024F),
        (0x2C60, 0x2C7F),
        (0x16A0, 0x16F0),
        (0x0370, 0x0377),
        (0x037A, 0x037E),
        (0x0384, 0x038A),
        (0x038C, 0x038C),
        (0x4e00, 0x62ff)
    ]
    return convert_to_chars(unicode_ranges)


def latin_1_chars():
    latin_1_ranges = [
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
    ]
    return convert_to_chars(latin_1_ranges)


def convert_to_chars(ranges):
    chars = [
        chr(code_point) for current_range in ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return chars


def calculate_md5(str_to_cal):
    if isinstance(str_to_cal, str):
        str_to_cal = str_to_cal.encode('utf-8')
    return hashlib.md5(str_to_cal).hexdigest()


def calculate_content_md5(body_str):
    if isinstance(body_str, str):
        hash_md5 = hashlib.md5(body_str.encode()).digest()
        base64_md5 = base64.b64encode(hash_md5).decode('ascii')
    return base64_md5


def generate_sse_c_key(original_key=None, key=None):
    if original_key is None:
        original_key = random_string(128)
    if isinstance(original_key, str):
        original_key = original_key.encode('utf-8')
    if isinstance(key, str):
        key = key.encode('utf-8')
    key = key or hashlib.sha256(original_key).digest()
    key_b64 = base64.b64encode(key).decode('utf-8')
    key_md5 = base64.b64encode(hashlib.md5(key).digest()).decode('utf-8')
    return {"key": key, "key_b64": key_b64, "key_md5": key_md5}


def url_encoded(str_to_encode):
    # return requote_uri(str_to_encode)
    return urllib.parse.quote_plus(str_to_encode)


def generate_tmp_file(filename, content=None, filedir=None):
    content = random_string() if content is None else content
    filedir = os.path.join(os.getcwd(), 'tmp') if filedir is None else filedir
    pathlib.Path(filedir).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(filedir, filename)
    with open(filepath, 'w') as fw:
        fw.write(content)
    return filepath


def validate_response(actual_response,
                      expected_response_code,
                      expected_response_header=None,
                      expected_response_header_schema=None,
                      expected_response_body=None,
                      expected_response_body_schema=None,
                      check_amz_id=False,
                      logger=None):

    try:
        # 1. extract actual response code/header/body
        if isinstance(actual_response, dict):
            actual_response.should.have.key("ResponseMetadata").have.key("HTTPStatusCode")
            actual_response_metadata = actual_response["ResponseMetadata"]
            actual_response_code = actual_response_metadata["HTTPStatusCode"]

            actual_response_metadata.should.have.key("HTTPHeaders")
            actual_response_header = actual_response_metadata["HTTPHeaders"]

            actual_response_body = actual_response['ResponseBody'] if 'ResponseBody' in actual_response \
                else {i: actual_response[i] for i in actual_response if i != 'ResponseMetadata'}
            if check_amz_id:
                actual_response_header.should.have.key('x-amz-request-id').be.a(str)
                actual_response_metadata.should.have.key('RequestId').be.equals(
                    actual_response_header['x-amz-request-id'])
                if 'x-amz-id-2' in actual_response_header:
                    actual_response_header['x-amz-id-2'].should.be.a(str)
                    actual_response_metadata.should.have.key('HostId').be.equals(
                        actual_response_header['x-amz-id-2'])
                else:
                    actual_response_metadata.should.have.key('HostId').be.a(str)
            if actual_response_body == {}:
                actual_response_body = ''
        else:
            actual_response.should.have.property("status_code")
            actual_response_code = actual_response.status_code

            actual_response.should.have.property("headers")
            actual_response_header = actual_response.headers

            actual_response.should.have.property("text")
            try:
                actual_response_body = actual_response.json()
            except json.decoder.JSONDecodeError:
                actual_response_body = actual_response.text
    except AssertionError as e:
        if logger:
            logger.error(ansi_fail("Response isn't as expected:"))
            logger.error(ansi_fail("- actual: %s" % actual_response))
            logger.error(ansi_fail("- expected:\n-- code: %s" % expected_response_code))
            if isinstance(expected_response_header, dict):
                logger.error(ansi_fail("-- header: %s" % expected_response_header))
            if isinstance(expected_response_header_schema, dict):
                logger.error(ansi_fail("-- header schema: %s" % expected_response_header_schema))
            if expected_response_body is not None:
                logger.error(ansi_fail("-- body: %s" % expected_response_body))
            if isinstance(expected_response_body_schema, dict):
                logger.error(ansi_fail("-- body schema: %s" % expected_response_body_schema))
            logger.error(ansi_fail("- details: %s" % e))
        raise e from None

    try:
        # 2. validate the response code
        if isinstance(expected_response_code, int):
            actual_response_code.should.be.equals(expected_response_code)
        elif isinstance(expected_response_code, list) and expected_response_code:
            actual_response_code.should.be.within(expected_response_code)
        else:
            if logger:
                logger.warn("Ignore response code validation, because cannot parse %s" % expected_response_code)
                logger.info(ansi_pass("Response code is as expected:"))
                logger.debug(ansi_pass("- actual code: %s" % actual_response_code))
                logger.debug(ansi_pass("- expected code: %s" % expected_response_code))
            print("Ignore response code validation, because cannot parse %s" % expected_response_code)

    except AssertionError as e:
        if logger:
            logger.error(ansi_fail("Response code isn't as expected:"))
            logger.error(ansi_fail("- actual: %s" % actual_response_code))
            logger.error(ansi_fail("- expected: %s" % expected_response_code))
            logger.error(ansi_fail("- details: %s" % e))
        raise e from None

    # 3. validate the response header
    if isinstance(expected_response_header, dict):
        # # TODO: add workaround here to skip the "x-amz-storage-class" header
        # # currently STANDARD storage profile does NOT need this header
        # #
        # # TODO: Method to get all the os.environ
        # if os.environ.get('WORK_AROUND') == 'enabled':  n
        #     self.logger.warn('Workaround: Pop x-amz-storage-class header')
        #     actual_response_header.pop('x-amz-storage-class', None)
        #     expected_response_header.pop('x-amz-storage-class', None)

        try:
            validate(actual_response_header, expected_response_header,
                     dict_match='partial',
                     validation_schema=expected_response_header_schema)
            if logger:
                logger.info(ansi_pass("Response header is as expected:"))
                logger.debug(ansi_pass("- actual: %s" % actual_response_header))
                logger.debug(ansi_pass("- expected: %s" % expected_response_header))
                if expected_response_header_schema:
                    logger.debug(ansi_pass("- expected schema: %s" % expected_response_header_schema))
        except AssertionError as e:
            if logger:
                logger.error(ansi_fail("Response header isn't as expected:"))
                logger.error(ansi_fail("- actual: %s" % actual_response_header))
                logger.error(ansi_fail("- expected: %s" % expected_response_header))
                if expected_response_header_schema:
                    logger.error(ansi_fail("- expected schema: %s" % expected_response_header_schema))
                logger.error(ansi_fail("- details: %s" % e))
            raise e from None  # TODO uncomment before merge!!!
    else:
        # ignore all non-dict expected header
        pass
    # 4. validate the response body
    if expected_response_body:
        try:
            # expected_response_body = update_expected_response_body(expected_response_body)

            validate(actual_response_body, expected_response_body,
                     dict_match='partial', list_match='equal',
                     validation_schema=expected_response_body_schema)
            if logger:
                logger.info(ansi_pass("Response body is as expected:"))
                logger.debug(ansi_pass("- actual body: %s" % actual_response_body))
                logger.debug(ansi_pass("- expected body: %s" % expected_response_body))
                if expected_response_body_schema:
                        logger.debug(ansi_pass("- expected schema: %s" % expected_response_body_schema))
        except AssertionError as e:
            if logger:
                logger.error(ansi_fail("Response body isn't as expected:"))
                logger.error(ansi_fail("- actual: %s" % actual_response_body))
                logger.error(ansi_fail("- expected: %s" % expected_response_body))
                if expected_response_body_schema:
                    logger.error(ansi_fail("- expected schema: %s" % expected_response_body_schema))
                logger.error(ansi_fail("- details: %s" % e))
            raise e from None  # TODO uncomment before merge!!!
    else:
        # ignore all None expected body ('' means empty body, None means no need to check body)
        pass

    return True


if __name__ == '__main__':
    pass
