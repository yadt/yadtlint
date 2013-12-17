"""
yadtlint

Usage:
yadtlint (-h | --help)
yadtlint validate <file> [options]
yadtlint --version

Options:
-h --help     Show this screen.
--version     Show version.

"""
from docopt import docopt
from logging import getLogger, basicConfig, INFO
import yaml
from yaml.scanner import ScannerError
import sys
import re
import os

__version__ = '${version}'


TargetRegExp = (
    "^.*((BeR|hAm|dev|tuV|Lst)[a-z]{3}" +
    "((\d\d)|(\d?\*)|(\[\d\.\.\d\d\])|(\[\d\d\.\.\d\d\])|(\[\d\.\.\d\]))).*$")
HostPattern = re.compile(TargetRegExp, re.IGNORECASE)

logger = getLogger('yadt_lint')
basicConfig()
logger.setLevel(INFO)


def run():

    args = docopt(__doc__, version=__version__)
    filename = os.path.basename(args['<file>'])
    if filename != 'target':
        logger.error(
            '%s is not a valid targetfile name, should be named "target"' % filename)
        sys.exit(1)
    _validate_yaml_input(args)


def _validate_yaml_input(args):
    try:
        configuration = _get_configuration(args)
        _validate_target_schema_new(configuration)
    except ScannerError as error:
        if hasattr(error, 'problem_mark'):
            mark = error.problem_mark
            logger.error(
                'Invalid YAML Format check position: (line:column) -> (%s:%s)' %
                (mark.line, mark.column + 1))
        sys.exit(1)
    except IOError as error:
        logger.error(error)
        sys.exit(1)


def _get_configuration(args):  # pragma: no cover
    with open(args['<file>']) as config_file:
        configuration = yaml.load(config_file)
    return configuration


def _validate_target_schema_new(configuration):
    for key in configuration:
        if key != 'hosts':
            logger.warn('target value deprecated: %s' % key)
    for key in configuration:
        if key == 'hosts':
            for row in configuration['hosts']:
                configuration['hosts']
                validate_hostnames(row.split())
    return configuration


def validate_hostnames(hosts):
    if not hosts:
        raise ValueError('No hostname given')
    for host in hosts:
        if not HostPattern.match(host):
            raise ValueError('hostname invalid: %s' % host)
    logger.info('targetfile valid')
    return hosts
