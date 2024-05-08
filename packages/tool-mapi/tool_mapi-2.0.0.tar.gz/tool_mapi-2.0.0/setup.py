 

from setuptools import find_packages, setup
# !python3 -m pip install wheel
# !python3 -m  pip install setuptools
# !python3 -m  pip install twine


MAJOR = 2
MINOR = 0
MICRO = 0
VERSION = '%d.%d.%d'%(MAJOR,MINOR,MICRO)

 
name='tool_mapi'
def _find_packages(packages , name):
    if name in packages:
        if name == f"{name}"[:len(name) ]:
            return  packages
packages=[i for i in find_packages() if _find_packages(i , name )  ]

setup(
    name=name,
    packages=packages,
    version=VERSION,
    # description='tool_mapi library',
    author='Me',
)


# pip install wheel
# pip install twine


#/usr/bin/python3 /home/ubuntu/my_python_library/setup.py bdist_wheel
# C:/Users/yosefb/AppData/Local/Programs/Python/Python39/python.exe "c:/Users/yosefb/Downloads/backup_04_08_2022 (1)/backup_04_08_2022/my_python_library/setup.py"  bdist_wheel



# python3 -m  pip install  /home/ubuntu/my_python_library/dist/tool_geox1-0.0.0-py3-none-any.whl

 









