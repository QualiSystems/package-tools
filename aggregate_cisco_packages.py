__author__ = 'oei'
import sys
import os
import re
import zipfile
import shutil

SETUP_TEMPLATE="""
from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()

with open('test_requirements.txt') as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name='cloudshell-networking-cisco-ios-package',
    url='http://www.qualisystems.com/',
    author='QualiSystems',
    author_email='info@qualisystems.com',
    packages=find_packages(),
	install_requires=required,
    tests_require=required_for_tests,
    version=version_from_file,
    description='QualiSystems networking cisco IOS specific Package',
    include_package_data = True
)"""

MANIFEST_TEMPLATE="""include *.txt
global-include *.ini
"""
README_TEMPLATE="""CloudShell shell core package powered by QualiSystems"""


def extract_zip(zip_file, dest_folder):
    fname = os.path.join(pkg_path, file)
    fh = open(zip_file, 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        z.extract(name, dest_folder)
    fh.close()

def move_file_to_folder(src_file , dest_file):
    os.rename(src_file, dest_file)

def write2file(fname, output_str):
    fhandler = open(fname, 'w')
    fhandler.write(output_str)
    fhandler.close()

def write_version_file(pkg_path):

    res = re.search("-([\d\.]+)", pkg_path)
    pkg_version = res.group(1)

    # set version to file
    ver_file_path = os.path.join(pkg_path, 'version.txt')
    write2file(ver_file_path, pkg_version)

def write_manifest(pkg_path):
    # set version to file
    manifest_file_path = os.path.join(pkg_path, 'Manifest.in')
    write2file(manifest_file_path, MANIFEST_TEMPLATE)


def write_readme(pkg_path):
    readme_file_path = os.path.join(pkg_path, 'README.txt')
    write2file(readme_file_path, README_TEMPLATE)

def write_setup_file(pkg_path):
    setup_file_name = os.path.join(pkg_path, 'setup.py')
    write2file(setup_file_name, SETUP_TEMPLATE)


if __name__ == '__main__':
    # package folder cloudshell-networking-cisco-1.0.10
    # aggregate_cisco_packages Package 1.0.10

    INSTALLATION_PACKAGE_NAME = 'cloudshell-networking-cisco-ios'
    #pkg_path='..\Package\\networking-cisco-package-1.0.15'
    pkg_path = sys.argv[1]

    dependencies_folder_name = 'dependencies'
    local_path = os.getcwd()

    dependencies_dest_folder = os.path.join(pkg_path, dependencies_folder_name )
    if os.path.exists(dependencies_dest_folder):
        shutil.rmtree(dependencies_dest_folder)

    os.mkdir(dependencies_dest_folder)

    for file in os.listdir(pkg_path):
        file_path = os.path.join(pkg_path, file)

        if re.search(INSTALLATION_PACKAGE_NAME, file) or file == dependencies_folder_name:
            continue
        elif re.search('-dependencies\.zip', file):
            extract_zip(file_path, dependencies_dest_folder)
            os.remove(file_path)
        else:
            move_file_to_folder(file_path, os.path.join(dependencies_dest_folder, file))

    #write_version_file(pkg_path)
    #write_setup_file(pkg_path)
    #write_manifest(pkg_path)
    #write_readme(pkg_path)

