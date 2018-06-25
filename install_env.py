#!/usr/bin/python3

import platform
from subprocess import call
import sys
import os


def main():
    if float(sys.version[0:3]) >= 3.4:
        if platform.system() == 'Windows':
            print('Windows')
            path_activate_env = os.path.join(os.getcwd(), r'venv\Scripts\activate.bat')
            call('python -m venv venv && {} && pip install -r requirements.txt'.format(path_activate_env), shell=True)
        elif platform.system() == 'Linux':
            print('Linux')
            call(r'python3 -m venv env && . env/bin/activate && pip install -r requirements.txt', shell=True)
        elif platform.system() == 'Darwin':
            print('MacOS')
            call(r'python3 -m venv env && . env/bin/activate && pip install -r requirements.txt', shell=True)
        else:
            print('For OS is non-installer, please install manually')
        print('created virtual environment and installed all packages')
    else:
        print('!!!you have an old version of the python, you need version 3.4 or higher!!!')


if __name__ == '__main__':
    main()
