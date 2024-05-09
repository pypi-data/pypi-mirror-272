import wget
import sys
import pkg_resources
import os
import zipfile
import subprocess

"""
Download Jmol-*-binary.tar.gz from
        https://sourceforge.net/projects/jmol/files/Jmol/,
        extract jsmol.zip, unzip it and create a soft-link:

            $ tar -xf Jmol-*-binary.tar.gz
            $ unzip jmol-*/jsmol.zip
            $ ln -s $PWD/jsmol /Users/jacob/miniconda3/lib/python3.9/site-packages/ase/db/static/jsmol
"""
def show(db_file = 'CryDB.db'):
    """
    db_file : the name of database file, default is 'CryDB.db'
    """
    file_url = 'https://figshare.com/ndownloader/files/46175526' # my figshare site

    ase_location = pkg_resources.get_distribution('ase').location
    static_folder = os.path.join(ase_location, 'ase', 'db', 'static')


    if os.path.isdir(os.path.join(static_folder, 'jsmol')):
        pass
    else:
        print("System file not found; downloading automatically.")
        wget.download(file_url, static_folder, bar=bar_progress)
        zipfile.ZipFile(os.path.join(static_folder, 'Jmol_binary.zip')).extractall(static_folder)
        zipfile.ZipFile(os.path.join(static_folder, 'jmol-16.2.15','jsmol.zip')).extractall(static_folder)

    print("Executable for Linux or macOS systems.")
    script_content = f"""
    #!/bin/bash

    # Crystal Database, Cao Bin, HKUST.GZ
    echo "Crystal Database, Cao Bin, HKUST.GZ"

    ase db {db_file} -w

    open http://10.5.151.180:5000
    """

    with open('db.sh', 'w') as file:
        file.write(script_content)

    os.chmod('db.sh', 0o755)

    os.system('./db.sh')


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()