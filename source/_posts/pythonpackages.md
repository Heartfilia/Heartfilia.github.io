---
title: 【打包】简述几种源码打包工具
tags: python
categories: 摘要
toc: true
date: 2023-05-11 16:10:45
---


本文讲的是的 python源码打包成 whl 或者 tar.gz 之类的  而不是 exe哈

<!-- more -->

# setuptools

最早的时候我们均按照这个东西，详细的东西就不说了，我就按照我的 [lite-tools](https://github.com/Heartfilia/lite_tools) 的打包参数来说好了

> setup.py

```python
# -*- coding: utf-8 -*-
# @Time   : 2021-04-06 15:25
# @Author : Lodge
from sys import version_info
from setuptools import setup

from lite_tools.version import VERSION


if version_info < (3, 8, 0):
    raise SystemExit("Sorry! lite_tools requires python 3.8.0 or later.")


with open("README.md", "r", encoding='utf-8') as fd:
    long_description = fd.read()

base_requires = [
    'loguru',          # 基本的日志打印相关的调用
]


setup(
    name='lite-tools',
    version=VERSION.strip(),
    description='一些让你效率提升的小工具集合包[还在持续增加及优化]',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lodge',
    author_email='lodgeheartfilia@163.com',
    url='https://github.com/Heartfilia/lite_tools',
    packages=[
        'lite_tools',
    ],
    license='MIT',
    install_requires=base_requires,
    python_requires=">=3.7",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)

```

上面的内容我是**移除了一些**内容，但是整体流程就是写一个这样的文件，后面我们在命令行执行下面的操作就可以打包文件到 `dist` 目录下了

```bash
python setup.py bdist_wheel      # 只打包 whl文件 比较常用 需要 pip install wheel
python setup.py sdist            # 这个就是把源码打包 当然也可以两个一起 两个命令都写后面
```



# pyproject.toml

这个只是一个文件，告诉构建工具该怎么做而已，这是最新的python 推荐使用的方式，我这里

`先`手动创建一个，后面有工具可以自己生成，但是我这里得先讲一下手动创建的这个步骤。

这个文件是放在之前放`setup.py`的那个目录层级的，现在我们不需要用`setup.py`来管理这个打包了。

现在我们是推荐用 `setup.cfg` 来配置，这个文件和 `setup.py`里面的内容很相似，基本都能找到对应的字段。可以写什么字段可以点击这里查看[详细文档](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)。

我下面把我现在写的 `部分` 配置贴出来：注意，没有引号。 (我下面内容还是删除了很多，实际这些内容点前面的详细文档里面有更详细的写法)

```ini
[metadata]
name = lite-tools
version = attr: lite_tools.version.VERSION
author = Lodge
author_email = lodgeheartfilia@163.com
description = 一些自己常用的小工具包
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/Heartfilia/lite_tools
classifiers =
    Intended Audience :: Developers
    Operating System :: OS Independent
license = MIT


[options]
python_requires = >=3.7
packages =
    lite_tools
install_requires =
    loguru

[options.entry_points]
console_scripts =
    lite-tools = lite_tools.commands.cmdline:execute

[options.extras_require]
all =
    reportlab
    Pillow

```

现在，我们有了`pyproject.toml` 和 `setup.cfg` 两个文件了，我们该怎么打包呢。

我们现在用工具一 `build`， 我们首先需要 `pip install --upgrade build`

然后

```bash
python -m build
```

它会自动去根据 `pyproject.toml` 和 `setup.cfg` 打包。

这个工具在windows可能会出现一些问题，我下面是因为有些描述文档有中文，我cfg文件里面有读取，导致异常了。

![image-20230511123002058](https://static.litetools.top/blogs/pythonpackages/image-20230511123002058.png)

然后我换了一个linux系统: `wsl` 就可以顺利执行了。



# poetry

这个工具也可以，我这里不讲了，自己网上搜 [Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/)



# flit

这个是一个更加方便的python打包工具，和上面poetry类似，根据自己喜好即可。[Flit 3.8.0 — Flit 3.8.0 documentation (pypa.io)](https://flit.pypa.io/en/stable/)
