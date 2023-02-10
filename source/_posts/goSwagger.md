---
title: 【goSwagger】goswagger+gin配置踩坑
date: 2023-02-10 11:14:15
tags: go
categories: 教程
toc: true
---



搭建一个swagger页面 手把手教学

<!-- more -->

# 一、基本介绍

## 1. 页面展示

> 最终页面

![image-20230209164726860](https://static.litetools.top/blogs/goswagger/image-20230209164726860.png)

我们将用上面的几个例子来展示一下几种普通请求的使用方式，然后再**稍微** 讲一下常用的一些参数，其它参数我代码里面不会展示，但是可以尝试配置一下，逻辑一样的。

> 代码层级

![image-20230209165144727](https://static.litetools.top/blogs/goswagger/image-20230209165144727.png)

# 二、实战

## 1. 开始

[**官方文档地址**](https://swagger.io/docs/specification/about/)

[**快速查询中文文档**](https://github.com/swaggo/swag/blob/master/README_zh-CN.md) : github的，可以查查



### 1.1 安装goswagger

```bash
# 我们先安装swag  这个地方有个坑
go get -u github.com/swaggo/swag/cmd/swag
```

> 如果上面安装了但是`swag.exe` 不在 `GOPATH/bin` 里面那么就需要执行下面操作

安装完了之后，如果`swag` 这个命令还不可以使用，这时候我们需要去到`GOPATH/pkg/mod/github.com/swaggo/swag@版本号` 这个位置执行一下`go install` 然后我们重启一下`cmd` 尝试一下是否可以返回版本号

```bash
swag -v
# 正常会直接返回一行版本信息
```



然后我们继续安装其它包

```bash
go get -u github.com/swaggo/gin-swagger
go get -u github.com/swaggo/gin-swagger/swaggerFiles
```



### 1.2 目录介绍

这里项目名称我是随意写的，我这里是`webbase` 然后这个东西在`GOPATH/arc/LearnTest` 下面，所以后面很多包的引用目录位置是从`LearnTest/webbase/xxxxx` 这样子的

#### 1) main.go

**这里只负责启动路由**，下面我写了很多注释在文件开头，这里我会和图片一起对照讲解。

| 注解           | 描述                                                    |
| -------------- | ------------------------------------------------------- |
| title          | **必需的。**应用程序的标题。                            |
| version        | **必需的。**提供应用程序API的版本                       |
| description    | 应用程序的简短描述。                                    |
| termsOfService | API的服务条款。                                         |
| contact.name   | 公开的API的联系信息。                                   |
| contact.url    | 指向联系信息的URL。必须采用网址格式。                   |
| contact.email  | 联系人/组织的电子邮件地址。必须采用电子邮件地址的格式。 |
| license.name   | **必需的。**用于API的许可证名称。                       |
| license.url    | 用于该API的许可证的URL。必须采用网址格式。              |
| host           | 提供API的主机（名称或IP）。                             |
| BasePath       | 提供API的基本路径。                                     |

```go
// @title 我的测试网站
// @version 1.0
// @description 这是我的api测试网站
// @termsOfService http://swagger.io/terms/

// @contact.name Heartfilia
// @contact.url https://heartfilia.github.io
// @contact.email xxxxxx@qq.com

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host 192.168.1.115:8888
// @BasePath
package main

import (
	"LearnTest/webbase/router"
)

func main() {
	router.Routers()
}
```

![image-20230209172213249](https://static.litetools.top/blogs/goswagger/image-20230209172213249.png)

这里有些东西不是必须写的 我这里写了四个板块(用换行符分割的)。这里面只要呈现了超链接样子的东西都可以不写的。核心是最后那个`host`

1. 如果你是放在有`nginx `服务的地方的话这里写`127.0.0.1:xxxx` **完全没有问题**，那么你将碰不到任何错误

2. 如果是**单机测试**，你写`127.0.0.1:xxxx` 也**没有任何问题**，访问也不会出错

3. 如果你写了`127.0.0.1:xxxx` 然后要给**内网**小伙伴玩，那么你会遇到如下问题，他用内网IP访问你的服务，swagger页面可以打开，但是api服务访问会出现`CORS`问题。

4. 如果你写了`内网ip:xxxx` 然后给内网小伙伴玩，那么一般是不会遇到任何问题的。但是，此时你自己用`127.0.0.1:xxxx` 去访问，你自己又会碰到`CORS`错误。这时候我们可以利用添加一个`CORS` 中间件来处理这个问题，下一个板块我就会写到，因为里面没啥东西讲的，先写前面。

   - 添加中间件后，我们测试访问`GET` 请求没问题，`POST json`数据依旧会出现`CORS` 问题，我们打开浏览器抓包一下请求看看

   ![image-20230209173904660](https://static.litetools.top/blogs/goswagger/image-20230209173904660.png)

   - 这时候我们就只好也走`内网ip` 然后接下来都`ok` 

5. 所以推荐`host` 参数设置如下

   - 这个位置如果是`nginx`服务，就写`127.0.0.1`即可。
   - 如果是内网，那么大家都用内网ip访问。
   - 如果是公网，那么就公网访问，也不会有问题。



#### 2) middlewares/cors.go

这里是我同源策略处理问题的时候，这里可以解决部分问题。毕竟这个地方可以在`nginx` 那里面替代处理

```go
package middlewares

import (
	"github.com/gin-gonic/gin"
)

func Cors() gin.HandlerFunc {
	return func(context *gin.Context) {
		method := context.Request.Method
		origin := context.Request.Header.Get("Origin") //请求头部
		if origin != "" {
			//接收客户端发送的origin （重要！）
			context.Writer.Header().Set("Access-Control-Allow-Origin", "*")

			//服务器支持的所有跨域请求的方法
			context.Header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE,UPDATE")
			//允许跨域设置可以返回其他子段，可以自定义字段
			context.Header("Access-Control-Allow-Headers", "Authorization, Content-Length, X-CSRF-Token, Token,session")
			// 允许浏览器（客户端）可以解析的头部 （重要）
			context.Header("Access-Control-Expose-Headers", "Content-Length, Access-Control-Allow-Origin, Access-Control-Allow-Headers")
			//设置缓存时间
			//c.Header("Access-Control-Max-Age", "172800")
			//允许客户端传递校验信息比如 cookie (重要)
			context.Header("Access-Control-Allow-Credentials", "true")
		}

		//允许类型校验
		if method == "OPTIONS" {
			context.AbortWithStatus(200)
		} else {
			context.Next()
		}
	}
}

```

这个使用的地方是在`router.go`里面

#### 3) router/router.go

```go
package router

import (
	"LearnTest/webbase/controller"
	_ "LearnTest/webbase/docs"       // 这个很重要 一定要导入计算好的这个目录，这个是swag init得到的
	"LearnTest/webbase/middlewares"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"   // 这个也要导入
	ginSwagger "github.com/swaggo/gin-swagger"   // 这个别忘记了也要
	"net/http"
)

func Routers() {
	router := gin.Default()
	router.Use(middlewares.Cors())  // 处理CROS问题的中间件，一般来说不用写，这里可以由nginx去解决
	// 这里是浏览器打开swagger的路由,这个地方 docs 可以是任意你想要的单词，这里也可以是你任意安排的路由
	router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
	
    // 下面是我的测试代码，展示了 4 种请求数据的方式，后面我会对每种数据方式的swagger模板进行设置
	test := router.Group("/test")
	{
		test.GET("/get_query", controller.TestGetQuery)
		test.GET("/get_param/:name", controller.TestGetParam)
		test.POST("/post_json", controller.TestPostJson)
		test.POST("/post_data", controller.TestPostData)
		test.POST("/", func(context *gin.Context) {
			context.JSON(http.StatusOK, gin.H{"code": "0", "msg": "默认路由返回"})
		})
	}
	router.Run(":8888")
}
```



#### 4) controller/controller.go

这里先展示**最上面**每个函数都可能会用到的东西

```go
package controller

import (
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

// 这个不是必要的，可以不弄这个，但是后面设置Success 和 Failure 的时候就需要弄其它模板
type Response struct {
	Msg  string `json:"msg"`
	From string `json:"from"`
}

// 这个不是必要的，可以不弄这个，但是后面设置Success 和 Failure 的时候就需要弄其它模板
type ResponseError struct {
	Code uint32 `json:"code"`
	Msg  string `json:"msg"`
}
```



> 下面代码都是接着上面写的 我们先对每一个板块单独写下来，然后汇总说一下

1. GET-query

   ```go
   // @Summary 这里是get测试query取值
   // @Description 这是description111
   // @Tags 测试
   // @produce json
   // @Router /test/get_query [get]
   // @Param name query string false "这里是get参数之一" default(swagger默认值) minlength(3) maxlength(100)
   // @Success 200 {object} Response "成功"
   // @Failure 400 {integer} integer "失败"
   func TestGetQuery(context *gin.Context) {
   	name := context.Query("name")
   	if name == "" {
   		name = "不传我就给这个默认值"
   	}
   	context.JSON(http.StatusOK, gin.H{"msg": name, "from": "get_query"})
   }
   ```

2. GET-param

   ```go
   // @Summary 这里是get测试param取值
   // @Description 这是description222
   // @Tags 测试
   // @produce json
   // @Router /test/get_param/{name} [get]
   // @Param name path string true "这里是get参数之一"
   // @Success 200 {object} Response "成功"
   func TestGetParam(context *gin.Context) {
   	name := context.Param("name")
   	context.JSON(http.StatusOK, gin.H{"msg": name, "from": "get_param"})
   }
   ```

3. POST-json

   ```go
   // @Summary 这里是post测试json取值
   // @Description 这是description333
   // @Tags 测试
   // @produce json
   // @Router /test/post_json [post]
   // @Accept json
   // @Param name body string true "测试"
   // @Success 200 {object} Response "成功"
   // @Failure 400 {object} ResponseError "失败"
   func TestPostJson(context *gin.Context) {
   	b, err := context.GetRawData()
   	if err != nil {
   		context.JSON(http.StatusBadRequest, gin.H{"msg": "传入数据有问题", "from": "post_json"})
   		return
   	}
   	var result map[string]interface{}
   	err = json.Unmarshal(b, &result)
   	if err != nil {
   		context.JSON(http.StatusBadRequest, gin.H{"msg": "传入的json有问题", "from": "post_json"})
   		return
   	}
   	context.JSON(http.StatusOK, gin.H{"msg": result, "from": "post_json"})
   }
   ```

4. POST-data

   ```go
   // @Summary 这里是post测试data取值
   // @Description 这是description444
   // @Tags 测试
   // @produce json
   // @Router /test/post_data [post]
   // @Param name formData string true "这里是post参数之一"
   // @Success 200 {object} Response "成功"
   func TestPostData(context *gin.Context) {
   	username := context.PostForm("name")
   	context.JSON(http.StatusOK, gin.H{"code": fmt.Sprintf("这里是post传过来的值: %v", username)})
   
   }
   ```

   
   
   > 通用模块位置， 下面出现的 `MIME` `参数类型` `数据类型` `param参数类型` 都在[二--> 1.3]里面详解
   
   **下面的很多参数用不到可以不写，可以看到我上面也不是全部都写的，对大小写不敏感**
   
   ``` go
   // @Summary      这个出现在参数的description位置 说这个参数做啥的
   // @Description  这个出现在URL后面，说明这个URL做啥的
   // @Tags         这个是对这个URL分组的，可以把多个统一名称tag放到一个组里面
   // @Produce      这个是值这个api产生什么类型的数据 选值从MIME类型里面选择  ---> 见 二->1->1.3 类型参数->MIME
   // @Accept       请求体接收的数据格式，值也是MIME类型
   // @Router       这个就是定义这个API的url的和请求方式 后面url和请求方式用空格分开，这里我要单独说
   // @Success      成功的时候的响应模板，这里不会对结果有影响，只是展示成功响应的情况，不写就不展示
   // @Failure      同成功。 -->这两个都是空格分隔，参数是: 响应码 {参数类型} 数据类型 备注  --> 见 二->1->1.3 类型参数->参数类型/数据类型
   // @Security     每个API操作的安全性。
   // @Header       请求头字段 格式是: 响应码 {参数类型} 数据类型 备注
   // @Param        这个位置下面细说 统一格式: 参数名称 param参数类型 数据类型 是否必须 备注 限制属性   --> 见 二->1->1.3 类型参数->param参数类型/限制属性
   ```
   
   
   
   > 单独说的参数
   
   `Router` : 这个其它参数都没有啥问题，就是取值类型为param的时候，这里我们不能按照`gin` url里面`xxx/:a/:b` 这样子写，这里我们需要写成`xxx/{a}/{b}`
   
   
   
   `Param` : 这个地方只有几个地方需要变就是param参数类型，统一的格式就是 `// @Param 参数名称 param参数类型 数据类型 是否必须 备注 限制属性 `    这里的详细讲解见 `1.3 下面的 param参数类型`  和`限制属性`.
   
   
   
   `Success / Failure `:  这里 格式是空格分隔 我们需要写如下几个参数，只会展示成功失败返回数据的基本模板，不会有具体值，这里也不会影响程序结果，只是**模板**， 所以可以定义多个成功和失败展示不同状态码的成功和失败的返回值
   
   ```go
   // @Success 状态码 {参数类型} 返回数据 备注
   // @Failure 状态码 {参数类型} 返回数据 备注
   ```
   
   
   
   ![image-20230210093727615](https://static.litetools.top/blogs/goswagger/image-20230210093727615.png)
   
   `Security` : 这个可以不写，写了就是做一些api校验，用的很少，如果要用可以查文档
   
   **通用API信息**
   
   ```go
   // @securityDefinitions.basic BasicAuth
   
   // @securitydefinitions.oauth2.application OAuth2Application
   // @tokenUrl https://example.com/oauth/token
   // @scope.write Grants write access
   // @scope.admin Grants read and write access to administrative information
   ```
   
   **每个API操作**
   
   ```go
   // @Security ApiKeyAuth
   ```
   
   **使用AND条件**
   
   ```go
   // @Security ApiKeyAuth
   // @Security OAuth2Application[write, admin]
   ```
   
   >这里摘抄自 中文文档: https://github.com/swaggo/swag/blob/master/README_zh-CN.md
   
   

### 1.3 类型参数

#### MIME

| 参数                  | 参数类型                          |
| --------------------- | --------------------------------- |
| json                  | application/json                  |
| x-www-form-urlencoded | application/x-www-form-urlencoded |
| xml                   | text/xml                          |
| plain                 | text/plain                        |
| html                  | text/html                         |
| mpfd                  | multipart/form-data               |
| json-api              | application/vnd.api+json          |
| json-stream           | application/x-json-stream         |
| octet-stream          | application/octet-stream          |
| png                   | image/png                         |
| jpeg                  | image/jpeg                        |
| gif                   | image/gif                         |



#### 参数类型

>  参数类型 Param Type

- object (struct 类型的东西写这个)
- string (string 类型写这个)
- integer (int, uinit, uint32, uint64 都写这个)
- number (float32 类型写这个称呼)
- boolean (bool)
- array



#### 数据类型

> 数据类型Data Type

- string (string)
- integer (int, uint, uint32, uint64)
- number (float32)
- boolean (bool)
- user defined struct     // 这里就比如我上面定义的成功失败的结构体



#### param参数类型

- **query** :  这个类型是取 `url?` 后面的数据的值，有几个参数就**写几行** 如下示例

  ```go
  // @Param name query string true "用户名"
  // @Param age query integer false "年龄" default(18)
  ```

- **path** : 这个类型是取restful格式的url的值 如路由那边写 `url/user/:name/:age` ,不过这里的Router得写成 `url/user/{name}/{age}` 下面才可以正常取值

  ```go
  // @Param name path string true "用户名"
  // @Param age path integer true "年龄"
  ```

- **header** : 这个是需要附加header里面参数的,这里注意**不能是中文**，最好是英文数字英文符号

  ```go
  // @Param token header string true "header需要的值"
  ```

- **body** : 这个是设置Json的数据,这里不和其它参数一样，这里**最好只设置一个**，设置多了虽然页面也会展示，但是api访问只会取最后一个框，他这个位置的第一个位置参数名无实际作用，配套的得在前面加一行传入参数限制才好。如下，name 无实际作用

  ```go
  // @Accept json
  // @Param name body string true "测试"
  ```

  ![image-20230210102518367](https://static.litetools.top/blogs/goswagger/image-20230210102518367.png)

- **formDate** : 取form-data的值的，有几个写几行

  ```go
  // @Param name formData string true "这里是post参数之一"
  // @Param age formData integer true "这里是post参数之二"
  ```

  

#### 限制属性

> 这里可以多个一起往后面写 也**可以不写**表示不限制，下面【】里面的是示例 没有示例的不咋常用

- defualt * 参数默认值    【default(666) default(这就是默认值)】
- maximum number 最大值  【maximum(199.99)】
- mininum number 最小值  【mininum(6.66)】
- maxLength integer 最大长度  【maxLength(1000)】
- minLength integer 最小长度   【minLength(1)】
- enums [*] 枚举类型  【enums(0, 1)】
- format string
- collectionFormat string query 数组分割模式



### 1.4 注意事项

1. 多字段定义时候不能跨字段，如两个相同的类型定义

   ```go
   // @Accept  json
   // @Produce json
   // @param id query string false "用户id" default("") minlength(3) maxlength(100)
   // @Produce json 这里将报错
   ```

   

2. 修改定义后需要重新执行，生成命令并重启服务

3. 路由配置的时候，需要引入文档

   ```go
   _ "LearnTest/webbase/docs"   // 如这一个引入
   ```

4. 备注那些字 一定有**双引号**包裹，不能裸奔

## 2. 运行

```bash
swag init       # 先计算出模板，没有问题我们测试运行
go run main.go  # 测试运行
```

访问页面测试，没有问题就行。 API单独访问是肯定没有问题的，主要是在swagger页面可能会出现一些问题。
