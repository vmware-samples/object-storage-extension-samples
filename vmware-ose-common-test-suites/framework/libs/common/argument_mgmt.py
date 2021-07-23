import re, os
from enum import Enum
import argparse
import framework.libs.common.globalvar as gl
from framework.libs.common.globalvar import GlobalKeys
from framework.libs.common.utils import handle_ose_arguments


class ArgMgmt:
    @staticmethod
    def add_argument():
        # TODO: arguments
        parser = argparse.ArgumentParser()

        parser.add_argument('--priority', type=str, default='smoke',
                            choices=['smoke', 'regression', 'quick', 'full'],
                            help='Case priority')
        parser.add_argument('--scope', type=str, default='cloudian', choices=['full', 'ecs', 'cloudian'],
                            help='Case scope')

        parser.add_argument('--virtual-host-style', action='store_true',
                            default='False', help='Enable Virtual Hosting Style')

        parser.add_argument('--vcd-url', type=str, help='vcd url')
        parser.add_argument('--ose-url', type=str, help='ose url')
        parser.add_argument('--vcd-user', type=str, help='vcd username')
        parser.add_argument('--vcd-password', type=str, help='vcd user password')
        parser.add_argument('--file', type=str, help='user profile')

        parser.add_argument('--testcases', nargs='+', help='id(s) of testcase(s) to run',
                            required=False)

        # TODO: to be removed
        # support testing against vendor
        parser.add_argument('--log_level', type=str, default='info',
                            choices=['info', 'warn', 'debug', 'error'])
        parser.add_argument('--vendor', action='store_true',
                            default='False', help='Run against vendor endpoint')
        parser.add_argument('--skip_body_validation', action='store_true',
                            default='False', help='skip_body_validation')
        parser.add_argument('--email', action='store_true', default='False',
                            help='Email the test report')
        parser.add_argument('--email_receivers', nargs='+', help='Email receivers list')

        args = parser.parse_args()
        try:
            keys = ['priority', 'scope',
                    'virtual_host_style', 'ose_url', 'vcd_url',
                    'vcd_user', 'vcd_password', 'file', 'testcases', 'log_level',
                    'vendor', 'skip_body_validation', 'email', 'email_receivers']

            ose_args = ArgMgmt.handle_argument(keys, args)

            gl.init()
            gl.set_value(GlobalKeys.OSE_ARGS.value, ose_args)

            return ose_args
        except Exception:
            raise

    @staticmethod
    def handle_argument(keys, args):
        ose_args = dict()
        for arg in keys:
            arg_v = os.popen("echo $%s" % arg).read().strip('\n')

            if not arg_v:
                arg_v = getattr(args, arg) if hasattr(args, arg) else ''

            if arg in ['email',
                       'skip_body_validation',
                       'vendor', 'virtual_host_style'] and arg_v:
                if type(arg_v) == str:
                    arg_v = True if arg_v.lower() == 'true' else False

            else:
                if type(arg_v) == str:
                    arg_v = arg_v.lower()

            ose_args.update({arg: arg_v})

        ose_args = handle_ose_arguments(ose_args)

        return ose_args


if __name__ == '__main__':
    pass
