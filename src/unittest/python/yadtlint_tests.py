import unittest
from mockito import when as mock_when, verify, unstub, any as any_value, mock
from yaml.scanner import ScannerError
from yaml.error import Mark

import yadt_lint


class YadtLintTest(unittest.TestCase):

    def setUp(self):
        mock_when(yadt_lint.logger).warn(any_value()).thenReturn(None)
        mock_when(yadt_lint.logger).info(any_value()).thenReturn(None)
        mock_when(yadt_lint.logger).error(any_value()).thenReturn(None)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

    def tearDown(self):
        unstub()

    def test_should_initialize_docopt(self):
        mock_args = {'<file>': 'target',
                     'services_validate': False,
                     'target_validate': True}
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_when(yadt_lint)._get_configuration(any_value()).thenReturn(None)
        mock_when(yadt_lint)._validate_target_schema_new(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint).docopt(yadt_lint.__doc__, version=yadt_lint.__version__)

    def test_should_exit_when_invalid_targetfile_name_is_given(self):
        mock_args = {'<file>': 'foobar',
                     'target_validate': True,
                     'services_validate': False}
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)
        mock_when(yadt_lint)._validate_target_schema_new(any_value()).thenReturn(None)
        mock_when(yadt_lint)._validate_yaml_input(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint.sys).exit(1)

    def test_run_should_call_get_configuration_and_validate_target_schema_new(self):
        mock_args = {'<file>': 'target',
                     'services_validate': False,
                     'target_validate': True}
        mock_when(yadt_lint).docopt(any_value(), version=any_value()).thenReturn(mock_args)
        mock_configuration = mock()
        mock_when(yadt_lint)._get_configuration(any_value()).thenReturn(mock_configuration)
        mock_when(yadt_lint)._validate_target_schema_new(any_value()).thenReturn(None)

        yadt_lint.run()

        verify(yadt_lint)._get_configuration(mock_args)
        verify(yadt_lint)._validate_target_schema_new(mock_configuration)

    def test_should_warn_if_targetfile_contains_name(self):
        configuration = {'name': ['devabc03']}

        yadt_lint._validate_target_schema_new(configuration)

        verify(yadt_lint.logger).warn('target value deprecated: name')

    def test_should_warn_if_targetfile_contains_log_dir(self):
        configuration = {'log-dir': ['devabc03']}

        yadt_lint._validate_target_schema_new(configuration)

        verify(yadt_lint.logger).warn('target value deprecated: log-dir')

    def test_should_validate_one_hostname_after_validating_target_schema(self):
        configuration = {'hosts': ['devytc01']}

        yadt_lint._validate_target_schema_new(configuration)

        verify(yadt_lint.logger).info('targetfile valid')

    def test_should_validate_two_hostname_after_validating_target_schema(self):
        configuration = {'hosts': ['devytc01 devytc02']}

        yadt_lint._validate_target_schema_new(configuration)

        verify(yadt_lint.logger).info('targetfile valid')

    def test_run_should_exit_with_error_when_target_yaml_parsing_fails(self):
        problem_mark = Mark('name', 1, 2, 3, '', '')
        mock_when(yadt_lint)._get_configuration(any_value()).thenRaise(ScannerError(problem_mark=problem_mark))
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint._validate_yaml_input(problem_mark)

        verify(yadt_lint.sys).exit(1)
        verify(yadt_lint.logger).error('Invalid YAML Format check position: (line:column) -> (2:4)')

    def test_run_should_exit_with_error_when_non_existing_file_is_given(self):
        mock_when(yadt_lint)._get_configuration(any_value()).thenRaise(IOError)
        mock_when(yadt_lint.sys).exit(any_value()).thenReturn(None)

        yadt_lint._validate_yaml_input(IOError)

        verify(yadt_lint.sys).exit(1)

    def test_validate_hosts_should_raise_exception_when_host_is_invalid(self):
        host_list = ['devman01', 'tuvman01', 'foofail01']
        self.assertRaises(ValueError, yadt_lint.validate_hostnames, host_list)

    def test_validate_hosts_should_raise_exception_when_host_is_not_given(self):
        host_list = []
        self.assertRaises(ValueError, yadt_lint.validate_hostnames, host_list)

    def test_validate_hosts_should_not_raise_exception_when_host_is_valid(self):
        host_list = ['devman01', 'tuvman01']
        yadt_lint.validate_hostnames(host_list)


class RegexTests(unittest.TestCase):
    MATCHER = yadt_lint.HostPattern

    def test_should_not_match_invalid_hostname(self):
        self.assertFalse(self.MATCHER.match('foobartest'))
        self.assertFalse(self.MATCHER.match('devytcc02'))
        self.assertFalse(self.MATCHER.match('barytc01'))

    def test_should_match_host_name(self):
        self.assertTrue(self.MATCHER.match('devytc01'))

    def test_should_match_host_name_with_wildcard(self):
        self.assertTrue(self.MATCHER.match('devytc*'))

    def test_should_match_host_name_with_number_followed_by_wildcard(self):
        self.assertTrue(self.MATCHER.match('devytc0*'))

    def test_should_match_host_name_with_square_brackets(self):
        self.assertTrue(self.MATCHER.match('devytc[1..10]'))
        self.assertTrue(self.MATCHER.match('devytc[10..15]'))
        self.assertTrue(self.MATCHER.match('devytc[1..3]'))
