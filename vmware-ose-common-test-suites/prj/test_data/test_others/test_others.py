from framework.libs.common.utils import load_csv
import os


# multipart upload
def test_abort_multipart_upload_provider():
    f_name = "test_abort_multipart_upload_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_complete_multipart_upload_provider():
    f_name = "test_complete_multipart_upload_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_create_multipart_upload_provider():
    f_name = "test_create_multipart_upload_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_list_multipart_uploads_provider():
    f_name = "test_list_multipart_uploads_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_list_parts_provider():
    f_name = "test_list_parts_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_upload_part_copy_provider():
    f_name = "test_upload_part_copy_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_upload_part_provider():
    f_name = "test_upload_part_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# public access block
def test_delete_public_access_block_provider():
    f_name = "test_delete_public_access_block_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_get_public_access_block_provider():
    f_name = "test_get_public_access_block_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


def test_put_public_access_block_provider():
    f_name = "test_put_public_access_block_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


# restore
def test_restore_provider():
    f_name = "test_restore_prov.csv"
    folder = os.path.dirname(__file__)
    return load_csv(os.path.join(folder, f_name))


if __name__ == "__main__":
    pass
