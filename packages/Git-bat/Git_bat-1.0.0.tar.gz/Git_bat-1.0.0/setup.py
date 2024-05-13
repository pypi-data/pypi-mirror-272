# 'sdist'：用於建立原始碼分發包。
# 'bdist'：用於建立二進位分發包。
# 'install'：用於執行安裝操作。
# 'develop'：用於在開發模式下安裝包，通常用於開發過程中。
# 'clean'：用於清理建置產生的暫存檔案和目錄。
# 'test'：用於執行測試操作。
from setuptools import setup, find_packages

# 在安装前检查并删除目录的函数
def delete_directory():
    import os,shutil
    # 获取当前模块的安装路径
    module_installation_path = os.path.dirname(__file__)
    # directory_to_check = "your_directory_path_here"
    directory_to_check = os.path.join(module_installation_path, "your_directory_name_here")
    if os.path.exists(directory_to_check):
        shutil.rmtree(directory_to_check)
        print("Directory deleted successfully!")
    else:
        print("Directory does not exist.")

# 在安装前调用删除目录的函数
# delete_directory()
# import sys
# print(sys.argv)


# pip install --user chrome_pop

# 自定义 egg_info 命令
# from setuptools.command.install import install

# __import__('setuptools.command.egg_info', fromlist=['egg_info'])

class Var:
    name= 'Git_bat'
    @classmethod
    def del_fun( cls,directory):
        import shutil
        try:
            # 遞歸地刪除目錄及其子目錄和文件
            shutil.rmtree(directory)
            print(f"Directory '{directory}' deleted successfully.")
        except OSError as e:
            print(f"Error: {e.strerror}")

from setuptools.command.egg_info import egg_info as _egg_info
class egg_info(_egg_info, Var ):
    @staticmethod
    def delete_directory(directory):
        import shutil
        try:
            # 遞歸地刪除目錄及其子目錄和文件
            shutil.rmtree(directory)
            print(f"Directory '{directory}' deleted successfully.")
        except OSError as e:
            print(f"Error: {e.strerror}")
    def run(self):
        # 在此处执行创建 package1 目录的逻辑
        import os
        # os.makedirs( self.name , exist_ok=True)
        if  os.path.exists(os.getcwd()+os.path.sep+"build"):
            print("!!!!!!!!!!!!!!!",os.getcwd()) ## !!!!!!!!!!!!!!! E:\moon-start\Git.bat
            self.delete_directory( os.getcwd()+os.path.sep+"build" )
            self.delete_directory( os.getcwd()+os.path.sep+f"{Var.name}.egg-info")  ## Git_bat.egg-info
        _egg_info.run(self)

from setuptools.command.install import install
from setuptools import setup, find_namespace_packages
from setuptools.command.build import build
# __import__('setuptools.command.build', fromlist=['build'])
# import os


# os       = __import__('os')
# egg_info = __import__('setuptools.command.egg_info', fromlist=['egg_info'])

# python setup.py build_ext --inplace #### 這個錯誤表示你需要安裝Microsoft Visual C++ 14.0 或更高版本才能建置Cython 擴充功能
# ext_modules=cythonize("Git_bat/**.py", exclude=["venv", "Git_bat/AA/*.py"]),
# pip install Cython
from Cython.Build import cythonize
setup(
    # ext_modules=cythonize("Git_bat/**.py", exclude=["venv", "Git_bat/AA/*.py"]),
    # name='chrome_pop',
    name= Var.name ,
    version='1.0.0',
    # packages=find_packages(),
    packages=find_namespace_packages(include=[Var.name+f'*']),  
    install_requires=[
        'setuptools',
    ],
    cmdclass={
        #   egg_info刪除---會失效 packages
        # 'egg_info': egg_info,  # 使用自定义的 egg_info 命令
    
        # 'egg_info': type('',(egg_info,Var), {'run': lambda self:(egg_info.run(self))   })
        #                                                 #  Var.del_fun(  os.getcwd()+ os.path.sep+"build" ),  
        #                                                 #  Var.del_fun(  os.getcwd()+os.path.sep+f"{Var.name}.egg-info")  ## Git_bat.egg-info
        #                                             #    )   
        #                 # })
    },
    entry_points={
        'console_scripts': [
            ## 禁止::使用-當PY的檔案名稱
            ## '指令 = 實際的__init__檔案:函數名稱',
            # 'start-chrome = chrome_pop:start_chrome',
            # 'pip-s = chrome_pop:pip_install',
            # 'python3 = chrome_pop:python3',
            # 'chrome2 = mode_fun02:python3',

            f'pip-up = {Var.name}.pip_twine:pip_twine',
            f'pip-md = {Var.name}.pip_MD:pip_MD',
            ##### 重點::__init__把方法 from .檔案 import 方法
        ],
    },
)

import atexit


def my_clean():
    # 在这里添加你想要执行的操作，例如清理临时文件等
    # print("Custom cleanup after installation completed.")
    os = __import__('os')
    
    import sys
    if  not "sdist" in sys.argv :##and sys.argv.index("sdist")!=1:
        Var.del_fun(  os.getcwd()+os.path.sep+"build" )
    Var.del_fun(  os.getcwd()+os.path.sep+f"{Var.name}.egg-info")  ## Git_bat.egg-info

# 在 Python 进程退出时注册自定义清理函数
# python setup.py sdist
# import sys
# print("@@@!!!",sys.argv,sys.argv.index("sdist")==1  )
atexit.register(my_clean)




# setup 函数等其他设置代码...
# pip install .  --no-cache-dir  -v