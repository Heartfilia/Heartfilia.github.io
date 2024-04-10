---
title: 【https】原来自己签https网站这么简单
tags: ssl
categories: 教程
toc: false
date: 2024-04-09 23:44:33
---


自己签https证书

<!-- more -->

很多时候我们访问一些http的网站，浏览器总是会提示我们不安全。我们自己搭建一个博客，由于买不起高贵的ssl证书费用，所以我们大多数时候都是裸奔的http。

今天，我们自己来签，免费的 `https`

# 准备工作

1. 有服务器
2. 有域名



## 工具

我们采用的 [Let's Encrypt - 免费的SSL/TLS证书 (letsencrypt.org)](https://letsencrypt.org/zh-cn/)  这个网站里面的工具，但是里面的东西晦涩难懂，所以我这里直接就讲干的。



## 步骤

1. 安装 `snapd` 工具，后续无脑安装：这个我用的centos，直接`yum install snapd`

   ```bash
   安装操作也可以参考这里: 根据自己的系统选择安装方法即可
   https://snapcraft.io/docs/installing-snapd/
   ```

   

2. 确保你没有安装过旧版的 `certbot`:如果安装了，试试下面的删除方式

   1. `sudo apt-get remove certbot`
   2. `sudo dnf remove certbot`
   3. `sudo yum remove certbot`

3. 然后我们用`snapd`工具安装`certbot`

   ```bash
   sudo snap install --classic certbot
   ```

   ![image-20240409232442552](https://static.litetools.top/blogs/https/image-20240409232442552.png)


4. 安装好了之后绑定一下软连接

   ```bash
   sudo ln -s /snap/bin/certbot /usr/bin/certbot
   ```

   

5. 然后就可以直接一键操作了，因为我用的nginx，并且之前没有`https`，所以我直接一键操作

   > 操作之前可以先备份一下原始的nginx配置文件，以防万一

   ```bash
   sudo certbot --nginx
   ```

   当然也可以只生成证书

   ```bash
   sudo certbot certonly --nginx
   ```

6. 我是无脑操作，操作中会提示你输入一些选项，会自动识别你nginx配置的域名，根据提示操作即可

   ![Snipaste_2024-04-09_23-05-22](https://static.litetools.top/blogs/https/image-20240409232442553.png)

有上面的提示后，就签名成功了，注意你要用`https` ，你的服务器**安全组(防火墙)**，一定要把`443`端口对外开放



## 测试

浏览器直接访问你自己的域名，https访问通过即成功



## 续签

官方推荐以下操作续签

```bash
sudo certbot renew --dry-run
```

可以把上面的指令写进`crontab` 里面每天更新一下,如下：

```bash
0 0 * * * certbot renew --dry-run
```



