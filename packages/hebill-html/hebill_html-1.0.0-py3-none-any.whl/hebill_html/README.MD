## 说明
使用python生成HTML代码

## 步骤
1. 安装必要包  
   ``` 
   pip install setuptools
   pip install wheel
   pip install twine 
   ```

2. 目录结构格式：  
    ```text
    /source_root  
     -- /myProject  
     -- /myProject/__init__.py  
     -- /myProject/constants.py  
     -- /myProject/core.py  
     -- pypi.py  
     -- README.MD  
     -- requirements.txt
    ```
3. 在constants.py中设定常量   
    ```python
    VERSION = '1.0.0'
    NAME = 'myProject'
    DESCRIPTION = 'Project Description'
    LONG_DESCRIPTION = 'README.MD'
    LONG_DESCRIPTION_TYPE = 'text/markdown'
    URL = 'http://www.project.url/'
    AUTHOR = 'Your Name'
    AUTHOR_EMAIL = 'email@project.url'
    AUTHOR_URL = 'http://www.project.url/'
    ```
   
4. 在__init__.py中加载
    ```python
    from .core import MyModule
    from .constants import *
    ```
5. 编写 pypi.py 内容
   ```python
   from hebill_pypi import Pypi
   import myProject
   
   pypi = Pypi(myProject, r'D:\SDK\Environments\myProject\Scripts\python.exe')
   pypi.pack()
   ```

6. 运行 pypi.py
