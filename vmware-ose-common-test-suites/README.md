# S3 compatibility tests

## Descriptions

This tool provides common test suites for storage vendors. A set of AWS S3 compatible API test cases would be provided
and the storage vendors can run this tool to compare the results so that there won't be any regressions after up-gradation of newer 
versions of storage platform.

## Scenarios
- Tenant onboard and user onboard testing
    
    Validate if the Cloud Director tenants and users are successfully on board.


- S3 compatible API testing

    Validate if the provisioned S3 compatible API cases can be tested pass via user's access key and secret key.

## Preliminaries

- The test environment of vCD, OSE and storage platform needs to be setup according to OSE release notes.

- Have _python 3.0+_ installed

- Have _virtualenv_ installed
    
    `pip install virtualenv`

- Have required libraries installed

    `pip install -r requirements.txt`



## Configure

You need to specify test parameters before starting test. Editing user profile or passing command options are both supported.

### Command Options
**Required parameters:** 

- URL: You can specify vcd url, ose url. 

    `--vcd-url` `--ose-url`

- Test user: Primary test user is required and specify the user's login username and password as below.

    `--vcd-user` `--vcd-password`

**Optional parameters:**

- Test scope: Test scope is to determine test case scope including FULL and the pre-defined vendor names. If a vendor is specified, some cases can be excluded if we know these cases are not supported yet.

    `--scope [full, {vendor-name: cloudian or ecs}] ` 

- Virtual hosting style: Access to S3 resources by virtual-hosting style is supported. By default, path style is used.

    `--virtual-host-style`

- More options

    `python ose-runner.py -h`

**Update user profile**

### Edit User Profile
A sample user profile "user_profile.yml" has been provided in the repository. Once you copied and edited, you can run with new user profile:

`python ose-runner.py --file {new_user_profile.yml}`

More details on user profile keys are described in user profile.

## Run

You can run S3 tests with user profile or configured options

- Run with user profile

    `python ose-runner.py`

- Run with options

    `python ose-runner.py --vcd-url --ose-url --vcd-user --vcd-password --scope cloudian`
    
    `python ose-runner.py --testcases TestOthers#test03_test_create_multipart_upload#14-18 TestBucket#test01_test_create_bucket#3,12`





