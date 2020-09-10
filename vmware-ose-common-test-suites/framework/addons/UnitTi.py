import io
import os
import re
import sys
import copy
import importlib
import inspect
import unittest
import traceback
import threading
import functools
from unittest import suite
from unittest import SkipTest
from functools import wraps
from collections import defaultdict
from unittest.suite import TestSuite
from unittest.suite import _isnotsuite
from concurrent.futures import ThreadPoolExecutor, wait
from framework.libs.common.utils import update_csv


# refine this class
class DP:
    def __init__(self):
        self.dependency = defaultdict(list)
        self.visited = defaultdict(lambda: -1)
        self.res = []
        self.started = set()

    def add_dependency(self, a, b):
        self.dependency[b].append(a)
        if a not in self.dependency:
            self.dependency[a] = [None]

    def get_available_items(self):
        dp_items = set()
        for k, v in self.dependency.items():
            dp_items |= set(v)
        return [k for k, v in self.dependency.items() if k not in dp_items and k not in self.started]

    def start_item(self, x):
        self.started.add(x)

    def get_started_item_num(self):
        return len(self.started)

    def remove_item(self, x):
        self.dependency.pop(x, None)

    def sort_items(self):
        tests = set([x for x in self.dependency if x is not None])
        for test in tests:
            if self.visited[test] == -1:
                self.sort_helper(test)
        return self.res

    def sort_helper(self, a):
        self.visited[a] = 0
        for b in self.dependency[a]:
            if not b:
                continue
            if self.visited[b] == 0:
                raise ValueError('Cyclic dependency <{}> detected'.format(b))
            if self.visited[b] == -1:
                self.sort_helper(b)

        self.res.insert(0, a)
        self.visited[a] = 1


def _sort_tests(cls, test_list):
    dp = DP()
    test_set = set(test_list)
    for curr_test in test_list:
        func = getattr(cls, curr_test)
        dependency_list = getattr(func, '_depends_on_fn', [])

        for dp_test in dependency_list:
            if dp_test not in test_set:
                found = False
                for t in test_list:
                    # actual time complexity is O(m*n) in the worst case
                    if re.match(dp_test+'$', t):
                        found = True
                        dp.add_dependency(curr_test, t)
                        _append_to_list_attr(func, '_depends_on_fn', t)
                if not found:
                    raise ValueError(
                        'Cannot find dependency <{}>: test does not exist or is filtered out'.format(dp_test))
            else:
                dp.add_dependency(curr_test, dp_test)

    cls.dp_graph = dp
    dependent_tests = dp.sort_items()
    cls.dp_tests = dependent_tests
    other_tests = list(filter(lambda x: x not in dependent_tests, test_list))
    cls.other_tests = other_tests
    return dependent_tests + other_tests


def _sort_classes(class_list):
    dp = DP()
    class_map = defaultdict(list)
    for cls in class_list:
        class_map[cls.__name__].append(cls)

    for cls in class_list:
        dependencies = getattr(cls, '_depends_on_cls', [])
        for d in dependencies:
            if d not in class_map:
                raise ValueError('Cannot find dependency <{}>: class does not exist or is filtered out'.format(d))
            for x in class_map[d]:
                dp.add_dependency(cls, x)

    dependent_classes = dp.sort_items()
    return dependent_classes + list(filter(lambda u: u not in dependent_classes, class_list))


def _data_provider_wrapper(func, docstring, *args):
    @wraps(func)
    def wrapper(self):
        return func(self, *args)
    wrapper.__doc__ = docstring
    return wrapper


def _data_provider_exc_wrapper(func, exception):
    @wraps(func)
    def wrapper(self):
        raise exception
    return wrapper


def _process_group(test_case_class, test_case_names, include, exclude):
    test_case_class.group_map = defaultdict(list)
    class_group = getattr(test_case_class, '_group', [])
    f_override = getattr(test_case_class, '_override', True if class_group else False)
    f_append = getattr(test_case_class, '_append', False)

    if f_override:
        for test in test_case_names:
            test_case_class.group_map[test] = class_group
    else:
        for test in test_case_names:
            func = getattr(test_case_class, test)
            if f_append:
                test_groups = getattr(func, '_group', []) + class_group
            else:
                test_groups = getattr(func, '_group', class_group)
            test_case_class.group_map[test] = test_groups or ['Ungrouped']

    include = set(include)
    exclude = set(exclude)

    if include & exclude:
        raise ValueError('Include and exclude groups conflict: ' + ''.join(include & exclude))
    if include or exclude:
        if f_override:
            if not set(class_group) & include or set(class_group) & exclude:
                return []
        else:
            ret = []
            for t in test_case_names:
                func = getattr(test_case_class, t)
                if f_append:
                    test_groups = getattr(func, '_group', []) + class_group
                else:
                    test_groups = getattr(func, '_group', class_group)
                g = set(test_groups)

                # if g & include and not g & exclude:
                if g & include and not __validate_exclude(g, exclude):
                    ret.append(t)
            return ret
    return test_case_names


def __validate_exclude(g, exclude):
    #  return true if exclude is in set g
    g_str = ''.join(g).upper()
    for _item in exclude:
        if _item.upper() in g_str:
            return True
    return False


def _process_data_provider(test_case_class, test_case_names):
    ret = []
    for test_name in test_case_names:
        test_method = getattr(test_case_class, test_name)
        if getattr(test_method, '_derived', False):
            continue
        provider = getattr(test_method, '_provider', None)
        if provider:
            provider_func = provider.__func__ if type(provider) == staticmethod else provider
            try:
                test_data, f_path = provider_func()
            except Exception as e:
                setattr(test_case_class, test_name, _data_provider_exc_wrapper(test_method, e))
                ret.append(test_name)
                continue

            doc_list = getattr(test_method, '_doc_list', None)
            group_list = getattr(test_method, '_group_list', None)
            info_list = getattr(test_method, '_info_list', None)
            data_size = len(test_data)
            # refine this...
            if not doc_list:
                doc_list = [None] * data_size
            if len(doc_list) != data_size:
                raise ValueError('length of docstring list %s does not match test data size %s.' % (
                    str(len(doc_list)), str(data_size)))
            if not group_list:
                group_list = [None] * data_size
            if len(group_list) != data_size:
                raise ValueError('length of group list does not match test data size, %s:%s' % (
                    str(len(group_list)), str(data_size)))
            if not info_list:
                info_list = [None] * data_size
            if len(info_list) != data_size:
                raise ValueError('length of info list does not match test data size')

            provider_test_name_prefix = '{0}#{1}'.format(test_case_class.__name__, test_name)
            need_update_csv = True
            for i, (x, y, z, w) in enumerate(zip(test_data, doc_list, group_list, info_list)):
                # provider_test_name = '{0}_{1}'.format(test_name, i+1)
                if 'TCID' in test_data[i][0]:
                    provider_test_name = test_data[i][0]['TCID']
                    if provider_test_name.startswith(provider_test_name_prefix):
                        naming = provider_test_name.split('#')
                        if len(naming) == 3:
                            if naming[2].isdigit():
                                need_update_csv = False

                    if need_update_csv:
                        provider_test_name = '{0}#{1}#{2}'.format(
                            test_case_class.__name__,
                            test_name,
                            i + 2)

                        # time.strftime('%Y-%m-%d-%H_%M_%S'),

                        test_data[i][0]['TCID'] = provider_test_name
                        update_csv(test_data, f_path)
                else:
                    # TODO; add one TCID column?
                    provider_test_name = '{0}#{1}#{2}'.format(
                            test_case_class.__name__,
                            test_name,
                            i + 2)

                docstring = y if y else test_method.__doc__
                setattr(test_case_class, provider_test_name, _data_provider_wrapper(test_method, docstring, *x))
                new_func = getattr(test_case_class, provider_test_name)
                new_func._derived = True
                new_func._derived_by = test_method.__name__
                if z:
                    if hasattr(new_func, '_group'):
                        new_func._group = list(set(new_func._group + z))
                    else:
                        new_func._group = z
                if w:
                    new_func.info = getattr(test_method, 'info', {}).copy()
                    new_func.info.update(w)
                ret.append(provider_test_name)
        else:
            ret.append(test_name)

    return ret


def _append_to_list_attr(o, name, *args):
    args = list(args)
    getattr(o, name).extend(args) if hasattr(o, name) else setattr(o, name, args)


def _compare_test_by_ln(test_class, test_name_1, test_name_2):
    x = getattr(test_class, test_name_1).__code__.co_firstlineno
    y = getattr(test_class, test_name_2).__code__.co_firstlineno
    return (x > y) - (x < y)


class UtiTestLoader(unittest.TestLoader):
    # brute force recursive import
    # has issue with files having a same name
    @staticmethod
    def find_ut_classes_by_path(path, import_path='', level=1):
        ret = []
        if level == 0:
            return ret

        for f in os.listdir(os.path.abspath(path)):
            if f.startswith('_'):
                continue
            current_path = os.path.join(path, f)

            # python module
            if os.path.isfile(current_path) and f.endswith('.py'):
                sys.path.append(path)
                module = importlib.import_module(import_path + os.path.splitext(f)[0])
                for tp in inspect.getmembers(module, inspect.isclass):
                    if issubclass(tp[1], unittest.TestCase):
                        ret.append(tp[1])
            # directory
            elif os.path.isdir(current_path):
                ret += UtiTestLoader.find_ut_classes_by_path(current_path, import_path+f+'.', level-1)

        return ret

    def load_tests_from_module(self, module, include=(), exclude=(), stage=None):
        classes = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                classes.append(obj)
        return self.load_tests_from_classes(*classes, include=include, exclude=exclude, stage=stage)

    def load_tests_from_classes(self, *test_case_classes, include=(), exclude=(), stage=None):
        suites = []
        suite_class = ParallelTestSuite
        sorting_method = self.sortTestMethodsUsing
        test_case_classes = _sort_classes(test_case_classes)
        temp_stage = None
        for test_case_class in test_case_classes:
            if issubclass(test_case_class, suite.TestSuite):
                raise TypeError('Test cases should not be derived from TestSuite')

            s = getattr(test_case_class, '_stage', None)
            if s is not None:
                if temp_stage is None:
                    temp_stage = s
                elif temp_stage != s:
                    raise ValueError('Classes to be loaded into one suite shall have same stage number')

            if getattr(test_case_class, '_fdfe', False):
                stream = io.StringIO(inspect.getsource(test_case_class))
                stream.readline()
                exec('class UnitTiTempLoading:\n' + ''.join([x for x in stream if not x.strip().startswith('@')]))
                self.sortTestMethodsUsing = functools.partial(_compare_test_by_ln, eval('UnitTiTempLoading'))

            test_case_names = self.getTestCaseNames(test_case_class)
            self.sortTestMethodsUsing = sorting_method
            if not test_case_names and hasattr(test_case_class, 'runTest'):
                test_case_names = ['runTest']

            test_case_names = _process_data_provider(test_case_class, test_case_names)
            test_case_names = _process_group(test_case_class, test_case_names, include, exclude)

            test_case_names = _sort_tests(test_case_class, test_case_names)
            test_case_class._in_order = True

            pool_size = getattr(test_case_class, 'pool_size', None)
            if pool_size is not None and pool_size == 0:
                test_case_class.pool_size = len(test_case_names)

            retry_times = getattr(test_case_class, '_retry', 0)
            if retry_times:
                for test_name in test_case_names:
                    setattr(test_case_class, test_name, retry(retry_times)(getattr(test_case_class, test_name)))

            if test_case_names:
                suites.append(suite_class(map(test_case_class, test_case_names)))

        if temp_stage is None:
            x = stage
        elif stage is not None:
            assert stage == temp_stage, 'Stage set in class is different with parameter'
            x = temp_stage
        else:
            x = temp_stage
        ret = suite_class(suites)
        if x is not None:
            ret._stage = x
        return ret


# for class decoration
def _stage(stage):
    def decorator(cls):
        cls._stage = stage
        return cls
    return decorator


# for member function or class decoration
def group(*groups, override=True, append=False):
    def decorator(obj):
        if type(obj).__name__ == 'function':
            @wraps(obj)
            def wrapper(*args, **kwargs):
                obj(*args, **kwargs)
            _append_to_list_attr(wrapper, '_group', *groups)
            return wrapper
        else:
            _append_to_list_attr(obj, '_group', *groups)
            obj._override = override
            obj._append = append
            return obj
    return decorator


def _check_method_dep(cls, result_list, status, *dependency_list):
    for x in result_list:
        dependent_test = getattr(x[0], '_testMethodName')
        if type(x[0]) == type(cls) and dependent_test in dependency_list:
            cls.skipTest('Skip as dependent test <{0}> {1}'.format(dependent_test, status))


def _check_cls_dep(cls, result_list, status, *dependency_list):
    for x in result_list:
        class_name = type(x[0]).__name__
        if class_name == '_ErrorHolder':
            class_name = x[0].description.split('.')[-1][:-1]
        if class_name in dependency_list:
            method_name = getattr(x[0], '_testMethodName', None)
            if not method_name:
                method_name = x[0].description.split()[0]
            cls.skipTest('Skip as test <{0}> in dependent class <{1}> {2}'.format(method_name, class_name, status))


def _check_ff(cls, result_list):
    if result_list and type(result_list[-1][0]).__name__ == type(cls).__name__:
        cls.skipTest('Skip remaining tests as fast fail is enabled')


# for member function decoration
# refine this like style of data provider decorator
def depends_on_method(*func_names, hard_dependency=True):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(self, '_in_order', False) and hard_dependency:
                dp_list = getattr(wrapper, '_depends_on_fn')
                _check_method_dep(self, self._outcome.result.failures, 'failed', *dp_list)
                _check_method_dep(self, self._outcome.result.errors, 'error', *dp_list)
                _check_method_dep(self, self._outcome.result.skipped, 'skipped', *dp_list)
            return func(self, *args, **kwargs)
        _append_to_list_attr(wrapper, '_depends_on_fn', *func_names)
        return wrapper
    return decorator


# setUp wrapper to solve class dependency
def _dep_setup_wrapper(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if getattr(self, '_in_order', False):
            dependency_list = getattr(self, '_depends_on_cls')
            _check_cls_dep(self, self._outcome.result.failures, 'failed', *dependency_list)
            _check_cls_dep(self, self._outcome.result.errors, 'error', *dependency_list)
            _check_cls_dep(self, self._outcome.result.skipped, 'skipped', *dependency_list)
        return func(self, *args, **kwargs)
    return wrapper


# setUp wrapper to implement fast fail
def _ff_setup_wrapper(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        _check_ff(self, self._outcome.result.failures)
        _check_ff(self, self._outcome.result.errors)
        _check_ff(self, self._outcome.result.skipped)
        func(self, *args, **kwargs)
    return wrapper


# setUp wrapper to handle setUpClass error
def _stp_cls_err_wrapper(self):
    raise RuntimeError('setUpClass failed')


# for class decoration
def depends_on_class(*class_names):
    def decorator(cls):
        if type(cls).__name__ == 'type':
            cls.setUp = _dep_setup_wrapper(cls.setUp)
            _append_to_list_attr(cls, '_depends_on_cls', *class_names)
        return cls
    return decorator


# for class decoration, do not use this on parallel execution
def fast_fail(cls):
    if type(cls).__name__ == 'type':
        cls.setUp = _ff_setup_wrapper(cls.setUp)
    return cls


# for non-member function decoration
def data_provider(provider, docstring_list=None, group_list=None, info_list=None):
    def decorator(func):
        try:
            class_name = func.__qualname__.split(".")[0]
            for item in group_list:
                item.append(class_name)
        except:
            pass
        func._provider = provider
        func._doc_list = docstring_list
        func._group_list = group_list
        func._info_list = info_list
        return func
    return decorator


# for class decoration
def first_def_first_exec(cls):
    cls._fdfe = True
    return cls


# for function decoration
def retry(times):
    times = 0 if times < 0 else times

    def decorator(obj):
        if type(obj).__name__ != 'function':
            obj._retry = times
            return obj
        else:
            @wraps(obj)
            def wrapper(*args, **kwargs):
                exception = None
                for i in range(times+1):
                    try:
                        obj(*args, **kwargs)
                        break
                    except Exception as ex:
                        if type(ex) == SkipTest:
                            raise ex
                        traceback.print_exc()
                        exception = ex
                else:
                    sys.stderr.write('Retry times limit exceeded. Raise the exception...\n')
                    raise exception
            return wrapper
    return decorator


def parallel_tests(*args, **kwargs):
    if args:
        args[0].f_parallel = True
        args[0].pool_size = 4
        return args[0]
    else:
        def decorator(cls):
            cls.f_parallel = True
            cls.pool_size = kwargs['pool_size']
            return cls
        return decorator


def info(**kwargs):
    def decorator(func):
        func.info = kwargs
        return func
    return decorator


class ParallelTestSuite(TestSuite):
    thread_test_map = defaultdict(list)
    # refine the recursion of test info collection. put it to somewhere else

    def is_empty(self):
        return True if not self._tests else False

    def info(self):
        ret = []
        self.info_helper(ret)
        return ret

    def info_helper(self, test_info):
        for test in self:
            if _isnotsuite(test):
                func_name = test._testMethodName
                func_doc = test._testMethodDoc
                func = getattr(test.__class__, func_name)
                if not hasattr(func, 'info'):
                    continue
                elem = {
                    'name': func_name,
                    'real_name': getattr(func, '_derived_by', func_name),
                    'docstring': func_doc,
                    'groups': ', '.join(getattr(func, '_group', test.group_map.get(func_name, [])))
                }
                elem.update(getattr(func, 'info'))
                test_info.append(elem)
            else:
                test.info_helper(test_info)

    def run(self, result, debug=False):
        top_level = False
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = top_level = True

        for index, test in enumerate(self):
            if result.shouldStop:
                break
            if _isnotsuite(test):
                ParallelTestSuite._run_threads(test, result)
                self._tearDownPreviousClass(test, result)
                self._handleModuleFixture(test, result)
                self._handleClassSetUp(test, result)

                result._previousTestClass = test.__class__
                # if (getattr(test.__class__, '_classSetupFailed', False) or
                #         getattr(result, '_moduleSetUpFailed', False)):
                #     continue
                if getattr(test.__class__, '_classSetupFailed', False):
                    test.__class__.setUp = _stp_cls_err_wrapper
                if getattr(result, '_moduleSetUpFailed', False):
                    continue
                if getattr(test.__class__, 'f_parallel', None):
                    ParallelTestSuite.thread_test_map[threading.get_ident()].append(test)
                else:
                    test(result)
            else:
                test(result)

            if self._cleanup:
                self._removeTestAtIndex(index)

        if top_level:
            ParallelTestSuite._run_threads(None, result)
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False

        return result

    # refine this method
    @staticmethod
    def _run_threads(test, result):
        tid = threading.get_ident()
        if test.__class__ == getattr(result, '_previousTestClass', None) or not ParallelTestSuite.thread_test_map[tid]:
            return

        k = len(ParallelTestSuite.thread_test_map[tid])
        while k > 0:
            events = {}
            futures = []
            lock = threading.Lock()

            cls = ParallelTestSuite.thread_test_map[tid][0].__class__
            pool = ThreadPoolExecutor(cls.pool_size)
            dp_graph = copy.deepcopy(getattr(cls, 'dp_graph', None))
            dp_tests = getattr(cls, 'dp_tests', None)
            other_tests = getattr(cls, 'other_tests', None)

            def _dp_callback(*args):
                with lock:
                    tested.add(test_map[args[0]])
                    dp_graph.remove_item(args[0])
                    events[args[0]].set()
                if dp_graph.get_started_item_num() == len(dp_tests):
                    return
                _available_tests = dp_graph.get_available_items()
                for a in _available_tests:
                    if a not in dp_graph.started:
                        dp_graph.start_item(a)
                        fn = pool.submit(test_map[a], result)
                        fn.add_done_callback(functools.partial(_dp_callback, a))

            def _non_dp_callback(*args):
                with lock:
                    tested.add(test_map[args[0]])
                    events[args[0]].set()

            if not dp_tests:
                for t in ParallelTestSuite.thread_test_map[tid]:
                    futures.append(pool.submit(t, result))
                wait(futures)
                break

            else:
                test_map = {}
                tested = set()
                for t in ParallelTestSuite.thread_test_map[tid]:
                    events[t._testMethodName] = threading.Event()
                    test_map[t._testMethodName] = t

                for t in other_tests:
                    tested.add(test_map[t])
                    f = pool.submit(test_map[t], result)
                    f.add_done_callback(functools.partial(_non_dp_callback, t))

                available_tests = dp_graph.get_available_items()
                for t in available_tests:
                    tested.add(test_map[t])
                    dp_graph.start_item(t)
                    f = pool.submit(test_map[t], result)
                    f.add_done_callback(functools.partial(_dp_callback, t))

                for v in events.values():
                    v.wait()
                events.clear()
                assert tested == set(ParallelTestSuite.thread_test_map[tid])
                k -= len(tested)

        ParallelTestSuite.thread_test_map[tid] = []
