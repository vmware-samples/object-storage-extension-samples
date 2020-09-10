from framework.libs.common.utils import load_csv
import os


def test_bucket_crud_provider():
    f_name = "test_bucket_crud_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_bucket_tagging_provider():
    f_name = "test_bucket_tagging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_list_buckets_provider():
    f_name = "test_list_buckets_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_bucket_acl_provider():
    f_name = "test_bucket_acl_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_bucket_logging_provider():
    f_name = "test_bucket_logging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


if __name__ == "__main__":
    pass


