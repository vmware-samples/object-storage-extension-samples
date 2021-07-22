from framework.libs.common.utils import load_csv
import os


def test_create_bucket_provider():
    f_name = "test_create_bucket_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_location_provider():
    f_name = "test_get_bucket_location_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_head_bucket_provider():
    f_name = "test_head_bucket_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_provider():
    f_name = "test_delete_bucket_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# acl
def test_put_bucket_acl_provider():
    f_name = "test_put_bucket_acl_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_acl_provider():
    f_name = "test_get_bucket_acl_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_tagging_provider():
    f_name = "test_put_bucket_tagging_prov.csv"
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

#tagging
def test_get_bucket_tagging_provider():
    f_name = "test_get_bucket_tagging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_tagging_provider():
    f_name = "test_put_bucket_tagging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_tagging_provider():
    f_name = "test_delete_bucket_tagging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# enc
def test_get_bucket_encryption_provider():
    f_name = "test_get_bucket_encryption_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_encryption_provider():
    f_name = "test_delete_bucket_encryption_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_encryption_provider():
    f_name = "test_put_bucket_encryption_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# lifecycle
def test_get_bucket_lifecycle_provider():
    f_name = "test_get_bucket_lifecycle_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_lifecycle_provider():
    f_name = "test_delete_bucket_lifecycle_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_lifecycle_provider():
    f_name = "test_put_bucket_lifecycle_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_lifecycle_configuration_provider():
    f_name = "test_get_bucket_lifecycle_configuration_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_lifecycle_configuration_provider():
    f_name = "test_put_bucket_lifecycle_configuration_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# policy
def test_get_bucket_policy_provider():
    f_name = "test_get_bucket_policy_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_policy_status_provider():
    f_name = "test_get_bucket_policy_status_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_policy_provider():
    f_name = "test_delete_bucket_policy_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_policy_provider():
    f_name = "test_put_bucket_policy_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# logging
def test_put_bucket_logging_provider():
    f_name = "test_put_bucket_logging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_logging_provider():
    f_name = "test_get_bucket_logging_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# versioning
def test_put_bucket_versioning_provider():
    f_name = "test_put_bucket_versioning_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_bucket_versioning_provider():
    f_name = "test_get_bucket_versioning_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# cors
def test_get_bucket_cors_provider():
    f_name = "test_get_bucket_cors_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_cors_provider():
    f_name = "test_put_bucket_cors_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_cors_provider():
    f_name = "test_delete_bucket_cors_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# bucket_analytics_configuration
def test_get_bucket_analytics_configuration_provider():
    f_name = "test_get_bucket_analytics_configuration_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_bucket_analytics_configuration_provider():
    f_name = "test_put_bucket_analytics_configuration_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_delete_bucket_analytics_configuration_provider():
    f_name = "test_delete_bucket_analytics_configuration_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_list_bucket_analytics_configurations_provider():
    f_name = "test_list_bucket_analytics_configurations_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


if __name__ == "__main__":
    pass


