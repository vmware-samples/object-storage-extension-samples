import os, re
from framework.libs.common.utils import read_yml
import framework.libs.common.globalvar as gl
from framework.libs.common.globalvar import GlobalKeys

from framework.libs.common.login_util import LoginUtil
from framework.libs.clients.oss_api_client import OssAPIClient
from framework.libs.common.usr_management import UsrMgmt


class CfgMgmt:

    @staticmethod
    def get_cfg_profile(global_v_args):
        # Step1:
        # support --file to load a customised user_profile.yml
        cfg_file_n = global_v_args.get('file') if global_v_args.get('file') else 'user_profile.yml'

        config_file_path = os.path.join(os.getcwd(), 'prj', cfg_file_n)
        config_profile = read_yml(config_file_path)

        # update args info
        config_profile = CfgMgmt.overwrite_config_profile_by_args(config_profile, global_v_args)

        CfgMgmt.validate_config(config_profile)

        config_profile = CfgMgmt.update_config_profile(config_profile)

        gl.set_value(GlobalKeys.OSE_PROFILE_ARGS.value, config_profile)

        return config_profile

    @staticmethod
    def overwrite_config_profile_by_args(config_profile, global_v_args):
        for k, v in global_v_args.items():
            if v:
                if k in ['vcd_user', 'vcd_password']:
                    config_profile.get('group1').get('user1').get('login_credential').update(
                        {k: v})
                else:
                    config_profile.update({k: v})
        return config_profile

    @staticmethod
    def validate_config(conf):
        ose_url = conf.get('ose_url')
        vcd_url = conf.get('vcd_url')
        http_regex = re.compile(r'^http[s]?://')
        if not http_regex.match(ose_url) or not http_regex.match(vcd_url):
            raise Exception('Invalid vcd url or ose url!')

    @staticmethod
    def update_config_profile(config_profile):
        config_profile.update({'vcd_url': config_profile.get('vcd_url').strip().strip('/') + '/api/sessions'})
        ose_admin_endpoint = config_profile.get('ose_url').strip().strip('/') + '/api/v1/core'
        config_profile.update({'ose_admin_endpoint': ose_admin_endpoint})
        if config_profile.get('virtual_host_style'):
            config_profile.update({'ose_url': config_profile.get('ose_url').strip().strip('/')})
        else:
            config_profile.update({'ose_url': config_profile.get('ose_url').strip().strip('/') + '/api/v1/s3'})

        config_profile.update({'ose_url': config_profile.get('ose_url').strip().strip('/')})
        print("<----- Test Step: Fetch test user' info. ----->")

        role_l = [{'group1': 'user1'}, {'group1': 'user2'}, {'group2': 'user1'}]
        for i in role_l:
            for group, user in i.items():
                print("******{0}******".format(config_profile[group][user]['login_credential']['vcd_user']))
                login_util = LoginUtil(config_profile.get('vcd_url'),
                                       config_profile[group][user]['login_credential']['vcd_user'],
                                       config_profile[group][user]['login_credential']['vcd_password'])
                login_util.get_token()
                usr_mgmt = UsrMgmt(login_util, config_profile.get('ose_admin_endpoint'))

                if usr_mgmt.get_current_user():
                    # update main user's group info;
                    # update main user's info, including user id

                    config_profile.get(group).update({
                        'group_id': usr_mgmt.variables.get('tenant_id'),
                        'group_name': usr_mgmt.variables.get('tenant_name')})
                    config_profile.get(group).get(user).update({
                        'user_id': usr_mgmt.variables.get('user_id'),
                        'user_name': usr_mgmt.variables.get('user_name'),
                        'role': usr_mgmt.variables.get('role')})
                else:
                    print("Failed to retrieve user's user info")
                    if (group, user) == ('group1', 'user1'):
                        raise Exception("Fails to retrieve the main test user ({0}@{1})'s info."
                                        .format(user, group))
                    continue

                print('Step-a:{0}Retrieve key pair...'.format('\n  '))
                if usr_mgmt.get_user_credentials():
                    # update access_key and secret_key
                    config_profile.get(group).get(user).update({
                        'main_credential': {'access_key': usr_mgmt.variables.get('access_key'),
                                            'secret_key': usr_mgmt.variables.get('secret_key')}})
                    print("{0}Successfully get the user credential, Key: {1}."
                          .format('  ', usr_mgmt.variables.get('access_key')))
                else:
                    print("Failed to retrieve user's credential pair.")
                    if (group, user) == ('group1', 'user1'):
                        raise Exception("Fails to retrieve the main test user ({0}@{1})'s info."
                                        .format(user, group))

                print('Step-b:{0}Retrieve user canonical id...'.format('\n  '))
                if usr_mgmt.get_canonical_id():
                    config_profile.get(group).get(user).update(
                        {'canonical_id': usr_mgmt.variables.get('canonical_id')})
                    print("{0}Successfully get the user canonical ID: {1}. "
                          .format('  ', usr_mgmt.variables.get('canonical_id')))
                else:
                    print("Failed to retrieve user's canonical ID.")

        return config_profile


if __name__ == '__main__':
    pass
