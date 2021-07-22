# -*- coding:utf-8 -*-

from framework.addons.UtiHTMLTestRunner import HTMLTestRunner
import os
import time
import re
import json
import requests
from framework.addons.Logger import TestLog
import framework.libs.common.globalvar as gl
from framework.libs.common.globalvar import GlobalKeys
from framework.libs.common.utils import remove_test_buckets
from tools.utils import send_email

current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))


def mylauncher(*case_suite, report_name=current_time, report_title="API_Test", test_build="API_test", timeout=3600):
    print('<----- Test Step: Case Run ----->')
    current_path = os.getcwd()
    if not os.path.exists(current_path + "/report"):
        os.system("mkdir report")

    report_file = open(current_path + "/report/" + report_name + ".html", 'wb')
    my_runner = HTMLTestRunner(stream=report_file, title=report_title, description='Test build is: ' + str(test_build))

    if not case_suite:
        res = None
        my_test_result = 'No suite to run'
        timeout = False
    else:
        res, _, timeout = my_runner.run_stage(*case_suite, timeout=timeout, pool_size=0)
        my_test_result = str(res)

    print('<----- Test Step: Test Data Clean Up ----->')
    ose_profile_configs = gl.get_value(GlobalKeys.OSE_PROFILE_ARGS.value)
    remove_test_buckets(ose_profile_configs)

    report_file.close()

    my_test_log = TestLog().getlog()

    if ose_profile_configs.get('email'):
        print('<----- Test Step: Upload test report and email ----->')
        try:
            send_email(report_name + '.html', current_path, ose_profile_configs)
        except KeyError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    if timeout:
        my_test_log.error("API test timeout")
        my_test_log.error(my_test_result)
        raise Exception("API test timeout")
    else:
        if "errors=0 failures=0" in my_test_result:
            my_test_log.info("API test pass")
            my_test_log.info(my_test_result)
        else:
            my_test_log.error("API test failed")
            my_test_log.error(my_test_result)
            raise Exception("API test failed")

