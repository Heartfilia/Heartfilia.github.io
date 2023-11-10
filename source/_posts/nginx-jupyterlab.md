---
title: 【Jupyter】搭配nginx可能出现问题食用方法
tags:
  - jupyter
  - nginx
categories: 教程
toc: false
date: 2023-11-10 23:17:52
---


本篇虽然讲的是jupyterlab出现的问题，但是核心和jupyter是相关的

<!-- more -->

# 大概问题

> 以下问题基本上只会在你用nginx代理服务器的时候jupyterlab会出现的问题



## 1. 打不开内部的终端

这个问题是因为，没有在nginx配置文件里面配置wss相关的属性，所以不能访问。如下修改即可

```nginx
upstream notebook {
    server 127.0.0.1:xxx;
}

server {
  listen       80;
  # listen       [::]:80;
  server_name  xxx.xxxxxx.xxx;   # 域名
  root         /usr/share/nginx/html;

  location ~ /api/kernels/ {
    proxy_pass            http://notebook;
    proxy_set_header      Host $host;

    proxy_http_version    1.1;  # websocket support
    proxy_set_header      Upgrade "websocket";
    proxy_set_header      Connection "Upgrade";
    proxy_read_timeout    86400;
  }

  location ~ /terminals/ {
    proxy_pass            http://notebook;
    proxy_set_header      Host $host;

    proxy_http_version    1.1; 
    proxy_set_header      Upgrade "websocket";
    proxy_set_header      Connection "Upgrade";
    proxy_read_timeout    86400;
  }
  
  # 上面两个是核心操作

  location ~ /lab/api/build {
    proxy_pass            http://notebook;
    proxy_set_header      Host $host;

    proxy_http_version    1.1; 
  }   # 这个加上没有用好像 但是加了也没事

  location / {
    proxy_pass http://notebook;
    proxy_set_header   Host             $host; 
    proxy_set_header   X-Real-IP        $remote_addr; 
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for; 
  }

  # Load configuration files for the default server block.
  include /etc/nginx/default.d/*.conf;

    error_page 404 /404.html;
    location = /40x.html {
		}

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
		}
}
```



## 2. 插件异常

后续异常的时候解决



# 留一句话

真的很好用 `Jupyterlab` 可以研究一下的
