#   YADT - an Augmented Deployment Tool
#   Copyright (C) 2010-2013  Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pybuilder.core import use_plugin, init, Author, task

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.flake8')
use_plugin('python.distutils')

authors = [Author('Maximilien Riehl', 'max@riehl.io')]

description = """Verify syntax and contents of YADT configurations.
"""

name = 'yadtlint'
license = 'GNU GPL v3'
summary = 'YADT linter'
url = 'https://github.com/yadt/yadtlint'
version = '0.0.0-dev'

default_task = ['publish']


@init
def set_properties(project):
    project.depends_on('PyYAML')
    project.depends_on('simplejson')
    project.depends_on('docopt')

    project.build_depends_on('mock')

    project.set_property('verbose', True)

    project.set_property('coverage_threshold_warn', 100)
    project.set_property('coverage_break_build', False)

    project.set_property('dir_dist_scripts', 'scripts')

    project.get_property('distutils_commands').append('bdist_egg')
    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration'
    ])

