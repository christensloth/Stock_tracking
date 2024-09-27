import subprocess
import sys
import os

packages = [
    'yfinance',
    'openpyxl',
]

def install_package(package):
    python_executable = sys.executable
    pip_path = os.path.join(os.path.dirname(python_executable), 'Scripts', 'pip.exe')
    subprocess.check_call([python_executable, '-m', 'pip', 'install', package])

def setup_packages():
    for package in packages:
        try:
            install_package(package)
        except Exception as e:
            print(f'Failed to install package, errorcode: {e}, exiting.')
            exit()

def main():
    setup_packages()

if __name__ == "__main__":
    main()