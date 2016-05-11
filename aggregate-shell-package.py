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
    name='$PKG_NAME',
    url='http://www.quali.com/',
    author='Quali',
    author_email='info@quali.com',
    packages=find_packages(),
	install_requires=required,
    tests_require=required_for_tests,
    version=version_from_file,
    description='Quali networking cisco IOS specific Package',
    include_package_data = True
)"""

MANIFEST_TEMPLATE="""include *.txt
global-include *.ini
"""
README_TEMPLATE="""CloudShell $PACKAGE_NAME package powered by Quali"""


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



def filter_downloaded_dependency_version(local_packages, dependencies_folder_path):
    ''' Filter duplicated package versions, leave only the same as in 'local_packages' to keep recent versions

    :param local_package_list: local_packages folder
    :param dependencies_folder_path:
    :return:
    '''

    local_package_names = []    # list of packages without versions
    local_package_list = []
    for name in os.listdir(local_packages):
        res = re.search('(cloudshell-[\w-]+)-+', name)
        if res:
            local_package_names.append(res.group(1))
            local_package_list.append(name)

    for package in os.listdir(dependencies_folder_path):
        if package in local_package_list:
            continue

        res = re.search('(cloudshell-[\w-]+)-+', package)
        if res:
            package_name = res.group(1)
            if package_name in local_package_names:
                print 'Deleting ', os.path.join(dependencies_folder_path, package_name)
                os.remove(os.path.join(dependencies_folder_path, package))
            else:
                print 'KEEP ', os.path.join(dependencies_folder_path, package)



if __name__ == '__main__':
    # package folder cloudshell-networking-cisco-1.0.10
    # aggregate_cisco_packages Package 1.0.10

    print 'ARGS: '
    print sys.argv
    global package_name

    LOCAL_PACKAGES = 'local_packages'

    if len(sys.argv) < 3:
        print 'Usage: aggregate_shell_package.py [package_folder_path] [package_name]'
        sys.exit(1)

    pkg_path = sys.argv[1]
    package_name =  sys.argv[2]
    local_path = os.getcwd()

    dependencies_folder_name = 'dependencies'
    dependencies_dest_folder = os.path.join(pkg_path, dependencies_folder_name )
    local_packages_path = os.path.join(pkg_path, LOCAL_PACKAGES)

    # ---- clear LOCAL_PACKAGES folder ---------
    if os.path.exists(local_packages_path):
        print 'Found {} folder, clearning'.format(local_packages_path)
        shutil.rmtree(local_packages_path)
    print 'Creating {0}'.format(local_packages_path)
    os.makedirs(local_packages_path)

    # -- copy all cloudshell* packages to LOCAL_PACKAGES (without '-dependencies') ---
    for file in os.listdir(pkg_path):
        file_path = os.path.join(pkg_path, file)
        if re.search('-dependencies\.zip', file) or file == LOCAL_PACKAGES:
            continue
        else:
            shutil.copy2(os.path.join(pkg_path, file), local_packages_path)


    # ---- clear dependencies folder -----
    if os.path.exists(dependencies_dest_folder):
        print 'Found {} folder, clearning'.format(dependencies_dest_folder)
        shutil.rmtree(dependencies_dest_folder)

    print 'Creating {0}'.format(dependencies_dest_folder)
    os.makedirs(dependencies_dest_folder)

    # ---- extract/copy cloudshell and x-dependencies.zip into dependencies ----
    for file in os.listdir(pkg_path):
        file_path = os.path.join(pkg_path, file)
        print 'Working with {}'.format(file_path)

        if re.search(package_name, file) or file in [dependencies_folder_name, dependencies_dest_folder, LOCAL_PACKAGES] :
            print 'Skip.'
            continue
        elif re.search('-dependencies\.zip', file):
            print 'Extracting {} to {}'.format(file_path, dependencies_dest_folder)
            extract_zip(file_path, dependencies_dest_folder)
            os.remove(file_path)

        else:
            move_file_to_folder(file_path, os.path.join(dependencies_dest_folder, file))

    # --- clean duplicates in dependencies, leave only local packages ---
    filter_downloaded_dependency_version(local_packages_path, dependencies_dest_folder)
    print 'done'
