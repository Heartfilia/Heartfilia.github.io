---
title: 【wsl】在windows的linux子系统问题整体
tags:
  - wsl
categories: 摘要
toc: true
date: 2023-03-02 11:20:03
---








持续更新~

<!-- more -->

# 一、安装时

## 1. 无法安装wsl

1. 可能需要开启下面的东西

      这里的两个选项可以先勾上，如果测试不行我们再打开 `Hyper-V`, 我这个电脑安装的时候提示需要开启`Hypter-V` 然后我打开了就可以实现安装了，就没有勾选下面这两个服务测试。

      ![image-20230302102904835](https://static.litetools.top/blogs/wsl/image-20230302102904835.png)

2. 可能需要开启 `hyper-v`

      ![image-20230302101251753](https://static.litetools.top/blogs/wsl/image-20230302101251753.png)

## 2. 没有centos

在微软应用商店是没有centos的wsl镜像的，这时候我们可以去  [下载地址](https://github.com/mishamosher/CentOS-WSL/releases) 这里下载centos的镜像



当然新版本的镜像哪些我们可能需要切换到`wsl2`  

### 设置wsl版本

```bash
wsl --set-default-version 2    # 使你安装的任何新发行版均初始化为 WSL 2 发行版
```

### 查看wsl信息

```bash
wsl -l -v
```





下载完毕后，放在你要放的地方，然后解压出来，用**管理员权限**打开 `CentOS*.exe` 这个安装上系统就好了，安装完成了后会退出一下，然后在安装目录或者cmd输入`wsl`进入linux系统。当然更加方便的就是使用`WindowsTerminal` 一键直达~



# 二、运行时

## 1. 无网络

我们刚进入linux系统的时候，可以更新一下yum 或者 apt 源

```bash
# 以我安装的centos为例
yum -y update

# 很多时候会发现可能没有网络之类的 所以我们需要换源
```

这里有个问题，网上找到的教程里面都是去更换 `/etc/yum.repos.d/` 里面的信息，然后 `yum makecache` 之类的，但是你会发现部分版本并没有那个文件(可能不在，如果在按照网络上的操作即可)



> 手动修改三个文件： 注意我这里是Centos8  如果其他版本自己网上查询

国内源我这里提供两个任选其一即可

```properties
# 清华云
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/virt/$basearch/advanced-virtualization/
# 阿里云
baseurl=https://mirrors.aliyun.com/centos-vault//$contentdir/$releasever/AppStream/$basearch/os/
# 官方的其它源 我测试下来就这个好用
baseurl=http://vault.centos.org/$contentdir/$releasever/extras/$basearch/os/
```



**注释掉 ** `mirrorlist=`    **替换** `baseurl=`

1. CentOS-Linux-AppStream.repo
2. CentOS-Linux-BaseOS.repo
3. CentOS-Linux-Extras.repo

![image-20230302103830368](https://static.litetools.top/blogs/wsl/image-20230302103830368.png)

下面是示例，三个文件是一样的，所以我展示一个

![image-20230302103850038](https://static.litetools.top/blogs/wsl/image-20230302103850038.png)

都弄完了试试下面，如果卡住不行的话，那么就得操作其它方法了

```bash
yum clean all     # 清除系统所有的yum缓存
yum repolist
yum grouplist
yum makecache     # 生成yum缓存

# 如果其它源卡住了，换成官方的那个 重新试试
```

如果上面设置了**还不起作用**，那么就用下面这个万能的方法：

## 2. 设置代理

首先你的windows 得有代理：

我这个主机开启的是 `sock5` 的代理，开启的局域网端口是`19876`

操作这个之前 我们得去windows的防火墙位置设置 入站规则: 控制面板 --> 系统和安全 --> Windows Defender 防火墙 --> 高级设置 --> 入站规则 --> (右边)新建规则 --> (选择)端口 --> 特定本地端口: (输入) 你要开启的端口，可以多开几个后面http服务啥的用 我开了如下`80,6666,8888,8080,8000,9999,19876` 

![image-20230302104847308](https://static.litetools.top/blogs/wsl/image-20230302104847308.png)

编辑 `~/.bashrc` 因为我没有安装`zsh` 所以就改这个文件 或者 `/etc/profile`

```bash
# 自动获取ip 因为wsl每次启动都会分配不同的ip 所以要自动获取
export hostip=$(cat /etc/resolv.conf |grep -oP '(?<=nameserver\ ).*')

# 取一个快捷操作的别名需要网络的时候开启不用的时候一键关闭
# 我的代理是socks5协议的 如果你的是http协议 把socks5改成http即可
alias setproxy='export ALL_PROXY="socks5://${hostip}:19876";'
alias unsetproxy='unset ALL_PROXY'
```

写完了后记得操作保存一下

```bash
source ~/.bashrc
```



测试

```bash
# 我们输入以下命令开启代理
setproxy
# 然后测试一下google
curl http://www.google.com
# 如果直接返回内容证明代理配置ok
# 输入如下命令关闭代理
unsetproxy
```



如果都没有问题的话，那么在安装源啥的国内网络不行的情况下，我们可以直接开启代理下载更新。



## 3. 端口访问

我们有些时候需要部署一些服务在linux里面，然后外面想测试，自己电脑是肯定可以访问到的`127.0.0.1` 或者`linux的内网ip` 都可以，但是我要给局域网里面的其他人访问，那么就需要操作一下了

首先保证我们的服务的端口是在windows防火墙那里配置通过了的，就是上面设置代理那里，因为我默认开启了一堆端口，所以我后面的服务可以通过这些端口访问，当然如果你要部署一个nginx在linux里面转发，那就只需要开启一个对外端口即可

1. 开启windows防火墙端口
2. 在windows用管理员权限打开终端
3. 创建和删除映射
   - 创建映射: `netsh interface portproxy add v4tov4 listenport=win监听端口 listenaddress=0.0.0.0 connectport=wsl的端口 connectaddress=wsl内网ip`  
   - 删除映射: `netsh interface portproxy delete v4tov4 listenport=映射的端口 listenaddress=0.0.0.0`
4. 查看端口映射配置
   - `netsh interface portproxy show all`

![image-20230302105912912](https://static.litetools.top/blogs/wsl/image-20230302105912912.png)

这样子内网就可以愉快的访问你的服务器对应端口了。

> 注意

因为每次重启电脑，linux的内网ip会改变，所以上面的操作需要随时删除和创建

注意防火墙端口得开



## 4. 无systemctl

网上的解决办法基本都是安装下面的东西

```bash
dnf install -y mock perl openssh-server # 安装依赖

dnf install -y epel-release wget    # 如果有wget了就不用操作这里了

wget https://github.com/arkane-systems/genie/releases/download/v1.44/genie-1.44-1.fc34.x86_64.rpm    # 会下载一个文件到你电脑上 可以预先找个位置 或者指定输出位置执行

dnf install -y genie-1.44-1.fc34.x86_64.rpm

genie -s    # 这一步会巨久 好了之后可以测试一下

systemctl list-unit-files   # 测试 无报错即成功
```

但是这个只是一个服务来的，上面执行了后，重启又不行了，所以我们可以开启自启动

```bash
vim ~/.bashrc # 添加自启动

# 添加下面的内容
if [ "`ps -eo pid,lstart,cmd | grep systemd | grep -v -e grep -e systemd- | sort -n -k2 | awk 'NR==1 { print $1 }'`" != "1" ]; then
  genie -s
fi
```

测试 启动docker ok！

![image-20230302111151549](https://static.litetools.top/blogs/wsl/image-20230302111151549.png)
