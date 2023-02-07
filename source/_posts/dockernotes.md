---
title: 【Docker】万字详细笔记
date: 2023-01-19 18:30:03
tags: docker
categories: 教程
toc: true
---

基本的概念部分就不细说了，容器~ 我们直接从部署到使用学习开始好了。

<!-- more -->

**后面内容部分说明：如果命令前面有 `[root@heartfilia ~]#` 这样子，或者截图里面打了马赛克的部分，这里的命令表示是在宿主主机执行的命令**

**否则为在容器内执行的命令~**



# 一、基础

## 1. docker和虚拟机区别



> 传统的虚拟机方案

![image-20230118163412308](https://static.litetools.top/blogs/docker_notes/image-20230118163412308.png)

虚拟机技术缺点:

1. 资源暂用比较多
2. 冗余步骤多
3. 启动慢

> 容器化技术

**容器化技术不是模拟的一个完整的操作系统**

![image-20230118163853525](https://static.litetools.top/blogs/docker_notes/image-20230118163853525.png)

比较docker和虚拟机技术的不同：

- 传统虚拟机，虚拟出一条硬件，运行一个完整的操作系统，在这个系统上安装和运行软件
- 容器内的应用直接运行在宿主机的内核，容器是没有自己的内核，也没有虚拟硬件，所以很轻快
- 每个容器间是互相隔离，每个容器内都有一个属于自己的文件系统，互不影响



> DevOps(开发、运维)

**docker可以更快速的交付和部署**

- 传统：一堆帮助文档，安装程序
- Docker: 打包镜像发布测试，一键运行，**更便捷的升级和扩容缩**，更简单的系统运维，更高效的计算资源利用(内核级别的虚拟化， 可以在一个物理机上可以运行很多的容器实例，服务器的性能可以被压榨到极致)



**docker的架构图：**

![image-20230118170123233](https://static.litetools.top/blogs/docker_notes/image-20230118170123233.png)

- 镜像(image)：

docker的镜像好比是一个模板，可以通过这个模板来创建容器服务，通过这个镜像可以创建多个容器，最终的服务或项目运行实在容器中运行

- 容器(container)：

docker利用容器技术，独立运行一个或者一组应用，通过镜像来创建。

启动，停止，删除，这些基本命令运行即可！

目前就可以把这个容器理解为一个简易的linux系统

- 仓库(repository)：

仓库就是存放镜像的地方

仓库分为公有仓库和私有仓库

Docker Hub(默认官方 国外的)

阿里云...等等都有第三方镜像服务

## 2. docker的安装

### 2.1 环境准备

我们目前用`linux` 学习， 在`/` 目录下进行接下来的操作

```shell
[root@heartfilia /]# uname -r
5.10.0-60.18.0.50.r509_2.hce2.x86_64    # 查看一下系统内核版本
```

### 2.2 安装

> 官方的[帮助文档](https://docs.docker.com/engine/install/centos/)很详细，下面的内容均为复制帮助文档里面的

#### 1) 卸载旧版本

```shell
[root@heartfilia /]# yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

#### 2) 通过仓库安装

```shell
# 安装需要的基础包
[root@heartfilia /]# yum install -y yum-utils

# 设置仓库镜像 我们用国内阿里云的镜像
[root@heartfilia /]# yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo   
    # https://download.docker.com/linux/centos/docker-ce.repo   # 这个是国外的 我们要替换一下
    
# 更新yum软件包索引
yum makecache fast
```

#### 3) 默认安装docker

下面是默认安装最新版

```shell
[root@heartfilia /]# yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

> 如果这里报错：`Failed to download metadata for repo`...那么需要改一些东西才可以使用

报错原因:

1. 识别版本异常 我们打开`/etc/yum.repos.d/docker-ce.repo`  会发现 `/$releasever/` 有这个东西，这东西是要你去匹配系统版本的，我这里异常示例

   ![image-20230118182129419](https://static.litetools.top/blogs/docker_notes/image-20230118182129419.png)

2. 所以我们手动修改那个数据为对应版本的系统版本，如你的centos版本号

#### 4) 如果需要安装其它docker版本（执行了3就不用执行这里了）

```shell
[root@heartfilia /]# yum list docker-ce --showduplicates | sort -r

# 示例
docker-ce.x86_64                3:20.10.9-3.el8                 docker-ce-stable
docker-ce.x86_64                3:20.10.8-3.el8                 docker-ce-stable
docker-ce.x86_64                3:20.10.7-3.el8                 docker-ce-stable
docker-ce.x86_64                3:20.10.6-3.el8                 docker-ce-stable
docker-ce.x86_64                3:20.10.5-3.el8                 docker-ce-stable
```

选择你需要安装的版本(: 后面的是版本号) 如我这里选择 `18.09.0` 

> docker-ce 社区版     ee 企业版

```shell
[root@heartfilia /]# yum install docker-ce-18.09.0 docker-ce-cli-18.09.0 containerd.io docker-compose-plugin
```

#### 5) 启动docker

```shell
[root@heartfilia /]# systemctl start docker
```



可以测试一下看看docker详情

```shell
[root@heartfilia /]# docker version

Client:
 Version:           18.09.0
 EulerVersion:      18.09.0.300
 API version:       1.39
 Go version:        go1.17.3
 Git commit:        c0d3c43
 Built:             Wed Feb  9 09:00:41 2022
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.09.0
  EulerVersion:     18.09.0.300
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.17.3
  Git commit:       c0d3c43
  Built:            Wed Feb  9 09:00:41 2022
  OS/Arch:          linux/amd64
  Experimental:     false
 
```



> **其它特殊服务器情况(主流过的国外系统都在官网有教程，我这里是官网没有的教程的服务器)**

我这里服务器是华为的欧拉服务器

![image-20230119084915033](https://static.litetools.top/blogs/docker_notes/image-20230119084915033.png)

需要更改一下源

```shell
[root@heartfilia /]# cd /etc/yum.repos.d
[root@heartfilia /etc/yum.repos.d]# wget https://repo.huaweicloud.com/repository/conf/openeuler_x86_64.repo
[root@heartfilia /etc/yum.repos.d]# yum clean all
[root@heartfilia /etc/yum.repos.d]# yum makecache
```

然后再安装

```shell
[root@heartfilia /]# yum -y install docker
```



#### 6) 测试是否成功

```shell
[root@heartfilia /]# docker run hello-world
```

![image-20230119091001621](https://static.litetools.top/blogs/docker_notes/image-20230119091001621.png)

然后可以通过，以下命令查看运行情况

```shell
[root@heartfilia /]# docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              feb5d9fea6a5        16 months ago       13.3kB
```



#### 7) 卸载docker

具体参照 [官方教程](https://docs.docker.com/engine/install/centos/)最下面移除板块，我这里是`centos` 的移除

```shell
# 卸载依赖
[root@heartfilia /]# yum remove docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-ce-rootless-extras

# 删除资源
[root@heartfilia /]# rm -rf /var/lib/docker
[root@heartfilia /]# rm -rf /var/lib/containerd
```



### 2.3 镜像加速

这里就是可以绑定某个服务商的镜像加速哒，大体都是去 阿里云，腾讯云，百度云，华为云...这些等等这些后台创建了后搜索一下找到配置文件一键配置就好了

搜索 `容器镜像服务` 

### 2.4 底层原理

#### 1) docker run 原理

![image-20230119095853421](https://static.litetools.top/blogs/docker_notes/image-20230119095853421.png)

#### 2) docker工作原理

Docker 是一个`client-server` 结果的系统，Docker的守护进程运行在主机上，通过Socket从客户端访问

`DockerServer`  接收到的Docker-Client指令，就会执行这个命令~

> 下图可以看到 docker容器是和linux服务器是独立的 连通后面再讲

![image-20230119100722712](https://static.litetools.top/blogs/docker_notes/image-20230119100722712.png)



> Docker 为什么比虚拟机快

1. Docker有着比虚拟机更少的抽象层
2. Docker 利用的是宿主机的内核，vm需要GuestOS

![image-20230119100953979](https://static.litetools.top/blogs/docker_notes/image-20230119100953979.png)

所以说，新建一个容器的时候，docker不需要像虚拟机一样重新加载一个操作系统内核，避免引导，虚拟机是需要加载guestos，分钟级别的，而Docker是利用宿主机的操作系统，省略了这个复杂的过程是秒级的~

![image-20230119101610852](https://static.litetools.top/blogs/docker_notes/image-20230119101610852.png)

 

# 二、开始

## 1. Docker 常用命令

> 这里的命令目前是最基础部分，后面会持续拓展，docker命令十分多，先记录常用的

### 1.1 帮助命令

```shell
docker version       # 查看docker相关版本信息
docker info          # 可以查看更加详细的命令 系统级别的信息 镜像和容器的相关信息
docker 命令 --help    # 万能命令 不懂就查的
```

**帮助文档地址**[点这里](https://docs.docker.com/reference/)

**DockerHub**[点这里](https://hub.docker.com/)

### 1.2 镜像命令

下面的可选项只列举了常用的，其它的还有的可以通过 `docker help xxx  或者 docker xxx --help` 来进行查看更多操作或者去帮助文档

#### 1) [docker images](https://docs.docker.com/engine/reference/commandline/images/) 

> **查看所有本地的主机上的镜像**

```shell
   [root@heartfilia ~]# docker images
   REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
   hello-world         latest              feb5d9fea6a5        16 months ago       13.3kB
   # 解释
   镜像的仓库源          镜像的标签            镜像的ID             镜像的创建时间         镜像的大小
   # 可选参数
   -a, --all             # 列出所有的镜像   Show all images (default hides intermediate images)
   -f, --filter filter   # 过滤           Filter output based on conditions provided
   -q, --quiet           # 只显示镜像的id   Only show numeric IDs
```

#### 2) [docker search](https://docs.docker.com/engine/reference/commandline/search/) 

> **搜索镜像**

```shell
[root@heartfilia ~]# docker search mysql
NAME                            DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
mysql                           MySQL is a widely used, open-source relation…   13708               [OK]                
mariadb                         MariaDB Server is a high performing open sou…   5232                [OK]
......
# 可选参数
-f, --filter filter   # 过滤 Filter output based on conditions provided
# 示例
[root@heartfilia ~]# docker search mysql -f=STARS=10000    # 搜索出来的镜像是STARS大于10000的
```

#### 3) [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) 

> **下载镜像**

```shell
[root@heartfilia ~]# docker pull mysql[:TAG]  # 不带tag默认下载最新版 这里的tag一定是dockerhub里面的包有的版本
Using default tag: latest           # 如果不写tag 默认最新版
latest: Pulling from library/mysql  # 
2c57acc5afca: Pull complete         # 下面分层下载 docker image 的核心 联合文件系统
0a990ab965c1: Pull complete 
7acb6a84f0f1: Pull complete 
6a2351a691a4: Pull complete         # 后续如果下载该镜像其它版本，如果某个分层一致将不会重新下载
cdd0aae0ac1a: Pull complete 
......
Digest: sha256:6f54880f928070a036aa3874d4a3fa203adc28688eb89e9f926a0dcacbce3378  # 签名
Status: Downloaded newer image for mysql:latest  
```

#### 4) [docker rmi](https://docs.docker.com/engine/reference/commandline/rmi/) 

> **删除镜像**

```shell
[root@heartfilia ~]# docker rmi -f e982339a20a5         # 这后面的是id 我写的是下载的mysql5.7版本的镜像
Untagged: mysql:5.7
Untagged: mysql@sha256:f04fc2e2f01e65d6e2828b4cce2c4761d9258aee71d989e273b2ae309f44a945
Deleted: sha256:e982339a20a53052bd5f2b2e8438b3c95c91013f653ee781a67934cd1f9f9631
Deleted: sha256:257a40f18bab42740005339d77bddbe7d49ed976e8c000a9ed0f08f7be373289
......

# 其它操作
[root@heartfilia ~]# docker rmi -f $(docker images -aq)    # 删除全部容器  骚操作一
[root@heartfilia ~]# docker rmi -f 容器id 容器id             # 删除多个容器
```



### 1.3 容器命令

> 说明：有镜像才可以创建容器，下载一个centos镜像来测试学习

```shell
[root@heartfilia ~]# docker pull centos
```

#### 1) [docker run](https://docs.docker.com/engine/reference/commandline/run/) 

> **新建容器并启动**

```shell
[root@heartfilia ~]# docker run [可选参数] image

# 可选参数
--name="Name"    容器名字 mysql01  mysql02, 用来区分容器
-d               后台方式运行，类似 nohup
-it              使用交互方式运行，进入容器查看内容
-p               指定容器的端口  -p 8080:8080
    -p ip:主机端口:容器端口
    -p 主机端口:容器端口  (最常使用)
    -p 容器端口
    容器端口
-P               随机指定端口，后面不用跟端口
-e               环境配置修改
```

```shell
[root@heartfilia ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
centos              latest              5d0da3dc9764        16 months ago       231MB
[root@heartfilia ~]# docker run -it centos /bin/bash    # 启动并进入容器
[root@cab206d99726 /]#                                  # 看主机名称就知道了进入容器了 这是centos基础版本 很多命令不可用
[root@cab206d99726 /]# exit                             # 退出容器
```

#### 2) [docker ps](https://docs.docker.com/engine/reference/commandline/ps/) 

> **查看当前运行的容器**

```shell
[root@heartfilia ~]# docker ps [可选参数]

# 可选参数
-a               列出当前正在运行的容器+历史运行过的容器
-n=?             显示最近创建的容器
-q               只显示容器的ID 可以组合 -aq 使用
```

#### 3) 退出容器

```shell
exit             # 容器停止并退出
ctrl + p + q     # 容器退出但不停止
```

#### 4) [docker rm](https://docs.docker.com/engine/reference/commandline/rm/)

> **删除容器**

```shell
# 可以直接删除 不在运行的容器
# 可以加上 -f  强制删除正在运行的容器
[root@heartfilia ~]# docker rm 容器id                    # 删除指定的容器(不可删除运行)
[root@heartfilia ~]# docker rm -f $(docker ps -aq)      # 删除所有的容器(运行+历史)
[root@heartfilia ~]# docker ps -a -q | xargs docker rm  # 删除所有的容器(历史)
[root@heartfilia ~]# docker rm -f 运行的容器id            # 删除正在运行的容器(运行+历史)
```

#### 5) 容器状态管理

```shell
[root@heartfilia ~]# docker start 容器id       # 把停止了的容器启动起来(从历史里面获取到)
[root@heartfilia ~]# docker restart 容器id     # 重启容器
[root@heartfilia ~]# docker stop 容器id        # 停止运行的容器
[root@heartfilia ~]# docker kill 容器id        # 强制停止当前容器
```



### 1.4 主要常用命令

#### 1) 后台启动

```shell
# docker run -d 镜像名称     >>> 不加 -d 就是一个前台应用 
[root@heartfilia ~]# docker run -d centos
5c8824348d86f4201280701a12dab7309ab1373a4395b5428773ce6f06d56da3
# 上面命令执行后，查看容器是停止了的，因为创建了打开了，但是没有人用着，就关掉了
# 常见的坑: docker 容器使用后台运行，就需要一个前台进程 类似 systemctl  启动的脚本必须要一直占用前台 否则会很快直接停掉
# nginx 容器启动后，发现自己没有提供服务，就会立刻停止
```

#### 2) 查看日志

```shell
[root@heartfilia ~]# docker logs [可选参数] 容器id

[root@heartfilia ~]# docker logs -t -f --tail 容器id

# 可选参数
-f, --follow         # 动态日志输出 Follow log output  同linux--> tail -f
--tail string        # 尾部打印后面需要跟数字 不加 --tail的话 直接就把全部日志打出来了不友好
-t, --timestamps     # 显示时间 Show timestamps   一般和f组合使用 -tf
```

```shell
# 为了测试日志查看 让这个程序一直运行输出内容
[root@heartfilia ~]# docker run -d centos /bin/sh -c "while true;do echo heartifilia666;sleep 1;done"

# 显示日志
[root@heartfilia ~]# docker logs -tf --tail 10 97f99d8537bd    # 可以循环查看尾部10条内容
2023-01-19T04:04:45.255383970Z heartifilia666
2023-01-19T04:04:46.256875838Z heartifilia666
2023-01-19T04:04:47.258419801Z heartifilia666
......
```

#### 3) 查看进程

```shell
[root@heartfilia ~]# docker top 容器id   # 查看容器内的进程id信息
```

#### 4) [docker inspect](https://docs.docker.com/engine/reference/commandline/inspect/) 【重要】

> 查看容器的信息，元数据

```shell
[root@heartfilia ~]# docker inspect 容器id
```

![image-20230119121510098](https://static.litetools.top/blogs/docker_notes/image-20230119121510098.png)

#### 5) [docker exec](https://docs.docker.com/engine/reference/commandline/exec/)  【重要】

> 进入容器并执行操作

```shell
[root@heartfilia ~]# docker exec -it 容器id /bin/bash
# 注解
-it         以交互方式进入
/bin/bash   用什么shell运行可以改其他的 我这里是bash 因为linux自带的
```

![image-20230119122222769](https://static.litetools.top/blogs/docker_notes/image-20230119122222769.png)

#### 6) [docker attach](https://docs.docker.com/engine/reference/commandline/attach/)

> 进入容器正在运行的状态

```shell
[root@heartfilia ~]# docker attach 容器id
```



> 5和6两点的区别

- docker exec
  - 进入容器后开启一个新的终端，可以在里面操作
- docker attach
  - 进入容器正在执行的终端，不会启动新的进程(容器是否在运行没有关系)

#### 7) [docker cp](https://docs.docker.com/engine/reference/commandline/cp/)

> 从容器内拷贝文件到主机上

```shell
[root@heartfilia ~]# docker cp 容器id:容器内路径 容器外路径   # 拷贝内容和容器是否在运行无关，只要容器在内容就在
```

![image-20230119141656800](https://static.litetools.top/blogs/docker_notes/image-20230119141656800.png)

> 目前拷贝是一个手动过程，后续我们可以使用 `-v` 卷的技术，可以实现，自动同步

**文件操作流程图**

![image-20230119142013844](https://static.litetools.top/blogs/docker_notes/image-20230119142013844.png)

#### 8) [docker stats](https://docs.docker.com/engine/reference/commandline/stats/)

> 查看docker的运行状态

```shell
docker stats [容器id]
```

#### 9) [docker commit](https://docs.docker.com/engine/reference/commandline/commit/)

> 这里在    `二  --> 4 --> 4.3`   板块细说



## 2. Docker练习

### 2.1 安装nginx

![image-20230119144019842](https://static.litetools.top/blogs/docker_notes/image-20230119144019842.png)

**端口暴露原理如图**

![image-20230119144553449](https://static.litetools.top/blogs/docker_notes/image-20230119144553449.png)

![image-20230119145502033](https://static.litetools.top/blogs/docker_notes/image-20230119145502033.png)



### 2.2 安装tomcat

```shell
[root@heartfilia ~]# docker run -it --rm tomcat:9.0   # 按照官方文档下面的操作  https://hub.docker.com/_/tomcat

# 之前启动都是后台，停止了容器之后，容器还是可以查到   加了 --rm 这个操作就是用完即删  一般测试用

# 我们平时不建议用完即删 我们先直接下载最新版  默认是精简版 很多东西是没有的哦~
[root@heartfilia ~]# docker pull tomcat

# 查看镜像
[root@heartfilia ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
tomcat              9.0                 aa0e5599989e        5 days ago          477MB
tomcat              latest              ad4994520144        5 days ago          475MB
nginx               latest              a99a39d070bf        8 days ago          142MB
centos              latest              5d0da3dc9764        16 months ago       231MB

# 启动容器
[root@heartfilia ~]# docker run -d -p 12345:8080 --name tomcat01 tomcat
# 因为我们有两个不同版本的镜像，最后tomcat没有加tag  所以默认就是通过 latest 的版本镜像创建容器

# 新开一个终端测试 或者开了安全组端口的话 可以直接浏览器测试
[root@heartfilia ~]# curl http://127.0.0.1:12345      # 直接返回了内容就是成功   
```



### 2.3 部署ES + Kibana

#### 1) 安装ES

```shell
# ES 暴露的端口很多
# ES 十分消耗内存                   : 启动了就会很卡 需要解决
# ES 的数据一般需要放置到安全目录挂载

# hub下面的启动教程  --net somenetwork  后面在网络板块细说，这里比较复杂
# docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:tag

# 我们不管网络 先这样子启动
[root@heartfilia ~]# docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.8

# 测试es是否成功 如果成功了 马上关闭 我们需要增加内存限制
# -e 环境配置修改  -Xms 最小占用  -Xmx 最多占用
[root@heartfilia ~]# docker run -d --name elasticsearch02 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms512m -Xmx1024m" elasticsearch:7.17.8
```

#### 2) 安装Kibana

 ```shell
 自己安装一下就好了 但是和es配对后面再讲，讲完了改这里~
 ```



### 思考一下

是否可以在本机部署服务然后利用容器内的`nginx`来控制呢?    (-v 卷技术在后面等我们呢)

以后部署项目，每次都要进入容器是不是十分麻烦？(要是可以在容器外部提供一个映射路径，我们在外部修改项目，自动同步到内部就好~同理还是 -v 卷技术)



## 3. 可视化

### 3.1 portainer (临时)

>不是最好的选择，但是目前我们先用这个

#### 1) 开始

```shell
[root@heartfilia ~]# docker run -d -p 8088:9000 --restart=always -v /var/run/docker.sock:/var/run/docker.dock --privileged=true portainer/portainer
```

#### 2) 额外说的

**一般不会使用可视化面板，测试玩一玩就可以了**



### 3.2 **Rancher** (CI/CD 时候使用)

> 先放着



## 4. docker镜像

### 4.1 镜像是什么

docker镜像是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如匿名卷、环境变量、用户等）；镜像不包含任何动态数据，其内容在构建之后也不会被改变。

所有的应用，直接打包docker镜像，可以直接跑起来~

如何得到镜像:

- 远程仓库下载
- 朋友拷贝
- 自己制作一个镜像DockerFile



### 4.2 Docker镜像加载原理

> UnionFS (联合文件系统)

我们下载镜像的时候看到一层一层的下载就是这东西~

**UnionFs**: UnionFS 时一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下。
**特性**： 一次同时加载多个文件系统，但从外面看起来，只能看到一个文件系统，联合加载会把各层文件系统叠加起来，这样最终的文件系统会包含所有底层的文件和目录。

> 加载原理

Docker的镜像实际上由一层一层的文件系统组成，这种层级的文件系统UnionFS（联合文件系统）。

**bootfs（boot file system）**：主要包含`bootloader`和kernel（Linux内核），`bootloader`主要是引导加载kernel，Linux刚启动时会加载`bootfs`文件系统，而在Docker镜像的最底层也是`bootfs`这一层，这与我们典型的Linux/Unix系统是一样的，包含boot加载器和内核。当boot加载完成之后，整个内核就都在内存中了，此时内存的使用权已由`bootfs`转交给内核，此时系统也会卸载`bootfs`。【系统启动需要引导加载】

即：系统启动时需要的引导加载，这个过程会需要一定时间。就是黑屏到开机之间的这么一个过程。电脑、虚拟机、Docker容器启动都需要的过程。在说回镜像，所以这一部分，无论是什么镜像都是公用的。

**rootfs（root file system）**：`rootfs`在`bootfs`之上。包含的就是典型Linux系统中的`/dev`，`/proc`，`/bin`，`/etc`等标准目录和文件。`rootfs`就是各种不同的操作系统发行版，比如`Ubuntu`，`Centos`等等。

**即**：镜像启动之后的一个小的底层系统，这就是我们之前所说的，容器就是一个小的虚拟机环境，比如Ubuntu，Centos等，这个小的虚拟机环境就相当于rootfs。

![image-20230119163633975](https://static.litetools.top/blogs/docker_notes/image-20230119163633975.png)

> 根据架构图来深度理解一下

所有的Docker镜像都起始于一个基础镜像层，当进行修改或增加新的内容时，就会在当前镜像层之上，创建新的镜像层。

举一个简单的例子，假如基于Ubuntu Linux 16.04创建一个新的镜像，这就是新镜像的第一层；如果在该镜像中添加Python包，就会在基础镜像层之上创建第二个镜像层；如果继续添加一个安全补丁，就会创建第三个镜像层。

该镜像当前已经包含3个镜像层，如下图所示（这只是一个用于演示的很简单的例子）。

![image-20230119164503363](https://static.litetools.top/blogs/docker_notes/image-20230119164503363.png)

在添加额外的镜像层的同时，镜像始终保持是当前所有镜像的组合，理解这一点非常重要。下图中举了一个简单的例子，每个镜像层包含3个文件，而整体的镜像包含了来自两个镜像层的6个文件

![image-20230119164826939](https://static.litetools.top/blogs/docker_notes/image-20230119164826939.png)

上图中的鏡像层跟之前图中的略有区别，主要目的是便于展示文件。

下图中展示了一个稍微复杂的三层镜像，在外部看来整个镜像只有6个文件，这是因为最上层中的文件7是文件5的一个更新版本。

![image-20230119164853554](https://static.litetools.top/blogs/docker_notes/image-20230119164853554.png)

这种情况下，上层镜像层中的文件覆盖了底层镜像层中的文件。这样就使得文件的更新版本作为一个新镜像层添加到镜像当中。
Docker通过存储引擎（新版本采用快照机制）的方式来实现镜像层堆栈，并保证多镜像层对外展示为统一的文件系统。

![image-20230119165211018](https://static.litetools.top/blogs/docker_notes/image-20230119165211018.png)

> 特点

docker 的镜像是只读的，容器启动时，一个新的可写层被加载到镜像的顶部，这一层就是容器层，容器之下的都叫镜像层

![image-20230119165325057](https://static.litetools.top/blogs/docker_notes/image-20230119165325057.png)



### 4.3 提交镜像

> docker commit

```shell
docker commit 提交容器称为一个新的副本

# 类似 git
docker commit -m="提交的描述信息" -a="作者" 容器id 目标镜像名[:TAG]

# 示例
[root@heartfilia ~]# docker ps                <<< 查看当前正在运行的容器
CONTAINER ID    IMAGE    COMMAND                CREATED        STATUS         PORTS       
0d70b0d1c73b    tomcat    "catalina.sh run"     5 minutes ago  Up 5 minutes   8080/tcp      
# 直接用改修改好了的容器创建镜像 -a=添加了作者 -m=添加了描述 选中的容器id 最后改了一个名字:也打了一个版本号
[root@heartfilia ~]# docker commit -a="Heartfilia" -m="addHTMLtoWebapps" 0d70b0d1c73b tomcat02:1.0   
sha256:05cfa5fb825aa4694e7f7818ccb63541d5a72c46a7be9532339f06d096415582
[root@heartfilia ~]# docker images  # 查看一下就可以看到我基于另外一个版本添加了内容的镜像在这里了
REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
tomcat02              1.0                 05cfa5fb825a        5 seconds ago       479MB
tomcat                latest              ad4994520144        5 days ago          475MB

# 如果想要保存当前容器的状态，就可以通过commit来提交，获得一个镜像  就和VM虚拟机的快照 一样的意思
```

>到这里，docker才算入门~

# 三、进阶【重点】

## 1. 容器数据卷

### 1.1 概念

如果数据在容器中，容器删除，数据就会丢失~   需求: **数据可以持久化**

MySQL的容器，容器删了，删库跑路？                需求: **MySql数据可以存储在本地**

所以：卷技术就是容器之间数据共享的技术，Docker容器中产生的数据，同步到本地

这就是卷技术，目录的挂载，将我们容器内的目录，挂载到linux上面~

![image-20230119172954403](https://static.litetools.top/blogs/docker_notes/image-20230119172954403.png)

**总结**：容器的持久化和同步操作，容器间也可以数据共享。

### 1.2 使用数据卷

> 方式一: 直接使用命令来挂载   -v

```shell
[root@heartfilia ~]# docker run -it -v 主机目录:容器内目录

[root@heartfilia ~]# ls /home       # 查看了本机home目录下东西 我这里是什么也没有
[root@heartfilia ~]# docker run -it -v /home/test:/home centos bin/bash    # 将启动的centos容器的home目录和本机/home/test绑定
[root@8343edc3791d /]# cd home
[root@8343edc3791d home]# ls       # 查看目前也没有什么东西
```

我们关注一下 docker的信息

```shell
[root@heartfilia ~]# docker inspect 8343edc3791d
# 下面有个 Mounts 配置信息 大概如下
"Mounts": [
    {
    "Type": "bind",
    "Source": "/home/test",
    "Destination": "/home",
    "Mode": "",
    "RW": true,
    "Propagation": "rprivate"
    }
]
```

**弄好了后，在容器里面或者主机上面添加删除内容，两边都是同步的~**

哪怕容器关闭了，我们在主机上操作文件后，容器打开也是可以同步看到，因为是映射关系~



**好处**：我们以后修改只需要在本地修改即可，容器内会自动同步

> 方式二:  docker volumes    后面具名，匿名挂载部分讲解
>
> 

### 1.3 实战练习

#### Mysql安装配置

1. 拉取[mysql镜像](https://hub.docker.com/_/mysql)

```shell
[root@heartfilia ~]# docker pull mysql    # 我直接用最新版了 反正是测试玩
```

2. 通过绑定配置文件启动

```shell
# 配置文件  数据文件 绑定了   还有配置mysql密码 这里是从mysql官方镜像下面的教程里面copy的
[root@heartfilia ~]# docker run -d -p 3306:3306 -v /home/mysql/conf:/etc/mysql/conf.d -v /home/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456789 --name mysql01 mysql
```



### 1.4 挂载模式

> 具名和匿名挂载，后面跟了中文的是用的多的，其他的可以点击进官网查看

- **docker volume**
  - [docker volume create](https://docs.docker.com/engine/reference/commandline/volume_create/)
  - [docker volume inspect](https://docs.docker.com/engine/reference/commandline/volume_inspect/) :后跟卷名可以查看详细信息
  - [docker volume ls](https://docs.docker.com/engine/reference/commandline/volume_ls/) :查看所有卷情况
  - [docker volume prune](https://docs.docker.com/engine/reference/commandline/volume_prune/)
  - [docker volume rm](https://docs.docker.com/engine/reference/commandline/volume_rm/)

#### 1) 匿名挂载

```shell
-v 容器内路径

docker run -d -P --name nginx01 -v /etc/nginx nginx

[root@heartfilia ~]# docker run -d -P --name nginx01 -v /etc/nginx nginx   # 按照这种方式只指定了容器内位置，没有指定容器外路径
f47dba795bc6757938e30fa3cb8c2fbc84a1c7737e0730fea33886afd878e7c6
[root@heartfilia ~]# docker volume ls
DRIVER              VOLUME NAME
local               7a4b62df4e73c69aa029ebda06aba792c44092322a7f05faea87bd3c1a92e610   # 这样子的就是匿名的
...
```

#### 2) 具名挂载

```shell
 # 注意这里是取名字，没有弄  /juming-nginx 这个斜杠 所以这不是一个目录啊
[root@heartfilia ~]# docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx nginx
6c7a1c7d3b3efdfdf2358d2f93b3ea57bf40901c5744b71a7388bcb019dce310
[root@heartfilia ~]# docker volume ls
DRIVER              VOLUME NAME
local               7a4b62df4e73c69aa029ebda06aba792c44092322a7f05faea87bd3c1a92e610   # 开始匿名方式启动后生成的
local               juming-nginx                                                       # 具名模式启动的
...

# 通过 -v  卷名:容器内路径
# 可以通过 docker volume inspect 卷名 查看详细信息
```

![image-20230120093652832](https://static.litetools.top/blogs/docker_notes/image-20230120093652832.png)

>  所有docker容器内的卷，没有指定目录的情况下都是在 `/var/lib/docker/volumes/xxxxxxxx/_data` 这个目录下

我们通过具名挂载可以方便的找到我们的一个卷，大多数情况下试用 **`具名挂载`**

```shell
# 如何确定是具名挂载还是匿名挂载，还是指定路径挂载
-v 容器内路径             # 匿名挂载
-v 卷名:容器内路径        # 具名挂载
-v /宿主机路径:容器内路径  # 指定路径挂载
```

#### 3) 拓展

>  **通过-v 容器内路径:`ro`/`rw` 改变读写权限**

```bash
ro  readonly    # 只读    --> 容器对我们挂载出来的内容有限定，容器内就不可以操作，只能通过宿主机操作改变
rw  readwrite   # 可读可写
[root@heartfilia ~]# docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx:ro nginx
[root@heartfilia ~]# docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx:rw nginx
```

### 1.5 初识DockerFile

> 构建docker镜像的构造文件

**关键词命令都是大写的**

```shell
[root@heartfilia ~]# cd /home
[root@heartfilia home]# ls
mysql  test
[root@heartfilia home]# mkdir docker_test_volume    # 在home目录随便创建一个目录 我们在里面写dockerfile
[root@heartfilia home]# cd docker_test_volume/  
[root@heartfilia docker_test_volume]# vim dockerfile1  # 创建一个dockerfile文件 名字随意 建议>>>>Dockerfile

# 下面在vim里面写了测试
FROM centos

VOLUME ["volume01", "volume02"]      # 这里是匿名挂载

CMD echo "----end-----"
CMD /bin/bash
# 上面是vim文件里面写的东西 用于测试  

#                                                                    这里不加:tag默认最新  这里点别漏了
[root@heartfilia docker_test_volume]# docker build -f dockerfile1 -t heartfilia/centos .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM centos
 ---> 5d0da3dc9764
Step 2/4 : VOLUME ["volume01", "volume02"]
 ---> Running in b5a781bf9802
Removing intermediate container b5a781bf9802
 ---> d0354d969df1
Step 3/4 : CMD echo "----end-----"
 ---> Running in be25fd844b25
Removing intermediate container be25fd844b25
 ---> 7af48f697947
Step 4/4 : CMD /bin/bash
 ---> Running in 12d2cc9f8880
Removing intermediate container 12d2cc9f8880
 ---> 4ec26fdbf056
Successfully built 4ec26fdbf056
Successfully tagged heartfilia/centos:latest
```

![image-20230120102003424](https://static.litetools.top/blogs/docker_notes/image-20230120102003424.png)

我们可以通过 `docker inspect 容器id` 查看一下 `Mounts` 挂载的两个目录，测试一下在容器内修改内容 容器外的目录内容情况

未来使用这种方式非常多，因为我们会经常构建自己的镜像

**如果构建容器的时候没有挂载卷，我们仍然可以采用** `-v 卷名:容器内路径`来手动挂载



### 1.6 数据卷容器

多个容器内进行沟通，数据同步

![image-20230120102751642](https://static.litetools.top/blogs/docker_notes/image-20230120102751642.png)

```shell
# 启动几个容器，用我们自己的镜像启动
# 写/bin/bash是规定镜像启动时执行这条指令，centos镜像启动时默认会启动并执行/bin/bash 所以可以不写

# 第一个创建的相当于是父容器
[root@heartfilia ~]# docker run -it --name docker01 heartfilia/centos
>>> 执行 ctrl + p + q  先退出一下 不退出也没有关系 新开一个窗口也可以
# 创建第二个容器和docker01的容器卷同步
[root@heartfilia ~]# docker run -it --name docker02 --volumes-from docker01 heartfilia/centos

# 删除父容器，其它容器的内容还在
```

多个mysql数据共享

```shell
[root@heartfilia ~]# docker run -d -p 3306:3306 -v /home/mysql/conf:/etc/mysql/conf.d -v /home/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456789 --name mysql01 mysql

[root@heartfilia ~]# docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456789 --name mysql02 --volumes-from mysql01 mysql

# 这个时候可以实现两个容器数据同步
```

结论：

容器之间配置信息的传递，数据卷容器的声明周期一直持续到没有容器使用为止。但是一旦持久化到了本地，这个时候，本地数据不会删除



## 2. DockerFile

### 2.1 构建步骤

1. 编写`dockerfile`文件
2. [docker build](https://docs.docker.com/engine/reference/commandline/build/) 构建成一个镜像
3. docker run 运行镜像
4. [docker push](https://docs.docker.com/engine/reference/commandline/push/) 发布镜像 (`DockerHub`、私有云仓库)
   - 官方放到github的 所以我们也可以按照这样子



很多官方镜像都是基础包，很多功能是没有的，我们通常会自己搭建自己的镜像



### 2.2 构建过程

#### 1) 基础知识

1. 每个保留关键字(指令) 建议都是大写字母
2. 指令从上到下顺序执行
3. `#` 表示注释
4. 每一条指令都会创建一个新的镜像层，并提交。



#### 4) 完整流程

`DockerFile` : 构建文件，定义了一切步骤

`DockerImages` : 通过`DockerFile`构建生成的镜像，最终发布和运行的产品

`DockerContainer` : 容器就是镜像运行起来提供的服务器



### 2.3 指令

![image-20230120111144095](https://static.litetools.top/blogs/docker_notes/image-20230120111144095.png)

```dockerfile
FROM          # 基础镜像，一切从这里开始构建
MAINTAINER    # 镜像是谁写的 姓名+邮箱
RUN           # 镜像构建的时候需要运行的命令
ADD           # 步骤:如tomcat镜像，这个tomcat压缩包添加内容
WORKDIR       # 镜像的工作目录
VOLUME        # 挂载的目录     没有写 -v
EXPOSE        # 对外暴露的端口  没有写 -p
CMD           # 指定这个容器启动的时候要运行的命令---**只有最有一个会生效**，可被替代
ENTRYPOINT    # 指定这个容器启动的时候要运行的命令---可以追加命令
ONBUILD       # 当构建一个被继承 DockerFile 这个时候就会运行 ONBUILD 的指令， 触发指令
COPY          # 类似ADD,  将我们文件拷贝到镜像中
ENV           # 构建的时候设置环境变量
```



#### 1) 构建`centos`测试

> Docker Hub 中99%镜像都是从 `scratch` 开始的

1. 编写文件

```shell
[root@heartfilia dockerfile]# pwd
/home/dockerfile    # 在这里vim 编辑一个文件  my_centos 
[root@heartfilia dockerfile]# cat my_centos 
FROM centos:7    # 用最新版构建后面yum那里可能会有问题我这里用:7
MAINTAINER heartfilia<xxxxxx@qq.com>

ENV MYPATH /usr/local     
WORKDIR $MYPATH                # 进入镜像就直接在这个目录

RUN yum -y install vim
RUN yum -y install net-tools

EXPOSE 80

CMD echo $MYPATH
CMD echo "------end------"
CMD /bin/bash
```

2. 构建镜像

```shell
docker build -f docker文件路径 -t 镜像名[:tag] .
[root@heartfilia dockerfile]# docker build -f my_centos -t my_centos:0.1 .    # 顺道构建一个版本
...

```

#### 2) [docker history](https://docs.docker.com/engine/reference/commandline/history/)

> 可以查看镜像的构建过程

```shell
docker history 镜像id


[root@heartfilia dockerfile]# docker history 1c878dfb0177
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
1c878dfb0177        17 minutes ago      /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "/bin…   0B                  
0d24f471f674        17 minutes ago      /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "echo…   0B                  
1f4d427b4cd2        17 minutes ago      /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "echo…   0B                  
0ed494b81565        17 minutes ago      /bin/sh -c #(nop)  EXPOSE 80                    0B                  
a1ee056b98ba        17 minutes ago      /bin/sh -c yum -y install net-tools             194MB               
5eb496b87336        17 minutes ago      /bin/sh -c yum -y install vim                   249MB               
de993362f7af        18 minutes ago      /bin/sh -c #(nop) WORKDIR /usr/local            0B                  
9790ee2442c8        18 minutes ago      /bin/sh -c #(nop)  ENV MYPATH=/usr/local        0B                  
66907b7e5f02        18 minutes ago      /bin/sh -c #(nop)  MAINTAINER heartfilia<xxx…   0B                  
eeb6ee3f44bd        16 months ago       /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                  
<missing>           16 months ago       /bin/sh -c #(nop)  LABEL org.label-schema.sc…   0B                  
<missing>           16 months ago       /bin/sh -c #(nop) ADD file:b3ebbe8bd304723d4…   204MB
```

我们平时拿到一个镜像可以用上面指令研究一下别人怎么做的

#### 3) CMD 和 ENTRYPOINT 区别

1. CMD

```shell
容器启动的时候要运行的命令   只有最有一个会生效

[root@heartfilia dockerfile]# cat docker_cmd_test 
FROM centos 
CMD ["ls", "-a"]                  # 写了如下内容
[root@heartfilia dockerfile]# docker build -f docker_cmd_test -t cmdtest .
Sending build context to Docker daemon  3.072kB
Step 1/2 : FROM centos
 ---> 5d0da3dc9764
Step 2/2 : CMD ["ls", "-a"]
 ---> Running in 114d93dd5b25
Removing intermediate container 114d93dd5b25
 ---> 8d959d187517
Successfully built 8d959d187517
Successfully tagged cmdtest:latest
[root@heartfilia dockerfile]# docker run 8d959d187517
.
..
.dockerenv
bin
dev
etc
home
......

但是执行下面操作 就是追加命令操作会报错
```

![image-20230120150337717](https://static.litetools.top/blogs/docker_notes/image-20230120150337717.png)



2. ENTRYPOINT

```shell
[root@heartfilia dockerfile]# cat docker_entrypoint_test 
FROM centos
ENTRYPOINT ["ls", "-a"]
[root@heartfilia dockerfile]# docker build -f docker_entrypoint_test -t entorypoint_test .
Sending build context to Docker daemon  4.096kB
Step 1/2 : FROM centos
 ---> 5d0da3dc9764
Step 2/2 : ENTRYPOINT ["ls", "-a"]
 ---> Running in e63f01af5768
Removing intermediate container e63f01af5768
 ---> 07631667be94
Successfully built 07631667be94
Successfully tagged entorypoint_test:latest
[root@heartfilia dockerfile]# docker run 07631667be94
.
..
.dockerenv
bin
dev
etc
home
......

到这里和CMD输出结果都是一致的  不同在追加命令
```

![image-20230120150557540](https://static.litetools.top/blogs/docker_notes/image-20230120150557540.png)



>  Dockerfile中很多命令都十分相似，我们需要了解他们的区别，最好的学习方法就是对比然后测试结果

#### 4) 构建`tomcat`测试

1. 准备镜像文件 tomcat 压缩包，jdk压缩包（我这里网络不好就没有下载 直接用截图了）

![image-20230120152053420](https://static.litetools.top/blogs/docker_notes/image-20230120152053420.png)

2. 编写dockerfile文件，官方命名 `Dockerfile` ,如果用这个 build的时候就会自动去用这个文件 就不用 `-f dockerfile名字`了

```shell
FROM centos:7
MAINTAINER heartfilia<xxxxx@qq.com>

COPY README.md /usr/local/README.md
ADD jdk-8u11-linux-x64.tar.gz /usr/local/      # 用ADD会自动解压缩
ADD apache-tomcat-9.0.22.tar.gz /usr/local/

RUN yum -y install vim

ENV MYPATH /usr/local
WORKDIR $MYPATH

ENV JAVA_HOME /usr/local/jdk1.8.0_11
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/apache-tomcat-9.0.22
ENV CATALINA_BASH /usr/local/apache-tomcat-9.0.22
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin

EXPOSE 8080    # 容器内暴露的端口

CMD /usr/local/apache-tomcat-9.0.22/bin/startup.sh && tail -F /usr/local/apache-tomcat-9.0.22/bin/logs/catalina.out
```

3. 构建镜像

写完了后，因为我们用的官方的标准名称 所以可以如下操作

```shell
[root@heartfilia tomcat]# docker build -t my_tomcat .
```

4. 运行容器

```shell
[root@heartfilia tomcat]# docker run -d -p 6666:8080 --name mytomcat01 -v /home/heartfilia/build/tomcat/test:/usr/local/apache-tomcat-9.0.22/webapps/test -v /home/heartfilia/build/tomcat/tomcatlogs/:/usr/local/apache-tomcat-9.0.22/logs my_tomcat
```

5. 访问测试

```shell
# 可以在index.jsp 里面随便写点东西测试一下  然后访问   http://主机ip:6666/test     # 后续版本这个test要放在ROOT下 index.jsp 和 WEB-INF在同一层
```

6. 发布项目(由于做了卷挂载，我们直接在本地编写项目就可以发布了)
   - 需要注册自己的账号 （dockerhub 板块）
   - 确定可以登录
   - 在服务器上提交自己的镜像

> [docker login](https://docs.docker.com/engine/reference/commandline/login/)


```shell
[root@heartfilia tomcat]# docker login -u 用户名

[root@heartfilia tomcat]# docker push 用户名/镜像名    # 自己发布的镜像尽量带上版本号
```

> [docker tag](https://docs.docker.com/engine/reference/commandline/tag/) : 给镜像打标签和重命名

```shell
[root@heartfilia ~]# docker tag 镜像id 新名字:tag号
```

![image-20230120160335220](https://static.litetools.top/blogs/docker_notes/image-20230120160335220.png)

> 发布到自己的镜像服务的话 我这里直接截图别人的操作了

![image-20230120160844915](https://static.litetools.top/blogs/docker_notes/image-20230120160844915.png)

剩下的直接按照教程就好了~



## 0. 总结

![image-20230120161307998](https://static.litetools.top/blogs/docker_notes/image-20230120161307998.png)



## 3. Docker网络

### 3.1 理解Docker0

> 建议清空所有镜像和容器 来学习理解

![image-20230120162920251](https://static.litetools.top/blogs/docker_notes/image-20230120162920251.png)

```shell
# 我们用一个tomcat 来测试一下
[root@heartfilia ~]# docker run -d -P --name tomcat01 tomcat

# 新版的tomcat下面操作 可能会有错 但是可以解决
[root@heartfilia ~]# docker exec -it tomcat01 ip addr

# 如果出现这种错误，就是新版tomcat没有继承ip相关的工具
OCI runtime exec failed: exec failed: container_linux.go:330: starting container process caused "exec: \"ip\": executable file not found in $PATH": unknown
# 我们需要先进入容器操作以下指令

root@1584d20cbd62:/usr/local/tomcat# apt update
root@1584d20cbd62:/usr/local/tomcat# apt install -y iproute2
# 然后出去执行上面一次就没有问题了

[root@heartfilia ~]# docker exec -it tomcat01 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
70: eth0@if71: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever

# 可以看到 docker0 是172.17.0.1   创建的容器里面的 是 172.17.0.2
# 测试是否本机可以ping通容器   > 可以
```

>  原理

1. 我们每启动一个docker容器，docker就会给docker容器分配一个`ip`，我们只要安装了docker，就会有一个网卡 `docker0`桥接模式，使用的技术是`veth-pair` 技术

   - 在主机再次用` ip addr` 测试会发现会多一个网络出来

2. 再启动一个容器，发现又多了一对网卡。

   ![image-20230120170617565](https://static.litetools.top/blogs/docker_notes/image-20230120170617565.png)

   - `evth-pair` 就是一对的虚拟设备接口，他们都是成对出现的，一段链接着协议，一段彼此相连
   - 正因为有这个特性，`veth-pair` 充当一个桥梁，链接着各种虚拟网络设备 
   - `OpenStac`, `Docker` 容器之间的链接， `OVS`的链接，都是使用的 `veth-pair` 技术

3. 我们测试容器间是否能相互ping(容器内可能没有这个命令还是得去单独下载`apt install -y iputils-ping`)   ：可以ping通！

![image-20230120171817783](https://static.litetools.top/blogs/docker_notes/image-20230120171817783.png)

4. **结论** :所有的容器不指定网络的情况下，都是`docker0` 路由的，docker会给我们的容器分配一个默认的可用IP

```shell
255.255.0.1/16
00000000.00000000.00000000.00000000
上面是16 所以-->255.255.x.x   就有后面那么多可以用的ip   （大约65535个）
如果是8  那么就是255.x.x.x
如果是24 那么就是 255.255.255.x  就x后面数量的ip  (大约255个)
上面的大约里面得排除一些特殊的哈
```



### 3.2 小结

Docker 使用的`linux`的 桥接， 宿主机中的一个Docker容器的网桥 `docker0`

![image-20230120172638043](https://static.litetools.top/blogs/docker_notes/image-20230120172638043.png)

> Docker 中的所有的网络接口都是虚拟的，虚拟的转发效率高 (内网传递效率快)

只要容器删除，对应的网桥一对就没有了。



### 3.3 --link

就是一个hosts映射, 真实使用的时候**不建议**用这个了操作了，但是原理我们要了解~

>  **思考**: 编写一个微服务，项目不重启，数据`ip`更换，可以通过名字来访问容器？

```shell
[root@heartfilia ~]# docker exec -it tomcat01 ping tomcat02
ping: tomcat02: Name or service not known

# 如上面的情况 我们接下来就是要这样子解决这个问题
[root@heartfilia ~]# docker run -d -P --name tomcat03 --link tomcat01 tomcat   # 这里这样绑定后 我们可以tomcat03 ping tomcat01
dab51eabde246eb7df50f7ab0785ad9763af088735e13f61a6ff33923917521b

# 如果没有ping这个命令记得进去03安装以下  apt update && apt install -y iputils-ping
[root@heartfilia ~]# docker exec -it tomcat03 ping tomcat01
PING tomcat01 (172.17.0.2) 56(84) bytes of data.
64 bytes from tomcat01 (172.17.0.2): icmp_seq=1 ttl=64 time=0.100 ms
64 bytes from tomcat01 (172.17.0.2): icmp_seq=2 ttl=64 time=0.048 ms
......

# 这个是单向的，没有配置的话不行的
```

- [docker network](https://docs.docker.com/engine/reference/commandline/network/) : 可以查看以下操作

![image-20230120174245717](https://static.litetools.top/blogs/docker_notes/image-20230120174245717.png)

 ```shell
 # 可以看到上面的--link的操作实际就是改tomcat03的hosts文件实现的
 [root@heartfilia ~]# docker exec -it tomcat03 cat /etc/hosts    
 127.0.0.1       localhost
 ::1     localhost ip6-localhost ip6-loopback
 fe00::0 ip6-localnet
 ff00::0 ip6-mcastprefix
 ff02::1 ip6-allnodes
 ff02::2 ip6-allrouters
 172.17.0.2      tomcat01 1584d20cbd62
 172.17.0.4      dab51eabde24
 ```



### 3.4 自定义网络

> 查看所有的docker网络

```shell
[root@heartfilia ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
dc3247cafe52        bridge              bridge              local
a58455253718        host                host                local
99178c9c2957        none                null                local

# 解释：
NAME--bridge: 桥接 docker默认，自己创建也使用桥接模式
    --none  : 不配置网络
    --host  : 和宿主机共享网络
    --container :容器网络连通(用的少，局限很大)
```

```shell
# 测试一下  --net bridge  这个就是默认的操作 docker0
[root@heartfilia ~]# docker run -d -P --name tomcat04 --net bridge tomcat

# docker0 特点：默认，域名不能访问，--link可以打通
# 自定义一个网络
[root@heartfilia ~]# docker network create --driver bridge --subnet 192.168.0.0/16 --gateway 192.168.0.1 mynet
e900ee535087966508dcb7e9ee5611d1a540991063a7fa60ae24762ebf2318d7
[root@heartfilia ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
dc3247cafe52        bridge              bridge              local
a58455253718        host                host                local
e900ee535087        mynet               bridge              local
99178c9c2957        none                null                local
```

![image-20230120180209605](https://static.litetools.top/blogs/docker_notes/image-20230120180209605.png)

我们创建好了一个我们自己的网络 后面就可以都用我们自己的网络来操作

```shell
[root@heartfilia ~]# docker run -d -P --name tomcat-net-01 --net mynet tomcat   # 如果是新创建的网络开的第一个服务 这里的ip是192.168.0.2
[root@heartfilia ~]# docker run -d -P --name tomcat-net-02 --net mynet tomcat   # 这里是192.168.0.3
```

> **自己创建的网络是全部都支持的**

```shell
[root@heartfilia ~]# docker exec -it tomcat-net-01 ping tomcat-net-02
[root@heartfilia ~]# docker exec -it tomcat-net-01 ping 192.168.0.3
```



> 好处

- 我们可以redis创建一个网络，mysql创建一个网络，这样子不同集群使用不同网络，保证集群是安全和健康的

### 3.5 网络连通

在不同的网络的容器可以连通,如a容器在自定义网络1  b容器在自定义网络2 这样子的，a容器需要和b容器通信就需要这样子操作

![image-20230202112035204](https://static.litetools.top/blogs/docker_notes/image-20230202112035204.png)

> docker network connect

```shell
[root@heartfilia ~]# docker network connect --help

Usage:  docker network connect [OPTIONS] NETWORK CONTAINER

Connect a container to a network

Options:
      --alias strings           Add network-scoped alias for the container
      --ip string               IPv4 address (e.g., 172.30.100.104)
      --ip6 string              IPv6 address (e.g., 2001:db8::33)
      --link list               Add link to another container
      --link-local-ip strings   Add a link-local address for the container
      
# 连通之后就是将 tomcat01 放到了 mynet 网络下 
# 一个容器两个地址，公网ip，私网ip

# apt install -y iputils-ping   新tomcat镜像无这个工具 需要单独安装
```

```bash
[root@heartfilia ~]# docker exec -it tomcat01 ping tomcat-net-01
ping: tomcat-net-01: Name or service not known                  # 直接访问会报这个错误

[root@heartfilia ~]# docker network connect mynet tomcat01       # 执行这个后 再次访问就通了 就把 网络和容器连接了
[root@heartfilia ~]# docker exec -it tomcat01 ping tomcat-net-01   # tomcat02 还是不能访问成功的 原理是下面图片
PING tomcat-net-01 (192.168.0.2) 56(84) bytes of data.
64 bytes from tomcat-net-01.mynet (192.168.0.2): icmp_seq=1 ttl=64 time=0.061 ms
```

> tomcat01 能和 mynet通信原理

```bash
[root@heartfilia ~]# docker network inspect e900ee535087     # 我们查一下mynet的情况
```

**相当于直接把tomcat01 放到了这个网络里面来实现的**

![image-20230202114255672](https://static.litetools.top/blogs/docker_notes/image-20230202114255672.png)

## 4. 实战

### 4.1 redis集群部署

```shell
[root@heartfilia ~]# docker network create redis --subnet 172.38.0.0/16   # 先创建一个redis专属网卡
```

**然后通过脚本创建六个redis配置**

```bash
[root@heartfilia ~]# 方便复制 我这里直接写这里表示这里是在主机操作的

for port in $(seq 1 6); \
do \
mkdir -p /mydata/redis/node-${port}/conf 
touch /mydata/redis/node-${port}/conf/redis.conf 
cat << EOF >/mydata/redis/node-${port}/conf/redis.conf 
port 6379 
bind 0.0.0.0 
cluster-enabled yes 
cluster-config-file nodes.conf 
cluster-node-timeout 5000 
cluster-announce-ip 172.38.0.1${port} 
cluster-announce-port 6379
cluster-announce-bus-port 16379
appendonly yes
EOF
done
```

![image-20230202121335623](https://static.litetools.top/blogs/docker_notes/image-20230202121335623.png)

**然后通过命令启动六个redis**

```bash
[root@heartfilia ~]# 方便复制 我这里直接写这里表示这里是在主机操作的

for port in $(seq 1 6); \
do \
docker run -p 637${port}:6379 -p 1637${port}:16379 --name redis-${port} \
-v /mydata/redis/node-${port}/data:/data:rw \
-v /mydata/redis/node-${port}/conf/redis.conf:/etc/redis/redis.conf:rw \
-d --net redis --ip 172.38.0.1${port} redis /usr/local/bin/redis-server /etc/redis/redis.conf
done
```

> 如果看到启动后 容器直接失效 可以通过以下命令查看一下情况

```bash

[root@heartfilia ~]# docker start -i 任意一个失效容器id 

查看到报错的情况后修正即可~
```

**我们进入任意一个redis一下，注意很多版本的redis是没有bash的 所以我们要用sh进入**

下面是我们随便进入的一个

```bash
[root@heartfilia ~]# docker exec -it redis-1 /bin/sh
```

**然后我们配置一下集群**

```sh
[redis容器]# redis-cli --cluster create 172.38.0.11:6379 172.38.0.12:6379 172.38.0.13:6379 172.38.0.14:6379 172.38.0.15:6379 172.38.0.16:6379 --cluster-replicas 1
# 然后会看到一堆日志 然后卡住 输入yes 回车即可
```

![image-20230202152449681](https://static.litetools.top/blogs/docker_notes/image-20230202152449681.png)

**链接集群**

```sh
[redis容器]# redis-cli -c    # 链接集群

127.0.0.1:6379> cluster info    # 在redis里输入信息查看一下情况
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_ping_sent:465
cluster_stats_messages_pong_sent:467
cluster_stats_messages_sent:932
cluster_stats_messages_ping_received:462
cluster_stats_messages_pong_received:465
cluster_stats_messages_meet_received:5
cluster_stats_messages_received:932
total_cluster_links_buffer_limit_exceeded:0

127.0.0.1:6379> cluster nodes      # 也可以查看主从关系
04af8aa880076f35c367700ad63768916c7f37ce 172.38.0.14:6379@16379 slave c00fb8dadaba76708410bc681171c956a39d0d00 0 1675322942674 3 connected
09c7cdb66bf87c5d60105d8c8c93cd0dc65ec10f 172.38.0.12:6379@16379 master - 0 1675322942000 2 connected 5461-10922
ce2ec85c83ae7156764b53dded98b4d5ce825435 172.38.0.15:6379@16379 slave edb1280152de757c76666ee2f7825a6653a8fdcc 0 1675322941000 1 connected
edb1280152de757c76666ee2f7825a6653a8fdcc 172.38.0.11:6379@16379 myself,master - 0 1675322940000 1 connected 0-5460
c00fb8dadaba76708410bc681171c956a39d0d00 172.38.0.13:6379@16379 master - 0 1675322942573 3 connected 10923-16383
c9a553fb14c57f38663a0dcc0308f8def7651b6b 172.38.0.16:6379@16379 slave 09c7cdb66bf87c5d60105d8c8c93cd0dc65ec10f 0 1675322941000 2 connecte
```

现在我们先随便存一个数据值试试

```bash
127.0.0.1:6379> set test 123
-> Redirected to slot [6918] located at 172.38.0.12:6379    # 可以看到这个由2号主机处理了数据
OK
```

然后我们新开一个窗口把二号redis给停了

```sh
docker stop redis-2   # 
```

```bash
127.0.0.1:6379> get test
-> Redirected to slot [6918] located at 172.38.0.16:6379    # 可以看到我们数据从6号redis获取的
"123"
172.38.0.16:6379> cluster nodes
# 然后这里可以看到 2号redis已经死掉了  master,fail
09c7cdb66bf87c5d60105d8c8c93cd0dc65ec10f 172.38.0.12:6379@16379 master,fail - 1675323275491 1675323273486 2 connected
ce2ec85c83ae7156764b53dded98b4d5ce825435 172.38.0.15:6379@16379 slave edb1280152de757c76666ee2f7825a6653a8fdcc 0 1675323347000 1 connected
# 我们的6号redis 已经从 slave 变成了 myself,master
c9a553fb14c57f38663a0dcc0308f8def7651b6b 172.38.0.16:6379@16379 myself,master - 0 1675323347000 7 connected 5461-10922
c00fb8dadaba76708410bc681171c956a39d0d00 172.38.0.13:6379@16379 master - 0 1675323348528 3 connected 10923-16383
edb1280152de757c76666ee2f7825a6653a8fdcc 172.38.0.11:6379@16379 master - 0 1675323348729 1 connected 0-5460
04af8aa880076f35c367700ad63768916c7f37ce 172.38.0.14:6379@16379 slave c00fb8dadaba76708410bc681171c956a39d0d00 0 1675323347000 3 connected
```



如果有更多镜像需要管理就需要下面的板块来搞了~



# 四、企业实战


## 1. Docker Compose

...




## 2. Docker Swarm

[大概参考位置](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/)


1. 首先需要多台服务器，最好是在同一内网网段的(公网慢而且说不定要钱)

2. 每台都安装了docker

3. 概念

   - 有两种节点：管理节点(操作都在manager) 和 工作节点(执行worker)

   ![image-20230203092609019](https://static.litetools.top/blogs/docker_notes/image-20230203092609019.png)

   - 一般10台以下可以这么玩，多了就需要k8s了
   - manager要奇数的(类似投票机制 所以**一般**要3以上奇数)

4. 搭建集群开始

### 2.1 命令详解

#### 1) [docker swarm](https://docs.docker.com/engine/reference/commandline/swarm/)

```shell
Usage:  docker swarm COMMAND

Manage Swarm

Commands:
  ca          Display and rotate the root CA
  init        Initialize a swarm
  join        Join a swarm as a node and/or manager
  join-token  Manage join tokens
  leave       Leave the swarm
  unlock      Unlock swarm
  unlock-key  Manage the unlock key
  update      Update the swarm
```

1. 创建一个集群

```shell
[root@ecs1 ~]# docker swarm init --help
Options:  # 下面很多命令 就这个用的多点
      --advertise-addr string                  Advertised address (format: <ip|interface>[:port])
```

然后我们先创建一个manager 主节点

> `docker swarm init`  初始化节点

```shell
[root@ecs1 ~]# docker swarm init --advertise-addr 这台服务器内网ip   # 后面命令不写也可以

Swarm initialized: current node (xxxxxxxxxxxxxxxxxx) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token 一堆串串 这台服务器内网ip:2377      默认2377端口，可以复制这一句就是添加worker到这个集群，后面添加worker需要单独运算一个令牌出来试试

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.    如果要添加

# 如果遇到这种报错
Error response from daemon: --live-restore daemon configuration is incompatible with swarm mode
#解决办法如下：
自己去查 大概率会查到官网这个，但是不一定有用: 
https://forums.docker.com/t/error-response-from-daemon-live-restore-daemon-configuration-is-incompatible-with-swarm-mode/28428
```

> `docker swarm join` 加入一个节点

```shell
# 加入worker节点  我们复制上面返回的 docker swarm join --token 那里在另外一个同内网服务器执行
[root@ecs2 ~]# docker swarm join --token 一堆串串 这台服务器内网ip:2377
# 会得到如下反馈  这个节点就变成了一个worker节点
This node joined a swarm as a worker.
```

我们查看以下1号服务器节点状态

![image-20230203102950814](https://static.litetools.top/blogs/docker_notes/image-20230203102950814.png)

```shell
# 如果我们还要添加工作节点或者主节点 我们需要获取令牌然后在新的服务器执行一下
docker swarm join-token manager    # 在初始化了的那台服务器执行这个后获取到manager的令牌 其它服务器执行令牌后加入manager节点
docker swarm join-token worker     # 在初始化了的那台服务器执行这个后获取到worker的令牌 其它服务器执行令牌后加入worker节点
```




## 3. CI/CD Jenkins 流水线

...



## 0. k8s

容器单独没有什么意义，有意义的是这里需要学习的`k8s`  这个地方后面单独一个版块学习，这个docker部分将不会讲到~

但是学这里需要掌握的东西先准备好：

1. **Go语言** 必须掌握
2. 一些并发语言
