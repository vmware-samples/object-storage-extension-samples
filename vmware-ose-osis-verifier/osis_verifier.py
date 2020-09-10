from __future__ import print_function

import collections
import inspect
import logging
import sys
import time
import uuid
from pprint import pprint

import namegenerator
import pyfiglet
import terminal_banner
import urllib3
from six.moves.urllib.parse import urlparse
from termcolor import colored

import openapi_client
from aws_client import AwsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
print(pyfiglet.figlet_format('OSIS Verifier'))

Choice = collections.namedtuple('Choice', ['description', 'callable'])


class OsisVerifier:
    
    def __init__(self, prompt):
        self.prompt = prompt
        self.configuration = openapi_client.Configuration(
            host=self.prompt.osis_endpoint(),
            username=self.prompt.osis_username(),
            password=self.prompt.osis_password()
        )
        self.configuration.access_token = None
        self.configuration.verify_ssl = False
        
        self.s3_endpoint = self.prompt.osis_s3_endpoint()
        self.s3_host = urlparse(self.s3_endpoint).netloc
        
        self._init_choices()
    
    def _init_choices(self):
        try:
            items = [Choice(OsisVerifier._get_method_doc(method), method) for name, method in
                     (inspect.getmembers(self, predicate=inspect.ismethod))
                     if str(name).startswith('verify')]
            
            items.insert(0, Choice(OsisVerifier._get_method_doc(self.quit), self.quit))
            items.append(Choice(self._get_method_doc(self.onboard_and_s3), self.onboard_and_s3))
            
            self.choices = {i: item
                            for i, item in enumerate(items)}
        except Exception as e:
            print(colored(f'Error occurs... Quit.\n{e}', 'red'))
            logger.exception(e)
            sys.exit(0)
    
    def run(self):
        with openapi_client.ApiClient(self.configuration) as api_client:
            while True:
                try:
                    self.print_banner('The verification items', max_width=60)
                    for k, v in self.choices.items():
                        print('%d. %s' % (k, v.description))
                    
                    user_choice = int(self.prompt.prompt_choice())
                    
                    if user_choice not in self.choices:
                        print(colored('#Invalid choice!#\n', 'red'))
                        continue

                    time.sleep(0.5)
                    self.choices[user_choice].callable(api_client)
                    time.sleep(1)
                except ValueError:
                    print(colored('\n#Enter number of the verifier items instead of other characters.#\n', 'red'))
                except Exception as e:
                    logger.exception(e)
                    time.sleep(1)
                    print(colored(
                        '\n#Error is detected. Please refer the log osis-verifier.log for the exception detail.#\n',
                        'red'))
    
    @classmethod
    def quit(cls, *args):
        """
        Quit the verifier
        """
        
        print('\nQuit the verifier.')
        sys.exit(0)
    
    @classmethod
    def _get_method_doc(cls, method):
        return inspect.getdoc(method)
    
    @classmethod
    def print_banner(cls, msg, *args, max_width=120):
        print(terminal_banner.Banner(msg.format(*args), max_width=max_width))
    
    @classmethod
    def validate_tenant(cls, tenant, exp_cd_tenant_id):
        assert tenant.active
        assert exp_cd_tenant_id in tenant.cd_tenant_ids
        assert tenant.tenant_id is not None
    
    @classmethod
    def validate_user(cls, user, exp_status, exp_cd_tenant_id, exp_cd_user_id):
        assert exp_status == user.active
        assert exp_cd_tenant_id == user.cd_tenant_id
        assert exp_cd_user_id == user.cd_user_id
        assert user.canonical_user_id is not None
        assert user.tenant_id is not None
        assert user.user_id is not None
        assert user.username is not None
    
    @classmethod
    def validate_credential(cls, credential, exp_cd_tenant_id, exp_cd_user_id, exp_tenant_id, exp_user_id,
                            exp_access_key=None):
        assert exp_cd_tenant_id == credential.cd_tenant_id
        assert exp_cd_user_id == credential.cd_user_id
        assert exp_tenant_id == credential.tenant_id
        assert exp_user_id == credential.user_id
        assert credential.access_key is not None
        assert credential.secret_key is not None
        assert exp_access_key is None or credential.access_key == exp_access_key
    
    @classmethod
    def validate_info(cls, info):
        assert info.platform_name is not None
        assert info.platform_version is not None
        assert info.api_version is not None
        assert info.logo_uri is not None
        assert info.status is not None
        assert info.auth_modes is not None
        assert len(info.auth_modes) > 0
    
    @classmethod
    def validate_capability(cls, capability):
        assert capability.exclusions is not None
        assert len(capability.exclusions) > 0
    
    def verify_tenant_api(self, api_client):
        """
        Verify Tenant APIs
        """
        cd_tenant_name = namegenerator.gen()
        cd_tenant_id_1 = uuid.uuid4().hex
        cd_tenant_id_2 = uuid.uuid4().hex
        tenant_api_instance = openapi_client.TenantApi(api_client)
        
        updated_tenant = None
        
        try:
            params = {
                'filter': f'cd_tenant_id=={cd_tenant_id_1}'
            }
            
            self.print_banner('Query tenant /api/v1/tenants/query?filter=cd_tenant_id=={}', cd_tenant_id_1)
            tenants = tenant_api_instance.query_tenants(**params)
            if tenants.page_info.total > 0:
                raise Exception(f'Cloud Director tenant with UUID {cd_tenant_id_1} should NOT appear in platform.')
            print(f'The tenant with cd_tenant_id=={cd_tenant_id_1} does not exist\n')
            
            osis_tenant = {'name': cd_tenant_name, 'active': True, 'tenant_id': None,
                           'cd_tenant_ids': [cd_tenant_id_1]}
            self.print_banner('Create tenant /api/v1/tenants')
            print(f'Payload:')
            pprint(osis_tenant)
            new_tenant = tenant_api_instance.create_tenant(osis_tenant=osis_tenant)
            self.validate_tenant(new_tenant, cd_tenant_id_1)
            print(f'New tenant created:')
            pprint(new_tenant)
            print('\n')
            
            self.print_banner('Head tenant /api/v1/tenants/{}', new_tenant.tenant_id)
            tenant_api_instance.head_tenant(new_tenant.tenant_id)
            print(f'Tenant {new_tenant.tenant_id} exists\n')
            
            self.print_banner('Patch tenant /api/v1/tenants/{}', new_tenant.tenant_id)
            osis_tenant = {'name': cd_tenant_name, 'active': True, 'tenant_id': None,
                           'cd_tenant_ids': [cd_tenant_id_1, cd_tenant_id_2]}
            print(f'Payload:')
            pprint(osis_tenant)
            updated_tenant = tenant_api_instance.update_tenant(new_tenant.tenant_id, osis_tenant=osis_tenant)
            print(f'The tenant {updated_tenant.tenant_id} updated')
            pprint(updated_tenant)
            OsisVerifier.validate_tenant(updated_tenant, cd_tenant_id_1)
            OsisVerifier.validate_tenant(updated_tenant, cd_tenant_id_2)
            print('\n')
            
            self.print_banner('List tenants /api/v1/tenants')
            tenants = tenant_api_instance.list_tenants()
            print(f'Tenants listed')
            pprint(tenants)
            print('\n')
            
            self.print_banner('Query tenant /api/v1/tenants/query?filter=cd_tenant_id=={}', cd_tenant_id_1)
            tenants = tenant_api_instance.query_tenants(**params)
            pprint(tenants)
            assert tenants.page_info.total == 1
            print('\n')
            
            print(colored('\nTenant APIs pass verification.', 'green'))
        finally:
            if updated_tenant is not None:
                self.print_banner('Clean up data\nDelete tenant /api/v1/tenants/{}', updated_tenant.tenant_id)
                tenant_api_instance.delete_tenant(updated_tenant.tenant_id)
                print(f'Tenant {updated_tenant.tenant_id} deleted')
    
    def verify_user_api(self, api_client):
        """
        Verify User APIs
        """
        tenant_api_instance = openapi_client.TenantApi(api_client)
        user_api_instance = openapi_client.UserApi(api_client)
        
        cd_tenant_name = namegenerator.gen()
        cd_tenant_id = uuid.uuid4().hex
        cd_user_id = uuid.uuid4().hex
        user_name = namegenerator.gen()
        
        new_tenant = None
        new_user = None
        
        try:
            
            osis_tenant = {'name': cd_tenant_name, 'active': True, 'tenant_id': None,
                           'cd_tenant_ids': [cd_tenant_id]}
            self.print_banner('Create tenant /api/v1/tenants')
            print(f'Payload:')
            pprint(osis_tenant)
            new_tenant = tenant_api_instance.create_tenant(osis_tenant=osis_tenant)
            self.validate_tenant(new_tenant, cd_tenant_id)
            print(f'New tenant created:')
            pprint(new_tenant)
            print('\n')
            
            params = {
                'filter': f'tenant_id=={new_tenant.tenant_id};cd_tenant_id=={cd_tenant_id}'
            }
            self.print_banner('Query users /api/v1/users/query?filter=tenant_id=={};cd_tenant_id=={}',
                              new_tenant.tenant_id, cd_tenant_id)
            pprint(user_api_instance.query_users(**params))
            print('\n')
            
            osis_user = {'tenant_id': new_tenant.tenant_id,
                         'active': True, 'username': user_name, 'role': 'TENANT_ADMIN',
                         'cd_user_id': cd_user_id,
                         'cd_tenant_id': cd_tenant_id}
            self.print_banner('Create user /api/v1/users')
            new_user = user_api_instance.create_user(new_tenant.tenant_id, osis_user)
            OsisVerifier.validate_user(new_user, True, cd_tenant_id, cd_user_id)
            pprint(new_user)
            print('\n')
            
            self.print_banner('Get users /api/v1/tenants/{}/users', new_tenant.tenant_id)
            users = user_api_instance.list_users(new_tenant.tenant_id)
            assert users.page_info.total == 1
            pprint(users)
            print('\n')
            
            self.print_banner('Get user /api/v1/tenants/{}/users/{}', new_tenant.tenant_id, new_user.user_id)
            user = user_api_instance.get_user_with_id(new_tenant.tenant_id, new_user.user_id)
            OsisVerifier.validate_user(new_user, True, cd_tenant_id, cd_user_id)
            pprint(user)
            print('\n')
            
            self.print_banner('Patch user /api/v1/tenants/{}/users/{}', new_tenant.tenant_id, new_user.user_id)
            osis_user = {'tenant_id': new_tenant.tenant_id,
                         'active': False, 'username': user_name, 'role': 'TENANT_ADMIN',
                         'cd_user_id': cd_user_id,
                         'cd_tenant_id': cd_tenant_id}
            print(f'Payload:')
            pprint(osis_user)
            updated_user = user_api_instance.update_user_status(new_tenant.tenant_id, new_user.user_id, osis_user)
            print(f'The user {updated_user.tenant_id} updated')
            pprint(updated_user)
            assert updated_user.active is False
            self.validate_user(updated_user, False, cd_tenant_id, cd_user_id)
            print('\n')
            
            self.print_banner('Get user /api/v1/users/{}', new_user.canonical_user_id)
            user = user_api_instance.get_user_with_canonical_id(new_user.canonical_user_id)
            self.validate_user(user, False, cd_tenant_id, cd_user_id)
            pprint(user)
            print('\n')
            
            params = {
                'filter': f'tenant_id=={new_tenant.tenant_id};cd_tenant_id=={cd_tenant_id};user_id=={new_user.user_id};cd_user_id=={new_user.cd_user_id};username=={new_user.username}'
            }
            self.print_banner(
                'Query users /api/v1/users/query?filter=tenant_id=={};cd_tenant_id=={};user_id=={};cd_user_id=={}',
                new_tenant.tenant_id,
                cd_tenant_id, new_user.user_id, new_user.cd_user_id)
            users = user_api_instance.query_users(**params)
            assert users.page_info.total == 1
            pprint(users)
            print('\n')
            
            print(colored('\nUser APIs pass verification.', 'green'))
        
        finally:
            if new_tenant is not None and new_user is not None:
                self.print_banner('Clean up data\nDelete user /api/v1/tenants/{}/users/{}', new_tenant.tenant_id,
                                  new_user.user_id)
                user_api_instance.delete_user(new_tenant.tenant_id, new_user.user_id)
                print(f'User {new_user.user_id} deleted\n')
            
            if new_tenant is not None:
                self.print_banner('Clean up data\nDelete tenant /api/v1/tenants/{}', new_tenant.tenant_id)
                tenant_api_instance.delete_tenant(new_tenant.tenant_id)
                print(f'Tenant {new_tenant.tenant_id} deleted')
    
    def verify_credential_api(self, api_client):
        """
        Verify S3 Credential APIs
        """
        
        tenant_api_instance = openapi_client.TenantApi(api_client)
        user_api_instance = openapi_client.UserApi(api_client)
        credential_api_instance = openapi_client.S3credentialApi(api_client)
        
        cd_tenant_name = namegenerator.gen()
        cd_tenant_id = uuid.uuid4().hex
        cd_user_id = uuid.uuid4().hex
        user_name = namegenerator.gen()
        
        new_tenant = None
        new_user = None
        
        try:
            osis_tenant = {'name': cd_tenant_name, 'active': True, 'tenant_id': None,
                           'cd_tenant_ids': [cd_tenant_id]}
            
            self.print_banner('Create tenant /api/v1/tenants:')
            print(f'Payload:')
            pprint(osis_tenant)
            new_tenant = tenant_api_instance.create_tenant(osis_tenant=osis_tenant)
            self.validate_tenant(new_tenant, cd_tenant_id)
            print(f'New tenant created:')
            pprint(new_tenant)
            print('\n')
            
            osis_user = {'tenant_id': new_tenant.tenant_id,
                         'active': True, 'username': user_name, 'role': 'TENANT_ADMIN',
                         'cd_user_id': cd_user_id,
                         'cd_tenant_id': cd_tenant_id}
            self.print_banner('Create user /api/v1/users')
            print(f'Payload:')
            new_user = user_api_instance.create_user(new_tenant.tenant_id, osis_user)
            self.validate_user(new_user, True, cd_tenant_id, cd_user_id)
            pprint(new_user)
            print('\n')
            
            params = {
                'filter': f'cd_tenant_id=={cd_tenant_id};cd_user_id=={cd_user_id};tenant_id=={new_tenant.tenant_id};user_id=={new_user.user_id};'
            }
            self.print_banner(
                'Query S3 credentials /api/v1/s3credentials/query?filter=cd_tenant_id=={};cd_user_id=={};tenant_id=={};user_id=={};',
                cd_tenant_id, cd_user_id, new_tenant.tenant_id, new_user.user_id)
            credentials = credential_api_instance.query_credentials(**params)
            assert credentials.page_info.total == 1
            self.validate_credential(credentials.items[0], cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id)
            pprint(credentials)
            print('\n')
            
            self.print_banner('Get S3 credentials /api/v1/tenants/{}/users/{}/s3credentials', new_tenant.tenant_id,
                              new_user.user_id)
            credentials = credential_api_instance.list_credentials(new_tenant.tenant_id, new_user.user_id)
            assert credentials.page_info.total == 1
            self.validate_credential(credentials.items[0], cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id)
            pprint(credentials)
            print('\n')
            
            self.print_banner('Create S3 credentials /api/v1/tenants/{}/users/{}/s3credentials', new_tenant.tenant_id,
                              new_user.user_id)
            new_credential = credential_api_instance.create_credential(new_tenant.tenant_id, new_user.user_id)
            self.validate_credential(new_credential, cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id,
                                     new_credential.access_key)
            pprint(new_credential)
            print('\n')
            
            params = {
                'filter': f'cd_tenant_id=={cd_tenant_id};cd_user_id=={cd_user_id};tenant_id=={new_tenant.tenant_id};user_id=={new_user.user_id};access_key=={new_credential.access_key}'
            }
            self.print_banner(
                'Query S3 credentials /api/v1/s3credentials/query?filter=cd_tenant_id=={};cd_user_id=={};tenant_id=={};user_id=={};access_key=={}',
                cd_tenant_id, cd_user_id, new_tenant.tenant_id, new_user.user_id, new_credential.access_key)
            credentials = credential_api_instance.query_credentials(**params)
            assert credentials.page_info.total == 1
            self.validate_credential(credentials.items[0], cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id,
                                     new_credential.access_key)
            pprint(credentials)
            print('\n')
            
            self.print_banner('Get S3 credentials /api/v1/s3credentials/{}', new_credential.access_key)
            credential = credential_api_instance.get_credential(new_credential.access_key)
            self.validate_credential(credential, cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id,
                                     new_credential.access_key)
            pprint(credential)
            print('\n')
            
            print(colored('\nS3 Credential APIs pass verification.', 'green'))
        finally:
            if new_tenant is not None and new_user is not None:
                self.print_banner('Clean up data\nDelete user /api/v1/tenants/{}/users/{}', new_tenant.tenant_id,
                                  new_user.user_id)
                user_api_instance.delete_user(new_tenant.tenant_id, new_user.user_id)
                print(f'User {new_user.user_id} deleted\n')
            
            if new_tenant is not None:
                self.print_banner('Clean up data\nDelete tenant /api/v1/tenants/{}', new_tenant.tenant_id)
                tenant_api_instance.delete_tenant(new_tenant.tenant_id)
                print(f'Tenant {new_tenant.tenant_id} deleted')
    
    def onboard_and_s3(self, api_client):
        """
        Verify tenant/user onboard and S3 request
        """
        
        tenant_api_instance = openapi_client.TenantApi(api_client)
        user_api_instance = openapi_client.UserApi(api_client)
        credential_api_instance = openapi_client.S3credentialApi(api_client)
        
        cd_tenant_name = namegenerator.gen()
        cd_tenant_id = uuid.uuid4().hex
        cd_user_id = uuid.uuid4().hex
        user_name = namegenerator.gen()
        
        new_tenant = None
        new_user = None
        
        try:
            params = {
                'filter': f'cd_tenant_id=={cd_tenant_id}'
            }
            
            osis_tenant = {'name': cd_tenant_name, 'active': True, 'tenant_id': None,
                           'cd_tenant_ids': [cd_tenant_id]}
            
            self.print_banner('Create tenant /api/v1/tenants:')
            print(f'Payload:')
            pprint(osis_tenant)
            new_tenant = tenant_api_instance.create_tenant(osis_tenant=osis_tenant)
            self.validate_tenant(new_tenant, cd_tenant_id)
            print(f'New tenant created:')
            pprint(new_tenant)
            print('\n')
            
            self.print_banner('Query tenant /api/v1/tenants/query?filter=cd_tenant_id=={}', cd_tenant_id)
            tenants = tenant_api_instance.query_tenants(**params)
            pprint(tenants)
            assert tenants.page_info.total == 1
            print('\n Finish tenant onboard.')
            
            params = {
                'filter': f'tenant_id=={new_tenant.tenant_id};cd_tenant_id=={cd_tenant_id};cd_user_id=={cd_user_id}'
            }
            self.print_banner(
                'Query users /api/v1/users/query?filter=cd_tenant_id=={};cd_user_id=={}',
                cd_tenant_id, cd_user_id)
            users = user_api_instance.query_users(**params)
            assert users.page_info.total == 0
            pprint(users)
            
            osis_user = {'tenant_id': new_tenant.tenant_id,
                         'active': True, 'username': user_name, 'role': 'TENANT_ADMIN',
                         'cd_user_id': cd_user_id,
                         'cd_tenant_id': cd_tenant_id}
            self.print_banner('Create user /api/v1/users')
            print(f'Payload:')
            new_user = user_api_instance.create_user(new_tenant.tenant_id, osis_user)
            self.validate_user(new_user, True, cd_tenant_id, cd_user_id)
            pprint(new_user)
            print('\n')
            
            params = {
                'filter': f'cd_tenant_id=={cd_tenant_id};cd_user_id=={cd_user_id};tenant_id=={new_tenant.tenant_id};user_id=={new_user.user_id};'
            }
            self.print_banner(
                'Query S3 credentials /api/v1/s3credentials/query?filter=cd_tenant_id=={};cd_user_id=={};tenant_id=={};user_id=={};',
                cd_tenant_id, cd_user_id, new_tenant.tenant_id, new_user.user_id)
            credentials = credential_api_instance.query_credentials(**params)
            assert credentials.page_info.total == 1
            self.validate_credential(credentials.items[0], cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id)
            pprint(credentials)
            print('\n')
            
            self.print_banner('Create S3 credentials /api/v1/tenants/{}/users/{}/s3credentials', new_tenant.tenant_id,
                              new_user.user_id)
            new_credential = credential_api_instance.create_credential(new_tenant.tenant_id, new_user.user_id)
            self.validate_credential(new_credential, cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id,
                                     new_credential.access_key)
            pprint(new_credential)
            print('\n')
            
            self.print_banner('Get S3 credentials /api/v1/tenants/{}/users/{}/s3credentials', new_tenant.tenant_id,
                              new_user.user_id)
            credentials = credential_api_instance.list_credentials(new_tenant.tenant_id, new_user.user_id)
            assert credentials.page_info.total == 2
            self.validate_credential(credentials.items[0], cd_tenant_id, cd_user_id, new_tenant.tenant_id,
                                     new_user.user_id)
            pprint(credentials)
            print('\n')
            
            self.print_banner('List S3 bucket with the credential of the new user {}', new_user.username)
            aws_client = AwsClient(aws_s3=self.s3_endpoint, access_key=credentials.items[0].access_key,
                                   secret_key=credentials.items[0].secret_key,
                                   host=self.s3_host,
                                   region='us',
                                   service='s3')
            pprint(aws_client.get_buckets().text)
            print(colored('\n Succeed to consume S3 API.', 'green'))
        
        finally:
            if new_tenant is not None and new_user is not None:
                self.print_banner('Clean up data\nDelete user /api/v1/tenants/{}/users/{}', new_tenant.tenant_id,
                                  new_user.user_id)
                user_api_instance.delete_user(new_tenant.tenant_id, new_user.user_id)
                print(f'User {new_user.user_id} deleted\n')
            
            if new_tenant is not None:
                self.print_banner('Clean up data\nDelete tenant /api/v1/tenants/{}', new_tenant.tenant_id)
                tenant_api_instance.delete_tenant(new_tenant.tenant_id)
                print(f'Tenant {new_tenant.tenant_id} deleted')
    
    def verify_info_api(self, api_client):
        """
        Verify Info API
        """
        info_api_instance = openapi_client.InfoApi(api_client)
        
        self.print_banner('Get /api/info')
        info = info_api_instance.get_info()
        self.validate_info(info)
        pprint(info)
        
        print(colored('\nInfo API passes verification.', 'green'))
    
    def verify_capability_api(self, api_client):
        """
        Verify S3 Capabilities API
        """
        capability_api_instance = openapi_client.S3capabilityApi(api_client)
        
        self.print_banner('Get /api/v1/s3capabilities')
        capability = capability_api_instance.get_s3_capabilities()
        self.validate_capability(capability)
        pprint(capability)
        
        print(colored('\nS3 Capabilities API passes verification.', 'green'))


class PromptUserInput(object):
    osis_endpoint_msg = 'Input OSIS Endpoint: [example - {}] '
    
    osis_s3_endpoint_msg = 'Input OSIS S3 Endpoint: [example - {}] '
    
    osis_username_msg = 'Input OSIS Username: '
    
    osis_password_msg = 'Input OSIS Password: '
    
    verifier_choice_msg = '\nWhat\'s your choice?\n'
    
    @classmethod
    def prompt_func(cls, message):
        time.sleep(0.2)
        return input(message)
    
    def osis_s3_endpoint(self):
        return self.prompt_func(self.osis_s3_endpoint_msg.format('http://ceph.osis.ose.vmware.com:31383'))
    
    def osis_endpoint(self):
        return self.prompt_func(self.osis_endpoint_msg.format('https://localhost:8443'))
    
    def osis_username(self):
        return self.prompt_func(self.osis_username_msg)
    
    def osis_password(self):
        return self.prompt_func(self.osis_password_msg)
    
    def prompt_choice(self):
        return self.prompt_func(self.verifier_choice_msg)


def main():
    logging.basicConfig(
        filename='osis-verifier.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s'
    )
    OsisVerifier(PromptUserInput()).run()


if __name__ == '__main__':
    main()
