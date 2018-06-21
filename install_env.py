import platform
from subprocess import call
import os


def install_win_env():
    print('Windows')
    print(os.system('python -V'))


def install_linux_env():
    print('Linux')


def install_mac_env():
    print('MacOS')


if __name__ == '__main__':
    if platform.system() == 'Windows':
        install_win_env()
    elif platform.system() == 'Linux':
        install_linux_env()
    elif platform.system() == 'Darwin':
        install_mac_env()
    else:
        print('!!!platform is not defined!!!')