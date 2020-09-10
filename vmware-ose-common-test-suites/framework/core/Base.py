import unittest
import os, ssl
import pprint
from framework.libs.s3api.s3_compatible_api import S3CompatibleAPI
from framework.libs.common.s3_utils import *
from framework.libs.common.utils import *
import framework.libs.common.globalvar as gl
from framework.libs.common.globalvar import GlobalKeys
from framework.core.common.definitions import CSVColumns


class Base(unittest.TestCase):

    @classmethod
    def initialize(cls):
        cls.cfg_profile = gl.get_value(GlobalKeys.OSE_PROFILE_ARGS.value)
        cls.logger = get_logger(cls.cfg_profile.get('log_level'))

        cls.client_instances = {}
        cls.global_variables = {}  #

    def get_user_info(self, role='group1:user1'):
        _group = role.split(':')[0]
        _user = role.split(':')[1]
        if not self.cfg_profile.get(_group).get(_user).get('main_credential'):
            raise Exception(ansi_fail('{2}Failed to login: {0}@{1}'
                                      .format(_group, _user, '\n')))
        elif not self.cfg_profile.get(_group).get(_user).get('user_id'):
            raise Exception(ansi_fail("{2}Failed to retrieve {0}@{1}'s user id or user name"
                                      .format(_group, _user, '\n')))
        elif not self.cfg_profile.get(_group).get(_user).get('canonical_id'):
            raise Exception(ansi_fail("{2}Failed to retrieve {0}@{1}'s canonical ID"
                                      .format(_group, _user, "\n")))

        return self.cfg_profile.get(_group).get(_user)

    '''
    Currently only support boto3 or boto2 as aws client. 
    We might enhance use action mapping mechanism for different clients. < , >
    
    @ testdata:
    
    '''
    def generic_s3_test_process(self, testdata, client_type=None, action=None):
        try:
            # TODO: need to confirm self.testdata needed.
            self.testdata = testdata  # used in teardown

            self.generate_variables(testdata, CSVColumns.Variables.value)

            # TODO: Tools to generate the "Description"
            # from "case title" and "caseExecution" and "postValidation"
            self.logger.info(ansi_description("Test case:\n%s" % testdata.get(CSVColumns.Description.value)))

            # TODO: Test case type support?

            # TODO: Need to track the test case result "SKIP" based on platform capability

            # TODO: Case Result: PASS, FAIL, ERROR, PARTIAL_PASS (PostValidation fail?), SKIP

            self.logger.info(ansi_title('Step1: Case Precondition'))
            self.execute_generic_steps(testdata, CSVColumns.PreCondition.value)

            self.logger.info(ansi_title("Step2: Case Execution"))
            client_type = testdata.get(
                CSVColumns.ClientType.value) if testdata.get(CSVColumns.ClientType.value) else client_type
            if not client_type:
                client_type = 'S3CompatibleAPI'  # TODO: to be enhanced to support different clients

            client_instance = self.get_api_host_instance(
                usr_role=testdata.get(CSVColumns.Role.value),
                api_host=client_type,
                auth_settings=testdata.get(CSVColumns.AuthSettings.value))

            action = testdata.get(
                CSVColumns.Action.value) if testdata.get(CSVColumns.Action.value) else action

            method_parameters = self.parse_testdata_column_value_to_dict(
                testdata=testdata,
                testdata_key=CSVColumns.Parameter.value,
                default_when_failure={})

            self.logger.info(ansi_info(
                "Operator: %s (auth settings: %s)" % (testdata.get(CSVColumns.Role.value),
                                                      testdata.get(CSVColumns.AuthSettings.value))))

            actual_response = self.func_hook(client_instance, action, **method_parameters)

            if action in ['create_multipart_upload', 'put_object', 'list_object_versions']:
                self.global_variables.update(new_passdown_variables(actual_response, self.global_variables,
                                                                    self.variables, action,
                                                                    parameters=method_parameters))

            self.logger.info(ansi_title("Step3: Case Validation"))
            # self.generate_variables('ResponseVariables')
            # extract expected response code from csv
            expected_response_code = int(testdata.get(CSVColumns.ExpectResponseCode.value))

            # extract expected response header from csv
            expected_response_header = self.parse_testdata_column_value_to_dict(
                testdata=testdata,
                testdata_key=CSVColumns.ExpectResponseHeader.value,
                default_when_failure={})

            # expected_response_header_schema = self.parse_str_to_dict(testdata_key="ExpectResponseHeaderSchema")
            # extract expected response body from csv
            expected_response_body = self.parse_testdata_column_value_to_dict(
                testdata=testdata,
                testdata_key=CSVColumns.ExpectResponseBody.value,
                default_when_failure={})

            expected_response_body_schema = self.parse_testdata_column_value_to_dict(
                testdata=testdata,
                testdata_key=CSVColumns.ExpectResponseBodySchema.value,
                default_when_failure={})

            if self.cfg_profile.get('skip_body_validation'):
                expected_response_body = None

            validate_response(actual_response=actual_response,
                              expected_response_code=expected_response_code,
                              expected_response_header=expected_response_header,
                              expected_response_header_schema=None,
                              expected_response_body=expected_response_body,
                              expected_response_body_schema=expected_response_body_schema,
                              check_amz_id=False,
                              logger=self.logger)

            self.logger.info(ansi_title("Step4: Case Post Validation"))
            self.execute_generic_steps(testdata, CSVColumns.PostValidation.value)

        except Exception as e:
            self.logger.error(ansi_fail("Testcase failed:\n- case: %s\n- details: %s" % (self.id(), e)))
            raise e from None

    def func_hook(self, client_ins, action, **method_parameters):
        self.logger.info(ansi_info("%s %s request:" % (client_ins, action)))
        if action in ('put_object', 'multipart_upload_file', 'put_multiple_objects', 'upload_part'):
            # self.logger.info(ansi_info(pprint.pformat(
            #     {i: method_parameters[i] for i in method_parameters if
            #      not isinstance(method_parameters[i], str) or len(method_parameters[i]) <= 1024})))
            method_parameters_display = {}
            for i in method_parameters:
                if i != 'Body' or len(method_parameters[i]) <= 10:
                    method_parameters_display[i] = method_parameters[i]
                else:
                    method_parameters_display[i] = "%s..." % method_parameters[i][:10]
            self.logger.info(ansi_info(pprint.pformat(method_parameters_display)))
        else:
            self.logger.info(ansi_info(pprint.pformat(method_parameters)))

        if hasattr(client_ins, action):
            try:
                f_action = getattr(client_ins, action)
                r = f_action(**method_parameters)
            except botocore.exceptions.ClientError as e:
                self.logger.debug(e.response)
                r = e.response
            except Exception as e:
                self.logger.error(ansi_fail("%s response failed:\n%s" % (action, e)))
                raise e from None
            self.logger.info(ansi_info("%s %s response:" % (client_ins, action)))
            self.logger.info(ansi_info(pprint.pformat(r)))

            return r

        return None

    # Precondition; PostValidation; CleanUp
    def execute_generic_steps(self, testdata, execution_type):
        '''
        :param:
            steps:
                [(who, using what, do what, para_content), ...]

                [("vcd0:org1:tu1", "S3CompatibleAPI", "create_bucket", {"Bucket":"tu1.s3.create-bucket.default"}),
                ("vcd0:org1:tu1", "S3CompatibleAPI", "put_object", {"Bucket":"tu1.s3.create-bucket.default", "Key":"tu1.s3.default.txt", "Body": "test"})]
        :return:
        '''

        steps_exceptions = []
        steps = self.parse_testdata_column_value_to_dict(testdata=testdata,
                                                         testdata_key=execution_type,
                                                         ignore_failure=False,
                                                         default_when_failure=None)
        if isinstance(steps, list):
            step_idx = 1
            for step in steps:
                # We only support tuple currently, we need to skip the steps platform does NOT support
                #

                if isinstance(step, tuple):
                    role, client_type, action, parameters, *others = step

                    if isinstance(client_type, tuple):
                        auth_settings = client_type[1]
                        client_type = client_type[0]
                    else:
                        auth_settings = None
                    if role is None:
                        continue
                    # if isinstance(role, list) and not set(priority_list).intersection(set(role)):
                    #     continue
                    keys = ["expected_response_code",
                            "variables",
                            "expected_response_header",
                            "expected_response_header_schema",
                            "expected_response_body",
                            "expected_response_body_schema"]
                    step_cfg = dict(zip(keys, others))
                    variables = step_cfg.get('variables')

                    client_instance = self.get_api_host_instance(role, client_type)

                    if auth_settings is None:
                        self.logger.info(ansi_info("%s Step %s (%s):" % (execution_type, step_idx, role)))
                    else:
                        self.logger.info(ansi_info("%s Step %s (%s, %s):" % (execution_type, step_idx, role, auth_settings)))
                    self.logger.debug(ansi_info(step))
                    step_idx += 1

                    if execution_type == "PreCondition" and action in ('create_multiple_buckets', 'put_multiple_objects'):
                        parameters['BrokenOnFailure'] = False
                    actual_response = self.func_hook(client_instance, action, **parameters)

                    if execution_type == "PreCondition":
                        if action in ['create_multipart_upload', 'put_object', 'list_object_versions']:
                            self.global_variables.update(
                                new_passdown_variables(actual_response, self.global_variables,
                                                       self.variables, action, parameters))
                    # ignore non-dict variables
                    if isinstance(variables, dict) and variables:
                        # save variables from response for later use
                        # {"version-1": "header['x-amz-version-id']"}
                        # {"continuation_token": "body['NextContinuationToken']", "key-0":"body['Contents'][0]['Key']"}
                        header = body = None
                        try:
                            header = actual_response['ResponseMetadata']["HTTPHeaders"]
                        except Exception as e:
                            pass
                        try:
                            body = {i: actual_response[i] for i in actual_response if i != 'ResponseMetadata'}
                        except Exception as e:
                            pass
                        for var_k, var_v in variables.items():
                            try:
                                self.variables[var_k] = eval(var_v)
                            except Exception as e:
                                self.logger.warn(
                                    "Fail to parse %s: %s" % (var_v, e))
                        self.logger.debug(self.variables)

                    # TODO: do we support skip precondition check?
                    # if os.environ.get('SKIP_PRECONDITION_CHECK') == 'enabled' and execution_type == "Precondition":

                    if step_cfg.get('expected_response_code') or \
                            step_cfg.get('expected_response_header') or \
                            step_cfg.get('expected_response_body'):
                        if self.cfg_profile.get('skip_body_validation'):
                            step_cfg['expected_response_body'] = None
                        if execution_type.lower() == "cleanup":  # TODO: do we need to validate res in cleanUp?
                            try:
                                validate_response(actual_response,
                                                  step_cfg.get('expected_response_code'),
                                                  step_cfg.get('expected_response_header'),
                                                  step_cfg.get('expected_response_header_schema'),
                                                  step_cfg.get('expected_response_body'),
                                                  step_cfg.get('expected_response_body_schema'),
                                                  logger=self.logger)
                            except Exception as e:
                                self.logger.warn(e)
                                steps_exceptions.append({"step_idx": step_idx, "step": step, "exception": e})
                        else:
                            validate_response(actual_response,
                                              step_cfg.get('expected_response_code'),
                                              step_cfg.get('expected_response_header'),
                                              step_cfg.get('expected_response_header_schema'),
                                              step_cfg.get('expected_response_body'),
                                              step_cfg.get('expected_response_body_schema'),
                                              logger=self.logger)

                    pass
                else:
                    # ignore non-tuple step
                    pass
        else:
            # ignore non-list steps
            pass
        # if execution_type.lower() == "cleanup":  # print BugNeeded Info
        #     self.logger.info(parse_testdata_column_value_to_dict(testdata=testdata,
        #                                                          testdata_key=CSVColumns.Comment,
        #                                                          default_when_failure=''))
        #     steps_exceptions.should.be.empty

    def generate_variables(self, testdata, testdata_key):
        # {"random_bucket":random_string(10)}
        if not hasattr(self, 'variables'):
            self.variables = {}
        extra_variables = self.parse_testdata_column_value_to_dict(testdata=testdata,
                                                              testdata_key=testdata_key,
                                                              ignore_failure=False,
                                                              default_when_failure=None)
        self.variables.update(extra_variables)

        self.logger.info("Dump variables info -->")
        self.logger.info(self.variables)

    def parse_testdata_column_value_to_dict(self, testdata,
                                            testdata_key,
                                            ignore_failure=True,
                                            default_when_failure=None):
        str_to_parse = testdata.get(testdata_key) if isinstance(testdata_key, str) else ''
        return self.parse_str_to_dict(str_to_parse=str_to_parse,
                                      ignore_failure=ignore_failure,
                                      default_when_failure=default_when_failure)

    def parse_str_to_dict(self, str_to_parse,
                          ignore_failure=True,
                          default_when_failure=None):
        self.logger.debug('To parse str: %s' % str_to_parse)
        try:
            parsed_rslt = json.loads(str_to_parse)
        except (TypeError, json.decoder.JSONDecodeError):
            try:
                parsed_rslt = eval(str_to_parse)
            except Exception as e:
                if ignore_failure or str_to_parse == '' or str_to_parse is None:
                    parsed_rslt = str_to_parse if default_when_failure is None else default_when_failure

                    self.logger.warn("Fail to parse: %s with exception: %s \nUse default value instead:\n%s" % (str_to_parse, e, parsed_rslt))
                    return parsed_rslt
                else:
                    raise Exception("Fail to parse: %s with exception: %s" % (str_to_parse, e))
        return parsed_rslt

    def get_api_host_instance(self, usr_role='group1:user1', api_host='S3CompatibleAPI', auth_settings=None):
        # group1:user1
        new_k = usr_role + '@' + api_host
        if new_k in self.client_instances:
            return self.client_instances[new_k]

        _group = usr_role.split(':')[0]
        _user = usr_role.split(':')[1]

        if api_host in ['S3CompatibleAPI']:
            s3_api = get_boto_client(self.cfg_profile, group=_group, user=_user)

            self.client_instances[new_k] = s3_api
            self.logger.debug("Client info: %s" % new_k)
            return self.client_instances[new_k]

        else:
            pass

    def tearDown(self):
        self.logger.info(ansi_title("Step5: Case Cleanup"))
        self.execute_generic_steps(self.testdata, CSVColumns.CleanUp.value)


if __name__ == '__Main__':
    base = Base()
    base.initialize()

