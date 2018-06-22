#!/usr/bin/python3

import platform
from subprocess import call
import sys
import os


def check_python():
    if float(sys.version[0:3]) >= 3.4:
        return True
    return False


def install_win_env():
    print('Windows')
    path_activate_env = os.path.join(os.getcwd(), r'venv\Scripts\activate.bat')
    if check_python():
        call('python -m venv venv && {} && pip install -r requirements.txt'.format(path_activate_env), shell=True)
        print('created virtual environment and installed all packages')
        os.ti


def install_linux_env():
    print('Linux')
    if check_python():
        call(r'python3 -m venv env && . env/bin/activate && pip install -r requirements.txt', shell=True)
    else:
        print('!!!you have an old version of the python, you need version 3.4 and higher!!!')


def install_mac_env():
    print('MacOS')


def main():

    if platform.system() == 'Windows':
        install_win_env()
    elif platform.system() == 'Linux':
        install_linux_env()
    elif platform.system() == 'Darwin':
        install_mac_env()
    else:
        print('!!!platform is not defined!!!')


if __name__ == '__main__':
    main()