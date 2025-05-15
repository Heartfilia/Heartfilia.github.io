---
title: 【linux】在没有root权限电脑安装编译后的python
tags:
  - openssl
  - linux
  - python
categories: 教程
date: 2025-05-15 16:54:48
---


为什么会出这个呢，因为当前工作碰到了，顺道记录一下解决方案

<!-- more -->



# 问题情况

1. 没有root权限
2. 自带的python或者已经装好的python或者conda 都不能装包或者下载东西，一直提示443异常

单独运行python代码会提示以下内容

```bash
    import _ssl   # if we can't import it, let the error propagate.....
ModuleNotFoundError: No module named '_ssl'
```

# 问题剖析

1. openssl版本过低
2. python编译的时候没有链接到openssl



# 大概解决思路

1. 要么安装比较低版本的python
2. 要么重新编译python



# 解决

**我这里选择重新编译，因为没有root权限，所以下面的操作都在用户目录下～**

## 1. 下载openssl

我这里选择python3.10版本，所以我这里的openssl至少得要1.1.1版本，其他的版本自行搜索处理

```bash
# 下载 OpenSSL 1.1.1（兼容 Python 3.10）
wget https://www.openssl.org/source/openssl-1.1.1w.tar.gz
tar xzf openssl-1.1.1w.tar.gz
cd openssl-1.1.1w

# 配置并安装到用户目录
./config --prefix=$HOME/.local/openssl --openssldir=$HOME/.local/openssl
make -j$(nproc) && make install

# 添加环境变量
echo 'export PATH="$HOME/.local/openssl/bin:$PATH"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$HOME/.local/openssl/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc
```

操作完了之后，输入

```bash
openssl version  # 应输出 OpenSSL 1.1.1w
```

## 2. 下载python

直接去官网下载你的python xz或者tar的都可以，先解压好

```bash
cd Python-3.10.X
make clean    # 清理之前的make数据，如果之前操作过

# 指定 OpenSSL 路径
export LDFLAGS="-L$HOME/.local/openssl/lib"
export CPPFLAGS="-I$HOME/.local/openssl/include"
export LD_LIBRARY_PATH="$HOME/.local/openssl/lib:$LD_LIBRARY_PATH"

# 配置时显式链接 OpenSSL
./configure \
  --prefix=$HOME/.local/python-3.10 \
  --with-openssl=$HOME/.local/openssl \
  --enable-optimizations \
  --disable-ipv6
  
# 编译安装
make -j$(nproc) && make install
```

## 3. 验证

```bash
$HOME/.local/python-3.10/bin/python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

只要上面没有报错就可以了

