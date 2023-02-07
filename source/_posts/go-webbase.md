---
title: 【Go web】后台框架入门
date: 2023-02-07 09:07:26
tags: go
categories: 框架
toc: true
---

---


逐步更新，但是这里只是入门板块，进阶板块后面会单独章节写。

计划逐步记录的框架 --> Gin、Beego、Iris

<!-- more -->

# 一、框架选择

我们简单了解一下部分后端框架，不是全部，还有很多其他的，目前我们大概了解一下如下框架

1. `Gin` : Go语言编写的Web框架，以更好的性能实现类似`Martini` 框架的API
   - Gin是一个`Golang` 的微框架，封装比较优雅，`API`友好，源码注释比较明确。具有快速灵活，容错方便等特点。
2. `Beego` : 开源的高性能Go语言Web框架
   - `beego` 是一个快速开发Go应用的`http` 框架，go 语言方面技术大牛。`beego` 可以用来快速开发`API、Web、后端` 服务等各种应用，是一个`RESTFul` 的框架，主要设计灵感来源于`tornado` 、`sinatra` 、`flask` 这三个框架，但是结合了Go本身的-一些特性(`interface、struct` 继承等)而设计的一个框架。
3. `Iris` : 全宇宙最快的Go语言Web框架，完备的`MVC` 支持，未来尽在掌握
   - `Iris`是一个快速，简单但功能齐全的和非常有效的web框架，提供了一个优美的表现力和容易使用你的下一个网站或者`API` 的基础



# 二、开始

## Gin

### 1. 安装

```bash
go get -u github.com/gin-gonic/gin
```

> 可能出现网络异常，修复手段如下

#### 1.0 异常

如果没有出现网络异常就可以忽略这里的板块，直接看后面的操作步骤

```bash
# 可以考虑更换一下GOPROXY   下面任选其一
go env -w GOPROXY="https://goproxy.io,direct"
go env -w GOPROXY="https://mirrors.aliyun.com/goproxy,direct"

# 然后包拉取我们得有 gomod 所以在项目文件夹里面操作如下
go mod init

# 一般来说 我们还可以设置 GO111MODULE
go env -w GO111MODULE=on
```

### 2. hello

##### 1) restful基本模板

**目前的目录结构**

```bash
项目名
  |__favicon.ico
  |__go.mod
  |__main.go
```

我们先创建一个最基本的模板

```go
package main

import "github.com/gin-gonic/gin"

// go get github.com/thinkerou/favicon  这个配置网页那个图片的 前后端分离不用管这个
import "github.com/thinkerou/favicon"

func main() {
	// 创建一个服务
	ginServer := gin.Default()
	ginServer.Use(favicon.New("./favicon.ico")) // 我这弄了玩,不用搞这里

	// 这里可以链接数据库 下面操作数据

	// 访问地址，处理我们的请求  Request  Response  下面是restful测试
	ginServer.GET("/", func(context *gin.Context) {
		context.JSON(200, gin.H{"msg": "hello,world"})
	})
	ginServer.POST("/user", func(c *gin.Context) {
		c.JSON(200, gin.H{"msg": "post user"})
	})
	ginServer.PUT("/user", func(c *gin.Context) {
		c.JSON(200, gin.H{"msg": "put user"})
	})
	ginServer.DELETE("/user", func(c *gin.Context) {
		c.JSON(200, gin.H{"msg": "delete user"})
	})

	// 服务器端口
	ginServer.Run(":8888")
}
```

##### 0) pycharm 异常

如果出现以下问题，可以查看一下是否下面两种情况异常，如果没有出现这种异常可以忽略下面操作

1. 首先我们需要在`settings` 里面找到`GOPATH` 把`Index entire GOPATH` 这个选择勾上

![image-20230207105746454](https://static.litetools.top/blogs/gowebbase/image-20230207105746454.png)

2. 然后在`Go Modules` 把我们配置的`GOPROXY` 如图配置上即可

![image-20230207105943968](https://static.litetools.top/blogs/gowebbase/image-20230207105943968.png)

##### 2) 渲染前端

**目前的目录结构**

```bash
项目名
  |__go.mod
  |__main.go
  |__templates
  |  |__index.html
  |__static
    |__css
    |  |__style.css
    |__js
       |__common.js
```



我们创建一个前端模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>我的一个go页面</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <script src="/static/js/common.js"></script>
</head>
<body><h1>大家好啊</h1>
<div>
    我们获取到的后端来的数据是: {{.msg}}    这个就是后端传过来的那个 H{}
</div>
</body></html>
```

前端需要一个`msg`参数 所以我们后端需要传递过来渲染

其中上面前端页面的资源引入这样子写了是不可以直接引用的，还需要go服务那边加载静态文件

```go
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	// 创建一个服务
	ginServer := gin.Default()
	// 加载静态页面 当前是测试后端渲染前端
	ginServer.LoadHTMLGlob("templates/*") // 全局加载
	//ginServer.LoadHTMLFiles("templates/index.html")  // 加载某个文件

	ginServer.GET("/index", func(context *gin.Context) {
		//context.JSON()  // 返回json数据
		context.HTML(http.StatusOK, "index.html", gin.H{
			"msg": "这是go后台传递来的数据",
		})
	})

	// 服务器端口
	ginServer.Run(":8888")
}
```

**测试响应状态**

![image-20230207120719951](https://static.litetools.top/blogs/gowebbase/image-20230207120719951.png)

### 3. 获取参数

下面是几种基础请求方案 从传来的参数获取值 当然判断逻辑那些是在获取参数和返回结果之间处理 这里逻辑就不概述了

```go
package main

import (
	"encoding/json"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	// 创建一个服务
	ginServer := gin.Default()

	// 如参数 url?userId=1&username=heartfilia
	ginServer.GET("/user/info", func(context *gin.Context) {
		userId := context.Query("userId")
		userName := context.Query("username")
		context.JSON(http.StatusOK, gin.H{
			"user_id":   userId,
			"user_name": userName,
		})
	})
	// 如参数 user/info/1/heartfilia
	ginServer.GET("/user/info/:userId/:username", func(context *gin.Context) {
		userId := context.Param("userId")
		userName := context.Param("username")
		context.JSON(http.StatusOK, gin.H{
			"user_id":   userId,
			"user_name": userName,
		})
	})
	// 前端给后端传json
	ginServer.POST("/json", func(context *gin.Context) {
		b, _ := context.GetRawData()
		var m map[string]interface{}
		_ = json.Unmarshal(b, &m) // 序列化包装为json 第一个参数是传入的[]byte
		context.JSON(http.StatusOK, m)
	})

	// 前端给后端传表单 form-data
	ginServer.POST("/form", func(context *gin.Context) {
		userName := context.PostForm("username")
		password := context.PostForm("password")
		context.JSON(http.StatusOK, gin.H{
			"msg":      "ok",
			"username": userName,
			"password": password,
		})
	})

	// 服务器端口
	ginServer.Run(":8888")
}
```

### 4. 路由操作

##### 1) 重定向

```go
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	// 创建一个服务
	ginServer := gin.Default()
	ginServer.LoadHTMLGlob("templates/*") // 全局加载

	// 路由操作 这里是单个操作的 后面会继续
	ginServer.GET("/test", func(context *gin.Context) {
		// 重定向
		context.Redirect(http.StatusMovedPermanently, "https://www.baidu.com")
	})

	// 404 页面 可以自定义那个 404.html里面内容 这里需要先全局加载一下
	ginServer.NoRoute(func(context *gin.Context) {
		context.HTML(http.StatusNotFound, "404.html", nil)
	})
	// 服务器端口
	ginServer.Run(":8888")
}
```

##### 2) 路由组

这里可以将同类型功能单独封装

```go
package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	ginServer := gin.Default()

	// 把大的操作往下拆分 创建各种不同的路由
	userGroup := ginServer.Group("/user")
	{
		userGroup.GET("/add") // 函数这里就不写了 和上面定义的差不多
		userGroup.POST("/login")
		userGroup.GET("/logout")
	}

	orderGroup := ginServer.Group("/order")
	{
		orderGroup.GET("/add")
		orderGroup.GET("/get")
		orderGroup.DELETE("/delete")
	}

	ginServer.Run(":8888")
}
```



### 5. 中间件

对数据预处理，授权验证，统计啥的...

```go
package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
)

// 自定义Go中间件 拦截器
func myHandler() gin.HandlerFunc {
	return func(context *gin.Context) {
		// 通过自定义的中间件，设置的值，在后续处理只要调用了这个中间件的都可以拿到这里的参数
		context.Set("userSession", "user_id-123") //这里可以有各种判断然后由下面的操作判断
		context.Next()                            // 数据如果通过校验，就可以放行
		//context.Abort() // 如果没有通过，就阻断 后面就拿不到这里设置的值之类的
	}
}

func main() {
	ginServer := gin.Default()
	// 注册中间件
	//ginServer.Use(myHandler()) // 这个是全局注册 会对后面所有接口都加上
	//ginServer.GET("/user/info", func(context *gin.Context) {   // 全局注册 就不用在这里写
	ginServer.GET("/user/info", myHandler(), func(context *gin.Context) { // 不全局注册 就在这里写中间件
		//取出中间件里面值
		handlerResult := context.MustGet("userSession").(string)
		log.Println(handlerResult)
		userId := context.Query("user_id")
		context.JSON(http.StatusOK, gin.H{
			"user_id": userId,
		})
	})

	ginServer.Run(":8888")
}

```



## Beego

未完待续......



## Iris

未完待续......
