import sys
import os
import zipfile
import shutil
import traceback

def main():
    print "ARGS: {}".format(sys.argv)

    if len(sys.argv) < 2:
        print "Usage: zip_shell_package.py [relative_driver_path]"
        sys.exit(1)

    relative_driver_path = sys.argv[1]
    path_to_dir = os.path.dirname(os.path.abspath(__file__))

    # path to driver directory
    driver_path = os.path.join(path_to_dir, '..', relative_driver_path)

    # check dir with driver data exists
    if not os.path.isdir(driver_path):
        print "Unable to find directory: {}".format(driver_path)
        sys.exit(1)

    # create zip archive for driver data
    driver_name = '{}.zip'.format(os.path.basename(driver_path))
    zip_name = os.path.join(driver_path, '..', driver_name)
    zf = zipfile.ZipFile(zip_name, mode='w')

    print 'Packaging \'{}\': '.format(os.listdir(driver_path))
    print os.listdir(driver_path)

    try:
        for file_name in os.listdir(driver_path):
            file_path = os.path.join(driver_path, file_name)
            zf.write(file_path, file_name)

    except Exception, e:
        print traceback.format_exc()
    finally:
        zf.close()

    print 'Done.'
    # remove folder with driver data for the archive
    print 'Remove path {}'.format(driver_path)
    shutil.rmtree(driver_path)
    print 'Done.'

if __name__ == "__main__":
    main()
