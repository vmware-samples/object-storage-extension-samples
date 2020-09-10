from framework.libs.common.utils import load_csv
import os

def test_curd_object_provider():
    f_name = "test_crud_object_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_list_object_provider():
    f_name = "test_list_objects_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_copy_object_provider():
    f_name = "test_copy_object_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_delete_objects_provider():
    f_name = "test_delete_objects_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_multipart_upload_provider():
    f_name = "test_multipart_upload_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_object_acl_provider():
    f_name = "test_object_acl.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

def test_object_tagging_provider():
    f_name = "test_object_tagging.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))

if __name__ == "__main__":
    pass
