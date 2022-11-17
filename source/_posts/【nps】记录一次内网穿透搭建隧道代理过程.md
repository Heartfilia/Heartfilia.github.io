---
title: 【nps】记录一次内网穿透搭建隧道代理过程
date: 2022-11-17 14:46:40
tags: 穿透
categories: 工具
---

# 工具选择
目前市面上有很多这种工具，原理其实都差不多，这里我采用黑哥推荐的 `**nps**`
**github页面地址：**[**点击这里**](https://github.com/ehang-io/nps)

# 准备工作
## 打开官网
> [官方文档地址](https://ehang-io.github.io/nps/#/?id=nps)

这里面其实写的都很详细，但是！！里面很多东西概念很模糊，不理解原理直接看官方文档的话，可能会浪费时间
**所以接下来我们就来理解理解~**
# 原理
**VPS 因为会一直换IP 没有对外使用的公网，所以VPS上面放的是客户端**
**所以我们需要一台有公网的服务器来挂服务端  **所以公网得有，还得开你要开的端口的**安全组**
**客户端和服务端保持链接，由服务端来进行分发**
原理大概如此，接下来就是一些简单的配置操作
# 配置
## 公网服务器-服务端
下载对应系统版本的服务包 然后解压出来，解压出来的东西是可以直接使用的话，如果你要修改配置，可以到**conf**目录下找到`nps.conf`然后在里面修改你想要修改的，这里我就只改web端的密码，其他的不作修改。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787085424-e68602aa-caaf-48c6-9e21-32657950397d.png#averageHue=%2320201f&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=205&id=u60e7967c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=205&originWidth=329&originalType=binary&ratio=1&rotation=0&showTitle=false&size=10450&status=done&style=none&taskId=u7a7a67d8-87cc-462a-bd74-10201703463&title=&width=329)
然后在外面目录下有一个`nps`的可执行文件
我们先按照官网的教程 `nps install` 然后 `nps start`（这个后台启动）或者直接 `nps`这样子可以看见日志，我这里直接用`nps`启动观察日志。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787210655-4133a48d-125a-4eaf-aad3-c2b55f66d230.png#averageHue=%2323477d&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=155&id=u6547fc87&margin=%5Bobject%20Object%5D&name=image.png&originHeight=155&originWidth=724&originalType=binary&ratio=1&rotation=0&showTitle=false&size=174099&status=done&style=none&taskId=u46c67a85-29a7-4875-86e3-9c0d2978808&title=&width=724)
随后通过`公网:端口`访问web页面，登录上后 我们要做的事情很简单，在客户端位置，创建一个东西
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787355961-6fa3385c-8366-4002-b635-d55625710624.png#averageHue=%23fefcfc&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=766&id=u1bce9a49&margin=%5Bobject%20Object%5D&name=image.png&originHeight=766&originWidth=463&originalType=binary&ratio=1&rotation=0&showTitle=false&size=31351&status=done&style=none&taskId=uc7032e95-92ce-450d-bded-b7eabe9279c&title=&width=463)
创建好了后我们点项目前面的 `+`可以展开，下面会有一个客户端命令，这里就是要我们在vps服务器上面启动的东西
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787428391-6a83c875-3e70-4786-9a05-2f28d8aa46a5.png#averageHue=%23d7b889&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=265&id=uc90d3756&margin=%5Bobject%20Object%5D&name=image.png&originHeight=265&originWidth=681&originalType=binary&ratio=1&rotation=0&showTitle=false&size=26455&status=done&style=none&taskId=uada8d4c9-6b4e-46af-8e59-0ea0c470370&title=&width=681)
## VPS-客户端
这边很简单，我们要做的就是

1. 如果要搭建`http`代理的话，我们在web端页面HTTP代理位置新增一个
2. ![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787776039-0f9db4d0-aeba-4505-8ed1-ba2e43d2643b.png#averageHue=%23fefcfb&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=516&id=u6953e955&margin=%5Bobject%20Object%5D&name=image.png&originHeight=516&originWidth=547&originalType=binary&ratio=1&rotation=0&showTitle=false&size=24416&status=done&style=none&taskId=u35520670-206a-42d1-b9bc-e98fe926d97&title=&width=547)
3. vps首先得拨号，有网络才可以
4. 直接执行上面说的客户端命令
5. ![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787871622-251f694b-7eca-4a22-a08f-d3b19e4d00c5.png#averageHue=%23d7bca1&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=126&id=u59fb001e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=126&originWidth=993&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16135&status=done&style=none&taskId=udfe21af3-e3cc-4a43-a3db-8ff0367f3ed&title=&width=993)
6. 如果出现这种就是链接成功了，这个时候web客户端位置会有链接信息

![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667787921190-ad2aa0aa-4f67-48ad-95b8-a769a393444e.png#averageHue=%23e2e4cb&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=120&id=u4058c18e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=120&originWidth=1614&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16711&status=done&style=none&taskId=u89a9206c-17c2-453d-9405-3217130dce2&title=&width=1614)
### 测试一下
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667788043804-1115900f-0262-4194-81d3-58ee010ce32c.png#averageHue=%23323a43&clientId=u98bed93f-60e0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=238&id=u2a4532e8&margin=%5Bobject%20Object%5D&name=image.png&originHeight=238&originWidth=656&originalType=binary&ratio=1&rotation=0&showTitle=false&size=25425&status=done&style=none&taskId=u8509e9d3-96d5-4b63-b18d-79a98bbabf9&title=&width=656)
上面的账号密码就是上面**新增客户端**位置设置的，公网ip后面的端口是后面设置HTTP代理那里设置的**开放的端口**
## 注意：
只要是需要对接的端口，记住需要开放公网服务器的安全组端口，要不然没有网，现在服务器基本都是默认关闭了对应端口的.


# 内网搭建API
## 适合需求
有些时候我们在内网服务器搭建了一个服务，但是我们想让其他人访问，这时候就可以通过这里下面的方案进行别人走一个公网，然后让别人访问到我们要访问的api啥的
## web端配置
### 第一步
我们要在客户端那里建立一个服务，现在这里不要设置账号密码了
别忘记在内网服务器也得执行一个那个**+号**下面的那个命令客户端保持连接哦，如果用了之前的，那么就不用了
### 第二步
我们这次要在**TCP隧道**位置创建一个服务
![image.png](https://cdn.nlark.com/yuque/0/2022/png/2975862/1667967821465-1c37e471-5839-4721-be3d-32922f8d9658.png#averageHue=%23fef9f7&clientId=u7d72f69b-2de0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=593&id=u04efc54d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=593&originWidth=751&originalType=binary&ratio=1&rotation=0&showTitle=false&size=46204&status=done&style=none&taskId=u22ca8cc9-0a0a-48bd-a214-502a1ec4b54&title=&width=751)
### 服务部署
在内网部署一个服务
然后在外面通过公网访问测试一下，ok就没有问题啦

