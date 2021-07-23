import os

from framework.addons.UnitTi import UtiTestLoader

from prj.cases.test_bucket import TestBucket
from prj.cases.test_object import TestObject
from prj.cases.test_others import TestOthers


class SuiteManagement:
    """
    # 1. suites policy
    # 2. suites / cases management
    # 3. scope filter control
    #
    """

    def __init__(self, config_profile):
        self.config_profile = config_profile
        self.suites_o = SuiteManagement.get_suites_list(self.config_profile.get('scope'))
        self.excludes = SuiteList.get_case_excludes(self.config_profile.get('scope'),
                                                          self.config_profile)
        self.pri_o = SuiteManagement.get_case_priority(self.config_profile.get('priority'))

        self.includes = []
        if 'testcases' in self.config_profile and self.config_profile.get('testcases'):
            self.includes.extend(self.config_profile.get('testcases'))
        else:
            self.includes.extend(self.pri_o)
        return

    @staticmethod
    def get_suites_list(scope):
        return SuiteList.get_suites(scope)

    @staticmethod
    def get_case_priority(priority):
        smoke_priority = ['P0']
        regression_priority = ['P0', 'P1']
        quick_priority = ['P1']
        full_priority = ['P0', 'P1', 'P2']

        if priority == 'smoke':
            pri_o = smoke_priority
        elif priority == 'quick':
            pri_o = quick_priority
        elif priority == 'regression':
            pri_o = regression_priority
        elif priority == 'full':
            pri_o = full_priority
        else:
            pri_o = smoke_priority
        return pri_o

    def get_parallel_suites(self):
        loader = UtiTestLoader()
        parallel_suites = []
        print("<----- Test Step: test suite info. ----->")

        for a_sui in self.suites_o:
            suite_l = loader.load_tests_from_classes(*[a_sui], include=self.includes, exclude=self.excludes)
            parallel_suites.append(suite_l)

        return parallel_suites


class SuiteList:
    full_suites = [TestBucket, TestObject, TestOthers]

    @staticmethod
    def get_suites(scope):
        if scope == 'FULL':
            return SuiteList.full_suites

        return SuiteList.full_suites

    @staticmethod
    def get_case_excludes(scope, config_profile):
        try:
            excludes = config_profile.get('case_scope').get(scope).get('excludes')
            return excludes
        except AttributeError:
            return []


if __name__ == '__main__':
    pass
