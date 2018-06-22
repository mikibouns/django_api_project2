import platform
from subprocess import call
import sys


def check_python():
    if float(sys.version[0:3]) >= 3.4:
        return True
    else:
        print('!!!you have an old version of the python, you need version 3.4 and higher!!!')
        return False


def install_win_env():
    print('Windows')
    if check_python():
        try:
            call(r'python -m venv env && . .\env\Scripts\activate.bat && pip install -r requirements.txt', shell=True)
        except Exception as e:
            print(e)


def install_linux_env():
    print('Linux')
    if check_python():
        try:
            call(r'python3 -m venv env && . env/bin/activate && pip install -r requirements.txt', shell=True)
        except Exception as e:
            print(e)




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