# -*- coding:utf-8 -*-

from framework.addons.UnitTi import data_provider, group
from framework.core.Base import Base
from framework.libs.common.utils import get_group_list, get_doc_string_list
from prj.test_data.test_object.test_object import *


class TestObject(Base):
    @classmethod
    def setUpClass(cls):
        cls.initialize()
        pass

    def setUp(self):
        pass

    prov = test_copy_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('copy_object', append=True)
    @data_provider(provider=test_copy_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test01_test_copy_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_delete_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test02_test_delete_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_object_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_object_tagging', append=True)
    @data_provider(provider=test_delete_object_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test03_test_delete_object_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_objects_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_delete_objects_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test04_test_delete_objects(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_get_object_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test05_test_get_object_acl(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_legal_hold_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_object_legal_hold', append=True)
    @data_provider(provider=test_get_object_legal_hold_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test06_get_object_legal_hold(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_lock_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_object_lock_configuration', append=True)
    @data_provider(provider=test_get_object_lock_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test07_get_object_lock_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_get_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test08_get_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_retention_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_object_retention', append=True)
    @data_provider(provider=test_get_object_retention_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test09_get_object_retention(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_object_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_object_tagging', append=True)
    @data_provider(provider=test_get_object_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test10_get_object_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_head_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('head_object', append=True)
    @data_provider(provider=test_head_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test12_test_head_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_objects_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('list_objects', append=True)
    @data_provider(provider=test_list_objects_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test14_test_list_objects(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_object_versions_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('list_object_versions', append=True)
    @data_provider(provider=test_list_object_versions_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test13_test_list_object_versions(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_objects_v2_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('list_objects_v2', append=True)
    @data_provider(provider=test_list_objects_v2_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test15_test_list_objects_v2(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_object_acl', append=True)
    @data_provider(provider=test_put_object_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test16_test_put_object_acl(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_legal_hold_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_put_object_legal_hold_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test17_put_object_legal_hold(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_lock_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_object_lock_configuration', append=True)
    @data_provider(provider=test_put_object_lock_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test18_put_object_lock_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_object', append=True)
    @data_provider(provider=test_put_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test19_test_put_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_retention_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_object_retention', append=True)
    @data_provider(provider=test_put_object_retention_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test20_put_object_retention(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_object_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_object_tagging', append=True)
    @data_provider(provider=test_put_object_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test21_put_object_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    '''
    prov = test_curd_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    prov = test_curd_object_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    #@unittest.skip("skip")
    @data_provider(provider=test_curd_object_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test_curd_object(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_multipart_upload_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @data_provider(provider=test_multipart_upload_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test_multipart_upload(self, testdata):
        self.generic_s3_test_process(testdata, "S3CompatibleAPI", "multipart_upload")

    prov = test_object_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    #@unittest.skip("skip")
    @data_provider(provider=test_object_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test_object_acl(self, testdata):
        self.generic_s3_test_process(testdata, "S3CompatibleAPI", "put_object_acl")
        
    '''
    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        pass
