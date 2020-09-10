from framework.addons.TestLauncher import mylauncher

from framework.libs.common.suite_management import SuiteManagement
from framework.libs.common.argument_mgmt import ArgMgmt
from framework.libs.common.cfg_management import CfgMgmt
from framework.libs.common.test_environment_mgmt import TestEnvMgmt

from framework.libs.common.utils import get_test_report_title

ose_args = ArgMgmt.add_argument()
config_profile = CfgMgmt.get_cfg_profile(ose_args)

sui_mgmt = SuiteManagement(config_profile)
parallel_suites = sui_mgmt.get_parallel_suites()

test_env = TestEnvMgmt()
test_env.env_init()


# define your test launcher
report_title = get_test_report_title()
mylauncher(*parallel_suites, report_name=report_title,
           report_title=report_title, timeout=72000)

test_env.env_teardown()

