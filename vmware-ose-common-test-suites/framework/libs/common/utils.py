import csv
import json
import re
import os
import pathlib
import shutil
import random
import yaml
import xmltodict
import time
from urllib.parse import quote, unquote
from subprocess import Popen
import subprocess
import requests
from framework.libs.s3api.s3_compatible_api import S3CompatibleAPI

import logging
from framework.addons.Logger import TestLog


def get_logger(log_level):
    logger = TestLog().getlog()
    log_level = log_level.upper() if log_level.lower() in [
        'info', 'warn', 'debug', 'error'] else 'INFO'
    logger.setLevel(getattr(logging, log_level))
    return logger


# load csv to [[OrderDict]]
def load_csv(csv_fp):
    res = []
    with open(csv_fp, "r") as csv_f:
        d_r = csv.DictReader(csv_f)
        for it in d_r:
            res.append([it])
    return res, csv_fp


def update_csv(res, csv_fp):
    fields = res[0][0].keys()
    with open(csv_fp, "w") as csv_f:
        d_w = csv.DictWriter(csv_f, fieldnames=fields)
        d_w.writeheader()
        for it in res:
            d_w.writerow(it[0])


def load_json(json_fp):
    with open(json_fp, 'r') as load_f:
        res = json.load(load_f)

    return res


def dump_yml(yml_fp, o):
    with open(yml_fp, 'w+') as outfile:
        yaml.dump(o, outfile)


def read_yml(yml_fp):
    with open(yml_fp, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def parse_xml_to_json(str_to_parse):
    if isinstance(str_to_parse, (str, bytes)) and str_to_parse:
        try:
            xml_dict = xmltodict.parse(str_to_parse, xml_attribs=False)
            return json.dumps(xml_dict)
        except:
            return str_to_parse
    elif isinstance(str_to_parse, dict):
        return json.dumps(str_to_parse)
    else:
        return str_to_parse


def url_encode(s):
    return quote(s, 'utf-8')


def url_decode(s):
    return unquote(s, 'utf-8')


# get group list for data provider
def get_group_list(old_prov):
    prov, _ = old_prov
    group_l = []
    for i in prov:
        grouplist = []
        priority = i[0].get("Priority")
        if priority is not None and priority.strip() != "":
            grouplist.append(priority)
        else:
            grouplist.append("P2")
        tcid = i[0].get("TCID")
        if tcid is not None and tcid:
            grouplist.append(tcid)
        tags = i[0].get("Tags")
        tagslist = []
        if tags is not None:
            tagslist = set([x.strip() for x in tags.split(',') if x.strip() != ''])
        grouplist.extend(tagslist)

        catalog = i[0].get("Catalog")
        if catalog is not None and catalog:
            grouplist.append(catalog)

        group_l.append(grouplist)

    return group_l


# get _doc_string list for data provider
def get_doc_string_list(old_prov):
    prov, _ = old_prov
    doc_str_l = []
    for i in prov:
        doc_str_l.append(i[0].get("CaseTitle"))
    return doc_str_l


def check_connection(host):
    if host == "":
        result = False

    with Popen(["ping -c 2 -W 5 " + host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as ping:
        ping_out = ping.stdout.read()
        ping_err = ping.stderr.read()

    if ping_out:
        ping_re = re.compile("100.*packet loss")
        if len(ping_re.findall(str(ping_out))) == 0:
            result = True
        else:
            result = False

    if ping_err:
        result = False
    return result


def get_fn_lst(dir_path):
    fn_lst = []
    for _, _, fns in os.walk(dir_path):
        for fn in fns:
            fn_lst.append(os.path.join(dir_path, fn))
    return fn_lst


def get_tmp_folder():
    fdir = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(fdir):
        mk_dir(fdir)
    return fdir


def rm_dir(path):
    shutil.rmtree(path)


def mk_dir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def create_file(file_dir, fn, size=5, unit="m"):
    fp = os.path.join(file_dir, fn)
    units = {'b': 1,
             'k': 1024,
             'm': 1024 * 1024,
             'g': 1024 * 1024 * 1024,
             't': 1024 * 1024 * 1024 * 1024}
    size = size*units[unit]
    with open(fp, 'wb') as f:
        f.write(os.urandom(size))
    return fp


def get_prj_base_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def handle_argument(keys, args):
    ose_args = dict()
    try:
        for arg in keys:
            arg_v = os.popen("echo $%s" % arg).read()
            if len(arg_v) > 1:
                arg_v = arg_v.strip("\n").upper()
            else:
                if hasattr(args, arg):
                    arg_v = getattr(args, arg)
                else:
                    arg_v = ''
            if arg_v:
                ose_args.update({arg: arg_v})

        return ose_args
    except:
        return


def get_case_scope(scope):
    from prj.cases.test_bucket import TestBucket
    from prj.cases.test_object import TestObject
    from prj.cases.test_others import TestOthers
    full_suites = [TestBucket, TestObject, TestOthers]
    if scope == 'full':
        sui_o = full_suites
    else:
        sui_o = full_suites
    return sui_o


def get_test_report_title():
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return str('s3-test') + '@' + current_time


def get_api_host_instance(self, usr_role='group1:user1', api_host='S3CompatibleAPI', auth_settings=None):
    # group1:user1
    new_k = usr_role + '@' + api_host

    _group = usr_role.split(':')[0]
    _user = usr_role.split(':')[1]

    if api_host in ['S3CompatibleAPI']:
        if new_k not in self.client_instances:
            s3_kwargs = dict()

            s3_kwargs.update({"aws_access_key_id": self.cfg_profile[
                _group][_user]['main_credential']['access_key'],
                              "aws_secret_access_key": self.cfg_profile[
                                  _group][_user]['main_credential']['secret_key'],
                              "verify": False,
                              "region_name": self.cfg_profile.get('storage').get('region')})

            if self.cfg_profile.get('virtual_host_style'):
                s3_kwargs["config"] = {"s3": {"addressing_style": "virtual"}}

            s3_kwargs["endpoint_url"] = self.cfg_profile.get('ose_url')

            if self.cfg_profile.get('vendor'):
                s3_kwargs.update({"endpoint_url": self.cfg_profile.get('vendor_s3_endpoint'),
                                  "region_name": self.cfg_profile.get('vendor_region')})

            s3_api = globals()[api_host](**s3_kwargs)
            self.client_instances[new_k] = s3_api
            self.logger.debug("Client info: %s" % new_k)
        return self.client_instances[new_k]

    else:
        pass


def get_boto_client(config_profile, group='group1', user='user1'):
    s3_kwargs = dict()

    s3_kwargs.update({
        "aws_access_key_id": config_profile[
            group][user]['main_credential']['access_key'],
        "aws_secret_access_key": config_profile[
            group][user]['main_credential']['secret_key'],
        "verify": False,
        "region_name": config_profile.get('storage').get('region')})

    if config_profile.get('virtual_host_style'):
        s3_kwargs["config"] = {"s3": {"addressing_style": "virtual"}}

    s3_kwargs["endpoint_url"] = config_profile.get('ose_url')

    if config_profile.get('vendor'):
        s3_kwargs.update({"endpoint_url": config_profile.get('vendor_s3_endpoint'),
                          "region_name": config_profile.get('vendor_region')})
    return S3CompatibleAPI(**s3_kwargs)


def remove_test_buckets(config_profile):
    boto3_client = get_boto_client(config_profile)
    buckets = boto3_client.list_buckets().get('Buckets')
    test_bucket_prefix = config_profile.get('test_bucket_prefix')
    if isinstance(buckets, list) and len(buckets) > 0:
        for bkt_item in buckets:
            if bkt_item.get('Name').startswith(test_bucket_prefix):
                print(bkt_item)
                boto3_client.force_delete_bucket(Bucket=bkt_item.get('Name'))

    print("Successfully cleaned up the test buckets.")
    return


'''
:param key: 'testcases'; 'scope'
:param ose_args: dict
:return: 
'''


def handle_ose_arguments(ose_args):
    if 'testcases' in ose_args and (
            ',' in str(ose_args.get('testcases'))
            or '-' in str(ose_args.get('testcases'))):
        # supports ', -'
        # TestBucket#test01_test_create_bucket#14 - 300
        # TestBucket#test01_test_create_bucket#14,15,37

        case_lst = ose_args.get('testcases')
        for case in case_lst:
            if ',' in case:
                suite_n, method_n, cases = case.split('#')

                for case_i in cases.split(','):
                    case_lst.append(suite_n + '#' + method_n + '#' + case_i.strip())

            if '-' in case:
                suite_n, method_n, cases = case.split('#')
                l, r = cases.split('-')
                for i in range(int(l), int(r)+1):
                    case_lst.append(suite_n + '#' + method_n + '#' + str(i))

        ose_args.update({'testcases': case_lst})

    if 'scope' in ose_args:
        pass
    return ose_args


def new_passdown_variables(actual_response, global_variables=None,
                           variables=None, action=None, parameters=None):
    if action == "create_multipart_upload":
        upload_id = actual_response.get('UploadId')
        if upload_id:
            obj_name = actual_response.get('Key')
            upload_id_index = obj_name + '_upload_id'
            global_variables[upload_id_index] = upload_id

    if action == "put_object":
        if variables is not None and 'object_name' in variables:
            obj_name = variables['object_name']
        else:
            if parameters and 'Key' in parameters:
                obj_name = parameters.get('Key')
            elif 'object_name' in global_variables:
                obj_name = global_variables['object_name']
            else:
                obj_name = 'uncertain'

        version_id = actual_response.get('VersionId')
        key_versions_index = obj_name + '_versions_v1'

        if version_id:
            if key_versions_index in global_variables.keys():
                global_variables[key_versions_index].append(version_id)
            else:
                global_variables[key_versions_index] = [version_id]

    if action == "list_object_versions":
        if variables is not None and 'object_name' in variables:
            obj_name = variables['object_name']
        else:
            obj_name = global_variables['object_name']
        key_deleted_index = obj_name + '_deleted_versions'
        key_versions_index = obj_name + '_versions_v2'
        # flag
        deleted_obj_vl = actual_response.get('DeleteMarkers')
        obj_vl = actual_response.get('Versions')

        if obj_vl:
            for item in range(0, len(obj_vl)):
                version_id = obj_vl[item].get('VersionId')
                if key_versions_index in global_variables.keys():
                    if version_id not in global_variables[key_versions_index]:
                        global_variables[key_versions_index].append(version_id)
                else:
                    global_variables[key_versions_index] = [version_id]

            if deleted_obj_vl:
                for item in range(0, len(deleted_obj_vl)):
                    deleted_version_id = deleted_obj_vl[item].get('VersionId')
                    if key_deleted_index in global_variables.keys():
                        global_variables[key_deleted_index].append(deleted_version_id)
                    else:
                        global_variables[key_deleted_index] = [deleted_version_id]

    return global_variables


if __name__ == '__main__':
    pass
