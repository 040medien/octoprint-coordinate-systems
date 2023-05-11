# coding=utf-8
''' Plugin setup file '''

from setuptools import setup
plugin_identifier = 'coordinatesystems'
plugin_package = 'octoprint_coordinatesystems'
plugin_name = 'OctoPrint-CoordinateSystems'
plugin_version = '0.1'
plugin_description = 'An OctoPrint plugin to manage workspace coordinate systems (G54-G59.3) for Marlin-based CNC machines'
plugin_author = 'Frederik Kemner'
plugin_author_email = 'coordinate-systems@fredo.org'
plugin_url = 'https://github.com/040medien/octoprint-coordinate-systems'
plugin_license = 'Apache License 2.0'
plugin_requires = ['OctoPrint>=1.8.0']
plugin_additional_data = []
plugin_additional_packages = []
plugin_ignored_packages = []
additional_setup_parameters = {}

try:
    import octoprint_setuptools
except ImportError:
    print('Could not import OctoPrint\'s setuptools, are you sure you are ' +
          'running that under the same python installation that OctoPrint ' +
          'is installed under?')
    import sys
    sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
    identifier=plugin_identifier,
    package=plugin_package,
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    mail=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    requires=plugin_requires,
    additional_packages=plugin_additional_packages,
    ignored_packages=plugin_ignored_packages,
    additional_data=plugin_additional_data
)

if additional_setup_parameters:
    from octoprint.util import dict_merge
    setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)