# -*- coding:utf-8 -*-

from framework.addons.UnitTi import data_provider, group
from framework.core.Base import Base
from framework.libs.common.utils import get_group_list, get_doc_string_list
from prj.test_data.test_others.test_others import *


class TestOthers(Base):
    @classmethod
    def setUpClass(cls):
        cls.initialize()
        pass

    def setUp(self):
        pass

    prov = test_abort_multipart_upload_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('Multipart', append=True)
    @data_provider(provider=test_abort_multipart_upload_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test01_test_abort_multipart_upload(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_complete_multipart_upload_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('Multipart', append=True)
    @data_provider(provider=test_complete_multipart_upload_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test02_test_complete_multipart_upload(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_create_multipart_upload_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('Multipart', append=True)
    @data_provider(provider=test_create_multipart_upload_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test03_test_create_multipart_upload(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_public_access_block_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_public_access_block', append=True)
    @data_provider(provider=test_delete_public_access_block_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test04_test_delete_public_access_block(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_public_access_block_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_public_access_block', append=True)
    @data_provider(provider=test_get_public_access_block_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test05_test_get_public_access_block(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_multipart_uploads_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('Multipart', append=True)
    @data_provider(provider=test_list_multipart_uploads_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test06_test_list_multipart_uploads(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_parts_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('Multipart', append=True)
    @data_provider(provider=test_list_parts_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test07_test_list_parts(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_public_access_block_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_public_access_block', append=True)
    @data_provider(provider=test_put_public_access_block_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test08_test_put_public_access_block(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_upload_part_copy_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('upload_part_copy', append=True)
    @data_provider(provider=test_upload_part_copy_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test10_test_upload_part_copy(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_upload_part_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('upload_part', append=True)
    @data_provider(provider=test_upload_part_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test11_test_upload_part(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_restore_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('test_restore', append=True)
    @data_provider(provider=test_restore_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test09_test_restore(self, testdata):
        self.generic_s3_test_process(testdata)

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        pass
