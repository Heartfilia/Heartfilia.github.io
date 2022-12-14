---
title: 【应用破解】Navicat重置试用
date: 2022-12-08 09:54:22
tags: 注册机
categories: 资源
---





懒得破解navicat 或者 避免被 递传票 可以试试以下方案



<!-- more -->

{% alertbox warning "本地教程只适用于非商业用途，其余看个人" %}

{% alertbox info "以下代码只适用于windows" %}



就是通过代码的方案，把本地注册表里面记录`navicat premium`的信息给抹了，然后就可以实现无限重置的效果，这个方法基本适用于所有版本，所以去官网下载 `navicat` 最新版即可!

# Python代码

这里是给有python环境的小可爱们准备的

{% collapse python代码 %}

```python
import winreg
import os
import time
from collections import deque
from typing import Any


# root
HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER

# key path
PREMIUM_PATH = r'Software\PremiumSoft'
CLSID_PATH = r'Software\Classes\CLSID'


def get_sub_keys(root: Any, reg_path: str) -> list:
    """This function will retrieve a list of sub-keys under the path
    of `root` + `reg_path`.

    Args:
        root(Any): Root registry.
        reg_path(str): The relative specific path under the root registry.

    Returns:
        The list of sub-keys.
    """
    key_result = winreg.OpenKeyEx(root, reg_path)
    i: int = 0
    sub_keys_list: list = list()

    while True:
        try:
            sub_keys = winreg.EnumKey(key_result, i)
            sub_keys_list.append(sub_keys)
            i += 1
        except Exception as e:
            break
    
    return sub_keys_list


def get_all_keys(root: Any, key_path: str) -> list:
    """Get the list of absolute path of all entries under the
    specified path through the deque.

    Args:
        root(Any): Root registry.
        key_path(str): The relative specific path under the root registry.

    Returns:
        A list of all entries under the keys.
    """
    all_keys_list: list = list()

    qeque = deque()
    qeque.append(key_path)

    while len(qeque) != 0:
        sub_key_path = qeque.popleft()

        for item in get_sub_keys(root, sub_key_path):
            item_path = os.path.join(sub_key_path, item)

            if len(get_sub_keys(root, item_path)) != 0:
                qeque.append(item_path)
                all_keys_list.append(item_path)
            else:
                all_keys_list.append(item_path)
    
    return all_keys_list


def main():
    """The entry function to be executed.

    Returns:
        None
    """
    clsid_all_keys_list = get_all_keys(HKEY_CURRENT_USER, CLSID_PATH)
    premium_all_keys_list = get_all_keys(HKEY_CURRENT_USER, PREMIUM_PATH)
    premium_sub_keys_list = [os.path.join(PREMIUM_PATH, item) for item in get_sub_keys(HKEY_CURRENT_USER, PREMIUM_PATH)]
    print(f"premium_sub_keys_list: {premium_sub_keys_list}")

    for clsid_item in clsid_all_keys_list:
        if "Info" in clsid_item:
            clsid_item_prefix = os.path.dirname(clsid_item)
            print(f"# Info item: {clsid_item}")
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item)
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item_prefix)
    
    # The outermost folder is not deleted.
    for premium_item in reversed(premium_all_keys_list):
        if "Servers" in premium_item:
            print(f"Tips: Servers => {premium_item} will not be deleted.")
            pass
        elif premium_item in premium_sub_keys_list:
            print(f"Tips: Servers => {premium_item} will not be deleted.")
            pass
        else:
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, premium_item)


if __name__ == "__main__":
    print("开始删除注册信息..耐心等待..期间请不要运行navicat")
    main()
    print("操作完成.")
```

{% endcollapse %}



# 没有python环境的小可爱



1. 创建一个空白的txt文件在任意位置都行

2. 在里面粘贴下方代码

   {% collapse bat代码 %}

   ```te
   @echo off
   
   echo Delete HKEY_CURRENT_USER\Software\PremiumSoft\NavicatPremium\Registration[version and language]
   for /f %%i in ('"REG QUERY "HKEY_CURRENT_USER\Software\PremiumSoft\NavicatPremium" /s | findstr /L Registration"') do (
       reg delete %%i /va /f
   )
   echo.
   
   echo Delete Info folder under HKEY_CURRENT_USER\Software\Classes\CLSID
   for /f %%i in ('"REG QUERY "HKEY_CURRENT_USER\Software\Classes\CLSID" /s | findstr /E Info"') do (
       reg delete %%i /va /f
   )
   echo.
   
   echo Finish
   
   pause
   ```

   {% endcollapse %}

3. 保存然后关闭窗口

4. 修改文件名称把末尾的`.txt` 改成 `.bat` 

   - 有的小可爱可能看不到这个`.txt` ,那么需要在windows文件管理器上面点击`查看` -> `显示` -> `文件的扩展名` 勾上

5. 然后保存文件，关闭窗口

6. 然后双击这个文件 弹出来一个窗口 显示`Finish` 即可





总体来说没啥难度，复制粘贴，然后就可以得到一个正版的不会被递传票的工具拉~

