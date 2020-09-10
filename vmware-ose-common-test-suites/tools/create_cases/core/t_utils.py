import re
import os
import yaml


def generate_tcid(rows, action, suite_n='Test'):
    index = []
    tcid_l = []
    for i in range(rows):
        index.append(i)
        tcid = suite_n + '#' + action + '#' + str(i+2)
        tcid_l.append(tcid)

    return index, tcid_l


def generate_catalog(rows, action, predata=None):
    catalog_l = []
    for i in range(rows):
        if isinstance(predata, list):
            catalog = action.replace('_', ' ') + '|' + predata[i]
            catalog_l.append(catalog)
        else:
            catalog = action.replace('_', ' ')
            catalog_l.append(catalog)

    return catalog_l


# TODO
def clean_data(rows, action, parm):
    cln_l = []
    for i in range(rows):
        if isinstance(parm, list):
            bkt_name = parm[i].get('Bucket')
            if isinstance(bkt_name, str):
                cln_up = '[("group1:user1", "S3CompatibleAPI", "force_delete_bucket", ' \
                            '{"Bucket":"' + bkt_name + '"}, [204, 404])]'
            else:
                # TODO
                cln_up = '["TODO: EmptyUserData"]'
            cln_l.append(cln_up)
    return cln_l


# TODO add other variables
def generate_variables(rows, action, parm):
    var_l = []
    for i in range(rows):
        if 'bucket_name' in parm[i].keys():
            bkt_v = parm[i].get('bucket_name')
        else:
            bkt_v = 'bkt-default'
        bkt_t = '"' + bkt_v + '.%s"%timestamp(format="%Y-%m-%dt%H-%M-%S.%fz")'
        var_d = {'bucket_name': bkt_t}
        var_l.append(var_d)
    return var_l


def generate_precondition(rows, action, parm):
    pre_l = []
    crt_bkt = ''
    cln_up = ''
    put_obj = ''
    for i in range(rows):
        if 'Bucket' in parm[i].keys():
            bkt_name = parm[i].get('Bucket')
            obj_name = 'obj-default'
            if isinstance(bkt_name, str):
                cln_up = '("group1:user1", "S3CompatibleAPI", "force_delete_bucket", ' \
                           '{"Bucket":"' + bkt_name + '"}, [204, 404])'
                crt_bkt = '("group1:user1", "S3CompatibleAPI", "create_bucket", ' \
                          '{"Bucket":"' + bkt_name + '"}, [200])'
                put_obj = '("group1:user1", "S3CompatibleAPI", "put_object", ' \
                          '{"Bucket":"' + bkt_name + '", "Key":"' + obj_name + '", "Body":"Test"}, [200])'
            else:
                # TODO
                print('There is no bucket name')

            if 'bucket' in action:
                if action == 'create_bucket':
                    pre = '[' + cln_up + ']'
                else:
                    pre = '[' + cln_up + ',\n' + crt_bkt + ',\n' + put_obj + ']'
            elif 'object' in action:
                if action == 'put_object':
                    pre = '[' + cln_up + ',\n' + crt_bkt + ']'
                else:
                    pre = '[' + cln_up + ',\n' + crt_bkt + ',\n' + put_obj + ']'
            else:
                pre = '[' + cln_up + ']'

            pre_l.append(pre)

        else:
            # TODO
            pre = '["TODO: EmptyUserData"]'
            pre_l.append(pre)

    return pre_l


def generate_parm(action_n, param_tab, req_data, user_data, default_data):
    parm_data_l = []
    catalog_sum = []
    parm_dict = {}
    cfg_l = []
    test_data = {}
    # prepare parameter
    if 'xmlNamespace' in param_tab.columns:
        xml_ns = param_tab.loc[:, 'xmlNamespace']
        for i in range(len(xml_ns)):
            if xml_ns[i]:
                cfg = xml_ns.index[i]
                cfg_l.append(cfg)
    else:
        pass

    parm_l = cfg_l

    if 'shape' in param_tab.columns:
        shape_n = param_tab.loc[:, 'shape']
        for i in range(len(shape_n)):
            if shape_n[i] == 'Body':
                sap = shape_n.index[i]
                parm_l.append(sap)

    if 'location' in param_tab.columns:
        location = param_tab.loc[:, 'location']
    else:
        location = []

    for i in range(len(location)):
        if location[i] in ['header', 'headers', 'querystring']:
            parm = param_tab.index[i]
            parm_l.append(parm)

    # supply parameter value
    all_parm = list(set(req_data+parm_l))
    for i in range(len(all_parm)):
        if action_n in list(default_data.keys()):
            if all_parm[i] in list(default_data[action_n].keys()):
                default_d = {all_parm[i]: default_data[action_n][all_parm[i]]}
                test_data.update(default_d)
            else:
                test_data.update({all_parm[i]: 'TODO'})
        else:
            test_data.update({all_parm[i]: 'TODO'})
        if test_data.get('Bucket') == 'TODO':
            test_data.update({'Bucket': 'bkt-default'})
        if test_data.get('Key') == 'TODO':
            test_data.update({'Key': 'obj_default'})

        # keep initial bucket value for generate variables
        test_data.update({'bucket_name': test_data.get('Bucket')})

        # update bucket name with timestamp
        test_data.update({'Bucket': 'self.variables["bucket_name"]'})

    # update test_data by user definition data
    test_data.update(user_data['user_definition'])

    # required parameters
    if isinstance(req_data, list):
        for i in range(len(req_data)):
            value_l = str(test_data[req_data[i]]).split(' | ')[0]
            if isinstance(value_l, str):
                parm_dict.update({req_data[i]: value_l})

    # keep static parameters
    key_marker = list(user_data['keep_param'].keys())
    for i in range(len(key_marker)):
        key = key_marker[i]
        value = user_data['keep_param'][key_marker[i]]
        if key in parm_l:
            parm_dict.update({key: value})
        else:
            pass

    # mixed values of parameters
    if isinstance(all_parm, list):
        for i in range(0, len(all_parm)):
            if all_parm[i] in ['GrantFullControl', 'GrantRead', 'GrantReadACP', 'GrantWrite', 'GrantWriteACP']:
                value_l = str(test_data['Grant']).split(' | ')
            else:
                value_l = str(test_data[all_parm[i]]).split(' | ')

            if value_l:
                for j in range(len(value_l)):
                    mix_value = {all_parm[i]: value_l[j]}
                    parm_data = {**parm_dict, **mix_value}
                    print(parm_data)
                    parm_data_l.append(parm_data)
                    catalog_sum.append(all_parm[i])

    else:
        parm_data_l = [parm_dict]

    return parm_data_l, catalog_sum


def re_name_action(action):
    pre_action = re.sub('[A-Z]', lambda x: '_'+x.group(0).lower(), action)
    action_new = re.sub('_request', '', pre_action)[1:]
    return action_new


def get_shape_info(data):
    data_shape = data.shape
    rows_count = list(data_shape)[0]
    columns_count = list(data_shape)[1]
    columns_content = data.columns
    data_dict = {
        'rows_count': rows_count,
        'columns_count': columns_count,
        'columns_content': columns_content
    }

    return data_dict


def get_prj_base_dir():

    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def get_param_data_info(data):
    rp = get_prj_base_dir()
    config_file_path = os.path.join(rp, 'tools/create_cases', data)
    with open(config_file_path, 'r') as f:
        config_profile = yaml.load(f, Loader=yaml.FullLoader)

    test_data = config_profile

    return test_data
