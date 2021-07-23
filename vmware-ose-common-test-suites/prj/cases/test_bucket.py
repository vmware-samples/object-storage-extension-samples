# -*- coding:utf-8 -*-

from framework.addons.UnitTi import data_provider, group
from framework.core.Base import Base
from framework.libs.common.utils import get_group_list, get_doc_string_list
from prj.test_data.test_bucket.test_bucket import *


class TestBucket(Base):
    @classmethod
    def setUpClass(cls):
        cls.initialize()
        pass

    def setUp(self):
        pass

    prov = test_create_bucket_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('create_bucket', append=True)
    @data_provider(provider=test_create_bucket_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test01_test_create_bucket(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_analytics_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket_analytics_configuration', append=True)
    @data_provider(provider=test_delete_bucket_analytics_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test02_test_delete_bucket_analytics_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_cors_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket_cors', append=True)
    @data_provider(provider=test_delete_bucket_cors_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test03_test_delete_bucket_cors(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_encryption_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('delete_bucket_encryption', append=True)
    @data_provider(provider=test_delete_bucket_encryption_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test04_test_delete_bucket_encryption(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_lifecycle_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket_lifecycle', append=True)
    @data_provider(provider=test_delete_bucket_lifecycle_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test06_test_delete_bucket_lifecycle(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_policy_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket_policy', append=True)
    @data_provider(provider=test_delete_bucket_policy_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test08_test_delete_bucket_policy(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket', append=True)
    @data_provider(provider=test_delete_bucket_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test09_test_delete_bucket(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_delete_bucket_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('delete_bucket_tagging', append=True)
    @data_provider(provider=test_delete_bucket_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test11_test_delete_bucket_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_acl', append=True)
    @data_provider(provider=test_get_bucket_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test14_test_get_bucket_acl(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_analytics_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_analytics_configuration', append=True)
    @data_provider(provider=test_get_bucket_analytics_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test15_test_get_bucket_analytics_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_cors_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_cors', append=True)
    @data_provider(provider=test_get_bucket_cors_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test16_test_get_bucket_cors(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_encryption_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('get_bucket_encryption', append=True)
    @data_provider(provider=test_get_bucket_encryption_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test17_test_get_bucket_encryption(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_lifecycle_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('get_bucket_lifecycle_configuration', append=True)
    @data_provider(provider=test_get_bucket_lifecycle_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test19_test_get_bucket_lifecycle_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    # prov = test_get_bucket_lifecycle_provider()
    # doc_l = get_doc_string_list(prov)
    # g_l = get_group_list(prov)
    #
    # # @unittest.skip("skip")
    # @data_provider(provider=test_get_bucket_lifecycle_provider,
    #                docstring_list=doc_l,
    #                group_list=g_l)
    # def test20_test_get_bucket_lifecycle(self, testdata):
    #     self.generic_s3_test_process(testdata)
    prov = test_get_bucket_location_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('get_bucket_location', append=True)
    @data_provider(provider=test_get_bucket_location_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test21_test_get_bucket_location(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_logging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    # @unittest.skip("skip")
    @group('get_bucket_logging', append=True)
    @data_provider(provider=test_get_bucket_logging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test22_test_get_bucket_logging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_policy_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_policy', append=True)
    @data_provider(provider=test_get_bucket_policy_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test26_test_get_bucket_policy(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_policy_status_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_policy_status', append=True)
    @data_provider(provider=test_get_bucket_policy_status_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test27_test_get_bucket_policy_status(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_tagging', append=True)
    @data_provider(provider=test_get_bucket_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test29_test_get_bucket_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_get_bucket_versioning_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('get_bucket_versioning', append=True)
    @data_provider(provider=test_get_bucket_versioning_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test30_test_get_bucket_versioning(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_head_bucket_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('head_bucket', append=True)
    @data_provider(provider=test_head_bucket_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test32_test_head_bucket(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_bucket_analytics_configurations_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('list_bucket_analytics_configurations', append=True)
    @data_provider(provider=test_list_bucket_analytics_configurations_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test33_test_list_bucket_analytics_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_list_buckets_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('list_buckets', append=True)
    @data_provider(provider=test_list_buckets_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test36_test_list_buckets(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_acl', append=True)
    @data_provider(provider=test_put_bucket_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test38_test_put_bucket_acl(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_analytics_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_analytics_configuration', append=True)
    @data_provider(provider=test_put_bucket_analytics_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test39_test_put_bucket_analytics_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_cors_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_cors', append=True)
    @data_provider(provider=test_put_bucket_cors_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test40_test_put_bucket_cors(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_encryption_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_encryption', append=True)
    @data_provider(provider=test_put_bucket_encryption_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test41_test_put_bucket_encryption(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_lifecycle_configuration_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_lifecycle_configuration', append=True)
    @data_provider(provider=test_put_bucket_lifecycle_configuration_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test43_test_put_bucket_lifecycle_configuration(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_logging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_logging', append=True)
    @data_provider(provider=test_put_bucket_logging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test45_test_put_bucket_logging(self, testdata):
        self.generic_s3_test_process(testdata)

    # prov = test_put_bucket_lifecycle_provider()
    # doc_l = get_doc_string_list(prov)
    # g_l = get_group_list(prov)
    #
    # # @unittest.skip("skip")
    # @data_provider(provider=test_put_bucket_lifecycle_provider,
    #                docstring_list=doc_l,
    #                group_list=g_l)
    # def test44_test_put_bucket_lifecycle(self, testdata):
    #     self.generic_s3_test_process(testdata)

    prov = test_put_bucket_policy_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_policy', append=True)
    @data_provider(provider=test_put_bucket_policy_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test50_test_put_bucket_policy(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_tagging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_logging', append=True)
    @data_provider(provider=test_put_bucket_tagging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test52_test_put_bucket_tagging(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_put_bucket_versioning_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    @group('put_bucket_versioning', append=True)
    @data_provider(provider=test_put_bucket_versioning_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test53_test_put_bucket_versioning(self, testdata):
        self.generic_s3_test_process(testdata)

    '''
    prov = test_bucket_acl_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    #@unittest.skip("skip")
    @data_provider(provider=test_bucket_acl_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test04_test_bucket_acl(self, testdata):
        self.generic_s3_test_process(testdata)

    prov = test_bucket_logging_provider()
    doc_l = get_doc_string_list(prov)
    g_l = get_group_list(prov)

    #@unittest.skip("skip")
    @data_provider(provider=test_bucket_logging_provider,
                   docstring_list=doc_l,
                   group_list=g_l)
    def test05_test_bucket_logging(self, testdata):
        self.generic_s3_test_process(testdata)
    '''

    def tearDown(self):
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        pass
