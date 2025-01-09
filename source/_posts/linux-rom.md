---
title: 【linux】磁盘挂载相关问题
tags:
  - linux
  - docker
categories: 教程
toc: true
date: 2025-01-09 15:59:06
---


记录一下在ubuntu中遇到的一些问题及相关的解决方法 ：root 登陆； 磁盘挂载

<!-- more -->



# 一、root权限

因为有些操作老是输入 `sudo` 很麻烦，所以我们最好还是像 centos 之类的默认就是root劝降来的舒服，首先我们进入账号 给root账号创建密码

1. 设置root账号的密码

```bash
sudo passwd root
```

然后输入并确认root账号的密码，可能会问你要密码先，如果没有配置的话，大概率是和你当前账号一样的密码

2. 允许 root用户通过ssh登陆

```bash
sudo vim /etc/ssh/sshd_config   # 打开配置文件
```

然后我们输入 `? `然后输入 `PermitRoot ` 直接回车

![image-20250109115600453](https://static.litetools.top/blogs/linux_rom/image-20250109115600453.png)

![image-20250109115644045](https://static.litetools.top/blogs/linux_rom/image-20250109115644045.png)

然后按 `n` 切换下一个匹配，找到这一行，我这里是改过的，如果没有改的话，这里应该是

`PermitRootLogin prohibit-password`  如果是 `yes` 那么忽略

![image-20250109115722248](https://static.litetools.top/blogs/linux_rom/image-20250109115722248.png)

如果是 `PermitRootLogin prohibit-password` 就改成我图中的 `yes`

在vim里面 可以用 (a i o或者其大写做一些插入，新手的话 直接用 `i` 就好了) 然后进入插入模式，然后按 `end`挪光标到末尾，删除`prohibit-password`  然后改成 `yes` 

最后按`ESC` 退出插入模式 然后按 `:` 进入编辑模式 输入 `wq` 保存退出

3. 重启 SSH 服务

```bash
sudo systemctl restart ssh
```



然后接下来我们就可以用 `root` 账号进行登陆了



# 二、挂载磁盘

> 走到这里，下面所有的内容我默认是root权限下运行的了，如果你不是，自己在命令前加 sudo ,下面截图均为示例



## 1. 查看磁盘信息

```bash
df -h
```

![image-20250109134328138](https://static.litetools.top/blogs/linux_rom/image-20250109134328138.png)

可以看到并没有挂载磁盘或者说没有我们目标中的~大磁盘

然后我们查看一下磁盘的信息

```bash
fdisk -l
```

![image-20250109134549771](https://static.litetools.top/blogs/linux_rom/image-20250109134549771.png)

看到我们有一个4T的盘没有挂载，如上示例 `nveme0n1` 即是我们要的盘

如果已经挂载了会有如下情况,下面两个情况都是已经创建了分区

![image-20250109134732240](https://static.litetools.top/blogs/linux_rom/image-20250109134732240.png)

## 2. 分区管理

### 2.1 如果已经有分区 - 删除(可选)

>  可选--我们可以删除分区（*不一定要实现这个操作啊*）

![image-20250109135123019](https://static.litetools.top/blogs/linux_rom/image-20250109135123019.png)

操作完之后 磁盘就是如下情况

![image-20250109135148583](https://static.litetools.top/blogs/linux_rom/image-20250109135148583.png)

### 2.2 没有分区(可选)

1. 创建分区

```bash
fdisk /dev/nvme0n1
```

出来输入行后先输入`n`  即 new 创建分区

后续操作后我们全部默认即可，然后输入 `w`退出，如下

![image-20250109135430019](https://static.litetools.top/blogs/linux_rom/image-20250109135430019.png)

操作完之后可以输入`lsblk` 查看一下 

![image-20250109135519035](https://static.litetools.top/blogs/linux_rom/image-20250109135519035.png)

> 注意这里，可能有的时候默认是2T，根据情况自己操作

**如下情况**

![image-20250109135822725](https://static.litetools.top/blogs/linux_rom/image-20250109135822725.png)

这个是因为磁盘的分区格式问题 之前是 MBR分区，所以我们可以转成GPT分区，这样子可以挂载更大的空间容量

### 2.3更改分区格式（可选）

操作如下：我们先按照上面的流程，`先删除磁盘的分区`，然后我们 使用 `parted`工具将磁盘格式化为GPT

```bash
parted /dev/nvme0n1
```

进入交互页面后输入

```bash
mklabel gpt
```

然后输入 `yes`  然后输入 `quit` 退出

![image-20250109140157319](https://static.litetools.top/blogs/linux_rom/image-20250109140157319.png)

然后我们就可以 继续上面`2.2`的流程 挂载全盘了(就是重新操作一遍)



## 3.格式化分区

1. 格式化为文件系统（ext4）

```bash
mkfs.ext4 /dev/nvme0n1p1
```

2. 创建挂载点

```bash
mkdir -p /mnt/data    # 这里是我创建到这里的，可以自己根据情况创建
```

3. 挂载分区 - 临时挂载分区以验证：

```bash
mount /dev/nvme0n1p1 /mnt/data
```

4. 验证是否挂载成功

```bash
df -h
```

如果出现了如下情况，就是成功了

![image-20250109141650093](https://static.litetools.top/blogs/linux_rom/image-20250109141650093.png)



## 4. 配置开机自动挂载

因为上面是临时挂载，如果电脑重启了，那么就还需要手动挂载一次，所以为了方便，我们都要进行一下开机自动挂载

1. 获取UUID

```bash
blkid /dev/nvme0n1p1
```

输入之后会出现如下情况

`/dev/nvme0n1p1: UUID="1234-ABCD" TYPE="ext4" ...`

我们复制UUID的内容 拼接这个字符串,后面粘贴进fs的文件

```bash
UUID=替换成你的UUID盘id  /mnt/data  ext4  defaults  0  2
```

2. 打开文件

```bash
vim /etc/fstab
```

然后我们刚才组合好的字符串放到文件后面就好了(这里的操作就不教了)

如下

![image-20250109142427534](https://static.litetools.top/blogs/linux_rom/image-20250109142427534.png)

保存退出，

3.校验

```bash
mount -a
```

如果上面的命令，没有报错，则挂载配置完成



# 额外信息

## 下面的内容和本文关系不大

### 只是用作记录备份

方便后面查看

## docker 更改镜像下载目录

因为我们现在有很大的空间了，我们可以把docker的镜像啥的东西搞到我们新弄的磁盘下面了

1. 停止docker（可选，不停也没关系）

```bash
systemctl stop docker
```

2. 创建数据挂载磁盘

```bash
# 假设你想将 Docker 的数据存储到我们的大空间磁盘 /mnt/data/docker，可以创建该目录
# 然后把权限配置好
mkdir -p /mnt/data/docker
chown -R root:root /mnt/data/docker
chmod -R 755 /mnt/data/docker
```

3. 编辑docker的配置文件

```bash
# 文件不存在会自动创建的 你没有动过的话 大概率里面是空的
vim /etc/docker/daemon.json    # 用你喜欢的编辑器就可以  nano 也可以
```

4. 把下面的内容贴进去

```bash
{
  "data-root": "/mnt/data/docker"   # 就是我们上面创建的挂载的目录
}
```

5. 重启docker服务

```bash
systemctl restart docker   # 如果你上面是stop了的 可以试试把restart换成start
```

6. 校验是否成功

```bash
docker info | grep "Docker Root Dir"

# ============ 如果成功的话，你会看到下面的的输出内容
Docker Root Dir: /mnt/data/docker
```

![image-20250109155232104](https://static.litetools.top/blogs/linux_rom/image-20250109155232104.png)

>  到此 docker的镜像下载目录就替换成功了
