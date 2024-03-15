
from tools.create_cases.core.t_utils import *
import pandas as pd
import json


class GenerateCases:

    def extract_data(self, file_path):
        data = {}
        data_src = open(file_path, 'r+')
        data_d = json.load(data_src)['shapes']
        d_k = list(data_d.keys())
        print('******', d_k)
        for i in range(len(d_k)):
            if d_k[i].endswith('Request'):
                key = d_k[i]
                value = data_d[d_k[i]]
                data.update({key: value})
        return data

    def re_data(self, item_data, action_n, user_data, default_data):
        req_parm = []

        for i in item_data.keys():
            if i == 'required':
                req_parm = item_data[i]

            if i == 'members':
                param_tab = pd.read_json(json.dumps(item_data[i]), orient='index')
                mixed_param_data = generate_parm(action_n, param_tab, req_parm, user_data, default_data)
                parm_l = mixed_param_data[0]
                catalog_l_1 = mixed_param_data[1]

        case_rows = len(parm_l)

        index = generate_tcid(case_rows, action_n, suite_n='test')[0]
        tcid = generate_tcid(case_rows, action_n, suite_n='test')[1]
        vrb = generate_variables(case_rows, action_n, parm_l)
        catalog = generate_catalog(case_rows, action_n, catalog_l_1)
        precondition = generate_precondition(case_rows, action_n, parm_l)
        cleanup = clean_data(case_rows, action_n, parm_l)

        case_info_d = {
            'index': index,
            'TCID': tcid,
            'Variables': vrb,
            'Catalog': catalog,
            'Action': action_n,
            'required': req_parm,
            'Parameter': parm_l,
            'PreCondition': precondition,
            'Cleanup': cleanup
        }

        return case_info_d

    def to_csv_file(self, columns, user_data, default_data, src_data_path):
        data = self.extract_data(src_data_path)
        action_l = list(data.keys())
        for item in range(len(action_l)):
            print('*******************', action_l[item], '*********************')
            action_n = re_name_action(action_l[item])
            item_data = data[action_l[item]]
            case_info_d = self.re_data(item_data, action_n, user_data, default_data)
            index = case_info_d.get('index')
            rows = len(index)
            re_data_all = pd.DataFrame(index=index, columns=columns)

            r_k = list(case_info_d.keys())
            for i in range(len(r_k)):
                if r_k[i] in columns:
                    re_data_all.at[0:rows, r_k[i]] = case_info_d.get(r_k[i])

            # TODO
            re_data_all.at[0:rows, 'Role'] = 'group1:user1'
            re_data_all.at[0:rows, 'Priority'] = 'P3'
            re_data_all.at[0:rows, 'ClientType'] = 'S3CompatibleAPI'
            re_data_all.at[0:rows, 'ExpectResponseCode'] = '200'
            re_data_all.at[0:rows, 'CaseTitle'] = case_info_d.get('Catalog')

            action_name = 'test_' + case_info_d.get('Action') + '_auto.csv'

            if 'bucket' in action_name:
                re_data_all.to_csv("case_data/test_bucket/" + action_name, index=False)
            elif 'object' in action_name:
                re_data_all.to_csv("case_data/test_object/" + action_name, index=False)
            else:
                re_data_all.to_csv("case_data/test_others/" + action_name, index=False)


if __name__ == '__main__':
    pass
