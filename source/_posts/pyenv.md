---
title: 【pyenv】python版本管理神器
tags:
  - python
  - pyenv
categories: 教程
toc: true
date: 2023-03-31 17:19:00
---


距离上一次写文章已经很久过去了，主要是工作繁忙，我想写的东西比较花时间，但是今天【20230331】写这个是比较简短的，耗时很少，但是确实有用。



<!-- more -->

所以到这个时间点，我工具均用最新版进行讲解，其中有一些问题也可以说出来避免踩坑~



# 一、这是什么

我们平时在开发东西的时候，都听说过虚拟环境，这样子可以让我们需要开发的东西所使用的包版本什么的是和我们日常使用的相互隔离，不会出现兼容问题。但是这个东西有个问题就是，大多情况下，我们都是同一个python，不能保证在其它版本python也能完美运行，所以就有了接下来我要说的这个神器----`pyenv`。



## 1. 说明

我这里会有很多特殊情况，如果你的**网络好**，或者**有梯子**之类的工具，可以按照官方的教程，但是这里得注意一个点，`pyenv` 这个工具**在windows 和 linux/mac 需要安装的是不一样的东西**。

> 下面是我贴出来的官方的链接

1. `window`: [点这里](https://github.com/pyenv-win/pyenv-win)

2. `linux`:  [点这里](https://github.com/pyenv/pyenv#installation)

3. `macos`: 和`linux`一样的，官方也推荐使用`homebrew` 

   <a id="homebrew"></a>

   - `homebrew`： mac 上面一个软件包管理神器，推荐使用，如果网络好可以参考[这里](https://brew.sh/index_zh-cn),不好也可以用国内源，这里给[一篇不错的教程](https://cloud.tencent.com/developer/article/1935121)

> 【如果是mac通过homebrew安装 或者linux通过官方安装的 不用考虑兼容问题，测试完美运行，尤其你用的是windows需要注意后面问题】如果要用pyenv，电脑上最好别用官方的python了，我们都用这个了，就可以更方便管理了。主要是环境变量里面如果还有系统自带的python那么可能会有一些问题，后面会说。

## 2. 安装

我们上面已经给出了基于官方的链接的安装地址，可以看里面的操作，一键安装。但是对于我们国内的用户来说，可能就没有那么轻松了。

### 2.1 mac

我们已经基于第一点说了那个homebrew，并且按照教程**配置了国内源**。所以这里安装就很轻松。

```zsh
brew install pyenv
brew install pyenv-virtualenv
```

如果安装的时候报错了,可以输入`brew version` 会提示你有两个命令，复制粘贴一下就好了。

### 2.2 linux

这里我教两个方案，网上都是按照官方的，可能会没有网络连接不上。

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

1. 方案一：把`https://github.com/pyenv/pyenv.git` 转移到`gitee` ，然后替换成`gitee`你设置的仓库地址就好了，下面是一个我复制别人转移好的仓库的示例，比较新(20230326迁移的，我看了一下这个仓库是持续维护的，后面pyenv-virtualenv 也是这个用户维护的，可以直接用)

   ```bash
   git clone https://gitee.com/cosynet/pyenv.git ~/.pyenv
   ```

   

2. 方案二： 手动直接下载下来，手动把zip文件解压到 `~/.pyenv` 这个目录

文件放到了`~/.pyenv` 目录下后，我们需要编译一下，直接按照官方教程

```bash
cd ~/.pyenv && src/configure && make -C src
```

然后我们需要添加一下系统环境变量，下面两点根据你的终端类型选择。

1. 对于`bash`

   ```bash
   # 下面是基于 .bashrc 的一些操作
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   ```

   

2. 对于`zsh`

   ```zsh
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

   

弄完了之后，需要重启一下`shell`

```bash
exec "$SHELL"
```

### 2.3 windows

这个地方和`linux/macos`的包是不一样的，我们可以在官方下载，也可以通过我们已有的python的pip来安装，下面的home可以是你任意目录，不写的话默认是在你windows主用户目录下。当然也可以安装好了剪切到你想要放的目录，然后按照下面的添加环境变量就好了。

```bash
pip install pyenv-win --target $HOME\.pyenv
```

然后我们需要去系统设置一下环境变量，我这里就不教命令行了，如果想用命令行也可以，但是大概率还得去系统设置里面调整一下顺序。

首先先在系统变量里面添加一个`pyenv`的root变量

![image-20230331112613562](https://static.litetools.top/blogs/pyenv/image-20230331112613562.png)

![image-20230331112725148](https://static.litetools.top/blogs/pyenv/image-20230331112725148.png)

我的是这个情况

![image-20230331112759833](https://static.litetools.top/blogs/pyenv/image-20230331112759833.png)

然后就是配置下面两个东西，我这个地方是把这俩往前面移动了

![image-20230331112419436](https://static.litetools.top/blogs/pyenv/image-20230331112419436.png)

然后我把我之前安装的python的环境变量给移除了，不移除也可以，但是为了避免可能出现的如下情况，下面是特殊情况的示例：

![image-20230331112948140](https://static.litetools.top/blogs/pyenv/image-20230331112948140.png)

![image-20230331113139912](https://static.litetools.top/blogs/pyenv/image-20230331113139912.png)

我系统是安装了`3.10.8`版本的普通python，然后切换了`pyenv`版本后替换不过去,因为我把python的环境变量顺序放在了pyenv的环境变量之前。我就想着我本来就要用pyenv管理python的，所以我就移除了之前的那个系统变量。

现在我弄好了情况如下：

![image-20230331113323938](https://static.litetools.top/blogs/pyenv/image-20230331113323938.png)

# 二、可能异常

## 1. 建议安装

因为有些包有什么版本问题啥的，所以这里建议先安装这些东西再进行下面的操作。

### 1.1 macos

需要安装`Xcode Command Line Tools`和`Homebrew`

```bash
xcode-select --install
```

`Homebrew `在前面已经讲了，[点击这里跳转](#homebrew)

### 1.2 linux

#### Ubuntu/Debian

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev
```

#### Fedora/Centos/RHEL

```bash
dnf install zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel
```

## 2. 安装python

<a id="install"></a>

这里一般都是网络的问题，要么替换国内源，要么就去下面下载离线镜像，python官网也可以下载，就看你了。

```bash
# 淘宝镜像  更新比较及时
https://registry.npmmirror.com/binary.html?path=python/
# 华为镜像  很久不更新了
https://mirrors.huaweicloud.com/python/
# 官方镜像  最即时但是可能很慢
https://www.python.org/ftp/python/
```

官方的情况如下：

![image-20230331115036842](https://static.litetools.top/blogs/pyenv/image-20230331115036842.png)

我们下载好了离线包之后，把包复制到`.pyenv`下面的目录

1. windows --> `你的目录\.pyenv\pyenv-win\install_cache` 这个目录下，把从你下载的python丢这里

2. mac/linux --> `你的目录\.pyenv\cache` (这个cache目录可能不存在，需要手动在这里创建一下)，然后可以直接在这个目录执行你想要下载的python版本，示例:

   ```bash
   wget https://registry.npmmirror.com/-/binary/python/3.11.2/Python-3.11.2.tar.xz
   ```

![image-20230331115950578](https://static.litetools.top/blogs/pyenv/image-20230331115950578.png)

然后我们就可以去命令行执行安装这个指定版本的python了

```bash
pyenv install 3.11.2
```

**安装的过程会比较久**~ 耐心等待



对自己网络自信的可以输入下面指令查看可以安装的python版本

```bash
pyenv install -l
# 看中了哪个python后 就可以
pyenv install 3.11.2   # 优先读取 cache 目录里面的已经有的包，没有才会联网下载
```



# 三、教程

## 1. 插件

这是一个虚拟环境插件，不过这个只适用于 linux/mac，windows这个属于另类，没有官方插件（主要是开发者大佬说兼容windows浪费时间，他又不用windows），但是可**以用其它工具实现**，道理一样的。

1. mac用户通过 `homebrew`轻松安装

   ```bash
   brew install pyenv-virtualenv
   eval "$(pyenv virtualenv-init -)"
   ```

   

2. linux 可以参考 [官方](https://github.com/pyenv/pyenv-virtualenv)，同理网络不好也可以用国内镜像

   ```bash
   git clone https://gitee.com/cosynet/pyenv.git $(pyenv root)/plugins/pyenv-virtualenv
   
   # 我这里是写入到bash的 可以根据你的终端类型更换  ~/.zshrc
   echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
   
   exec "$SHELL"
   ```
   
   然后其他的按照官方弄，我这里不讲了



插件安装完了之后，输入 `pyenv` 会发现多了一些东西

>  没安装的时候

```bash
pyenv 2.3.17
Usage: pyenv <command> [<args>]

Some useful pyenv commands are:
   commands    List all available pyenv commands
   exec        Run an executable with the selected Python version
   global      Set or show the global Python version(s)
   help        Display help for a command
   hooks       List hook scripts for a given pyenv command
   init        Configure the shell environment for pyenv
   install     Install a Python version using python-build
   latest      Print the latest installed or known version with the given prefix
   local       Set or show the local application-specific Python version(s)
   prefix      Display prefixes for Python versions
   rehash      Rehash pyenv shims (run this after installing executables)
   root        Display the root directory where versions and shims are kept
   shell       Set or show the shell-specific Python version
   shims       List existing pyenv shims
   uninstall   Uninstall Python versions
   --version   Display the version of pyenv
   version     Show the current Python version(s) and its origin
   version-file   Detect the file that sets the current pyenv version
   version-name   Show the current Python version
   version-origin   Explain how the current Python version is set
   versions    List all Python versions available to pyenv
   whence      List all Python versions that contain the given executable
   which       Display the full path to an executable
```

> 安装完了之后

```bash
pyenv 2.3.17
Usage: pyenv <command> [<args>]

Some useful pyenv commands are:
   activate    Activate virtual environment
   commands    List all available pyenv commands
   deactivate   Deactivate virtual environment
   exec        Run an executable with the selected Python version
   global      Set or show the global Python version(s)
   help        Display help for a command
   hooks       List hook scripts for a given pyenv command
   init        Configure the shell environment for pyenv
   install     Install a Python version using python-build
   latest      Print the latest installed or known version with the given prefix
   local       Set or show the local application-specific Python version(s)
   prefix      Display prefixes for Python versions
   rehash      Rehash pyenv shims (run this after installing executables)
   root        Display the root directory where versions and shims are kept
   shell       Set or show the shell-specific Python version
   shims       List existing pyenv shims
   uninstall   Uninstall Python versions
   --version   Display the version of pyenv
   version     Show the current Python version(s) and its origin
   version-file   Detect the file that sets the current pyenv version
   version-name   Show the current Python version
   version-origin   Explain how the current Python version is set
   versions    List all Python versions available to pyenv
   virtualenv   Create a Python virtualenv using the pyenv-virtualenv plugin
   virtualenv-delete   Uninstall a specific Python virtualenv
   virtualenv-init   Configure the shell environment for pyenv-virtualenv
   virtualenv-prefix   Display real_prefix for a Python virtualenv version
   virtualenvs   List all Python virtualenvs found in `$PYENV_ROOT/versions/*'.
   whence      List all Python versions that contain the given executable
   which       Display the full path to an executable
```

这里怎么使用也很简单的啦，后面轻度教学，核心使用直接看官方git下面~

## 2. 命令

主要列举了**常用**的一些，还有很多不常用的或者不同系统不兼容的就算了

### 1.0 `直接pyenv`

```bash
pyenv            # 这个会详细介绍每个做啥的
或者
pyenv commands   # 这个只会列出来可以操作的指令
```

### 1.1 `help`

```bash
pyenv help global
```

我把这个放在第一个，就是因为不懂得可以在这里输入看看教程

### 1.2 设置版本

我这里主要是为了把三个放一起，因为这三个是效果类似的，但是有差别，

`global`: 就是把某个python设置为全局使用的，就是你在哪儿打开都是这个版本的，我目前是喜欢用`python3.10` 所以我就设置了这个

![image-20230331115835952](https://static.litetools.top/blogs/pyenv/image-20230331115835952.png)

本来上面会有一个`system` 的选项的，因为我不想用了，移除了就没有了

直接把已经安装好的python版本操作如下：

```bash
pyenv global 3.10.5
```



`shell`: 这是给当前shell环境**临时**使用python版本，关掉了就恢复。

```bash
pyenv shell 3.8.5
```

![image-20230331121133488](https://static.litetools.top/blogs/pyenv/image-20230331121133488.png)

`pyenv shell --unset` 可以立即取消。



`local`: 这里给当前目录设置python版本，包括子目录。你下次打开就会默认这个版本python。在指定目录输入后，你会发现你的目录里面多了一个文件。这个地方就会一直用这个版本。

```bash
pyenv local 3.10.5
# 当然这个也可以 pyenv local 3.10.5 2.7.5  多个一起
```



![image-20230331121348374](https://static.litetools.top/blogs/pyenv/image-20230331121348374.png)

`pyenv local --unset` 取消本地的设置

### 1.2 `version`

```bash
pyenv version
```

查看当前正在使用的python版本。

### 1.3 `versions`

```bash
pyenv versions
```

查看已经安装好了的python版本信息

### 1.4 `install`

```bash
pyenv install -l  或者  pyenv install --list  展示可以安装的版本

pyenv install 3.8.5
```

如果网络不好，可以离线安装python，详细看前面，[点这里](#install)跳转。

### 1.5 `uninstall`

```bash
pyenv uninstall 3.8.5
```

卸载指定版本的python

### 1.6 `rehash`

```bash
pyenv rehash
```

按道理来说 安装了新版本后都应该执行以下，不过新版的好像移除了这个，但是**如果命名行相关工具出问题了，请记得输入这个一般可以恢复**

### 1.7 `shims`

```bash
pyenv shims
```

列出当前存在的shims（pyenv的工作原理就是在一个叫shims的目录下创建Python解释器的“假版本”，寻找Python应用时先从该目录查找）,这也是前面我们添加环境变量的时候需要添加一个这个的原因。

### 1.8 `which`

```bash
pyenv which scrapy
```

列举出这个环境下可执行文件的绝对路径。

### 1.9 `virtualenv`

这个是linux/macos安装了插件有的操作，windows得用其它pip安装的包实现。

```bash
pyenv virtualenv 3.8.5 my_project  # 通过3.8.5的python版本创建一个my_project的虚拟环境
```

```bash
pyenv virtualenvs                  # 查看当前创建的虚拟环境
```

```bash
pyenv virtualenvs active my_project   # 激活虚拟环境
```

```bash
pyenv deactivate                   # 在虚拟环境中退出去
```

### 1.10 更多

其实还有很多指令，但是不常用，也不兼容，不过linux/macos是完全体，所以很多在windows上没有的。不过又不常用我就不写了。

## 3. 更新pyenv

因为我们的`pyenv `是通过`git clone`的，所以我们只需要进入 `.pyenv`的目录下执行

```bash
git pull
```

