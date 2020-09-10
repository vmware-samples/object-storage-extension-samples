from tools.create_cases.core.generate_cases import GenerateCases
from tools.create_cases.core.t_utils import *

generate = GenerateCases()

# csv column definition
columns_seq = ['TCID', 'CaseTitle', 'Catalog', 'Priority', 'Variables', 'PreCondition',
               'Role', 'ClientType', 'AuthSettings', 'Action', 'Parameter', 'ExpectResponseCode',
               'ExpectResponseHeader', 'ExpectResponseBody',
               'ExpectResponseBodySchema', 'PostValidation', 'Cleanup',
               'Description', 'Comment']

user_data = get_param_data_info('prepare_data.yml')
default_data = get_param_data_info('default_data.yml')

# source data
root_path = get_prj_base_dir()
src_data_path = root_path+'/framework/libs/s3api/models/s3/custom-xml/service-2.json'

generate.to_csv_file(columns_seq, user_data, default_data, src_data_path)
