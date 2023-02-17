---
title: 【gRPC】师傅领进门，修仙靠个人
tags:
  - go
  - grpc
  - TLS
categories: 教程
toc: true
date: 2023-02-17 17:21:35
---


gRPC入门实战

<!-- more -->

# 一、基本介绍

## 1. 应用场景

我们先来简单的看一下

> 微服务

**单体架构**：

1. 一旦某个服务宕机，会引起整个应用不可用，隔离性差。
2. 只能整体应用进行伸缩，浪费资源，可伸缩性差。
3. 代码耦合在一起，可维护性差。

**微服务架构**:

解决了单体架构的弊端，但是引入了新的问题：

1. 代码冗余
2. 服务和服务之前存在调用关系。
3. 服务拆分后，服务和服务之间发生的是进程和进程之前的调用，服务器和服务器之间的调用。
4. 那么就需要发起网络调用，可能第一时间想起来的都是`http` 协议调用，大多微服务架构中，http虽然便捷方便，但是性能较低，这时候需要引入RPC，通过自定义协议发起TCP调用，加快传输效率。



## 2.过程

实际rpc是**客户端**与**服务端**沟通的过程

1. 客户端发送数据（以字节流的方式）
2. 服务端接收并解析。根据**约定**知道要执行什么，然后把结果返回给客户。

**RPC**:

1. 实际就是将上面过程封装一下，使其操作更加优化。
2. 使用一些大家都认可的协议，使其规范化。
3. 做成一些框架，直接或间接产生利益。



**gRPC**是一个高性能的、开源的通用RPC框架。

![Concept Diagram](https://grpc.io/img/landing-2.svg)



# 二、开始应用

## 1. protobuf

我们学习 gRPC需要使用`Protocol Buffss` 传输数据，这是谷歌搞得一套的数据结构序列化机制。

`序列化`: 将数据结构或对象转换成二进制串的过程。

`反序列化`: 将在序列化过程中所产生的二进制串转换成数据结构或者对象的过程。

>  protobuf的优势:

1. 序列化后体积相比JSON和XML都小，适合网络传输
2. 支持跨平台多语言
3. 消息格式升级和兼容新不错
4. 序列化和反序列化速度很快



### 1.1 proto文件介绍

> message

protobuf 中定义一个消息类型式是通过关键字 message字段指定的。 消息就是需要传输的数据格式的定义

`message` 关键字相当于 Cpp/Java/Python里面的class, go里面的struct

在消息中承载的数据分别对应于每一个字段，其中每个字段都有一个名字和一种类型，一个proto文件中可以定义多个消息类型。

> 字段规则

`required` : protobuf2 中消息体必填字段，不设置会导致编码异常，不过在protobuf3 里面被删除。

`optional` : 消息体重可选字段，protobuf3 里面没有required，optional等说明关键字，都默认optional。

`repeated` : 消息体中可重复字段，重复的值的顺序会被保留在go中重复的会被定义为**切片**。

```protobuf
message Hello {
	string requestName = 1;
	int64 age = 2;
	repeated string name = 3;     // Name []string 
}
```

> 消息号

在消息体的的定义中，**每个字段都必须要有一个唯一的标识号**，标识号是[1, 2^29 -1]范围内的**一个整数**。

> 嵌套消息

可以在其它消息类型中定义，使用消息类型，在下面的例子中，person消息就定在PersonInfo消息内:

```protobuf
message PersonInfo {
	message Person {
		string name = 1;
		int32 height = 2;
		repeated int32 weight = 3;
	}
	repeated Person info = 1;
}
```

如果要在它的父消息类型的外部重用这个消息类型，可以按照如下方式操作:

```protobuf
message PersonMessage {
	PersonInfo.Person info = 1;
}
```

> 服务定义

如果想要将消息类型用在PRC系统中，可以在 `.proto文件中顶一个rpc服务接口`，protocol buffer编译器将会根据所选择的不同语言生成服务接口代码及存根。

```protobuf
service SearchService {
	// rpc 服务函数名(参数) returns （返回参数)
	rpc Search(SearchRequest) returns (SearchResponse)	
	// 可以写多个
	rpc Search2(SearchRequest) returns (SearchResponse)

}
```

上诉代表表示，定义了一个RPC服务，该方法接收SearchRequest返回SearchResponse。



### 1.2 安装protobuf

[官方地址](https://github.com/protocolbuffers/protobuf): 点击找到`Releases` 下载想要的版本，下载下来是一个压缩包，把里面东西解压出来然后放到环境变量里面.

配置好了后重新打开终端输入 `protoc` 看一下是否正常即可。



### 1.3 安装gprc

```bash
go get google.golang.org/grpc
```

这里执行如果报如下错误，那么就是需要在项目目录下执行

![image-20230216175740512](https://static.litetools.top/blogs/grpc/image-20230216175740512.png)

然后我们在学习的目录下执行下面操作：

![image-20230216175818640](https://static.litetools.top/blogs/grpc/image-20230216175818640.png)

就可以正常执行了~

### 1.4 代码生成工具

上面我们安装了`protocol`的编译器，还有安装了核心库。我们在golang里面还需要执行以下俩操作:

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest  # 注意这里我们是从google.golang.org下载的 不是github.com/golang/ 这个位置下载的，这俩是不一样的。github的是旧版本，golang域名下的是新版本，API会有些不一样，所以我们也要用最新的版本
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

其实: 上面两个文件在安装`grpc`的时候已经下载了，只不过还没有安装，所以我们这里需要执行的是`install` 命令而不是`get` 。执行了之后这些东西都会在`GOPATH/bin`目录下面可以检查一下。



### 1.5 写一下

先直接看语法demo，这个东西并不是具体的数据，而是一个**约束**。

```protobuf
// 这里是在说明我们使用的是 proto3语法
syntax = "proto3";

// 这部分的内容是关于最后生成的go文件是在哪个目录哪个包中, . 代表当前目录生成, service代表了生成的go文件的包名是service,这个名字随便写无所谓的
option go_package = ".;service";

// 定义一个服务，在这个服务中需要一个方法，这个方法可以接受客户端的参数，再返回服务端的响应
// 其实很容易可以看出，我们定义了一个service， 称为SayHello, 这个服务中有一个rpc方法，名为 SayHello
// 这个方法会发送一个HelloRequest 然后返回一个HelloResponse
service SayHello {
  rpc SayHello(HelloRequest) returns (HelloResponse) {}
}

// message 关键字 可以理解为golang中的结构体
// 这里比较特别的是变量后面的 “赋值”。 这里并不是赋值，二十定义这个变量在这个message中的位置
message HelloRequest {
  string requestName = 1;
  // int64 age = 2;
}

message HelloResponse {
  string responseMsg = 1;
}
```

我们现在在目录下创建几个文件夹和文件，目录结构如下：

![image-20230216182621439](https://static.litetools.top/blogs/grpc/image-20230216182621439.png)

然后我们上面贴出的`proto`代码就是我们在`hello-server`里面写的内容。

接下来我们去往`hello-server/proto`目录下执行下面两条命令

```bash
protoc --go_out=. hello.proto        # 生成我们go相关文件 后面 . 就是当前位置 的 hello.proto文件
protoc --go-grpc_out=. hello.proto   # 生成我们的grpc相关文件
```

然后会给我们生成两个go代码在当前目录;

![image-20230216183841572](https://static.litetools.top/blogs/grpc/image-20230216183841572.png)

我们可以直接在生成的代码里面找到对应的方法然后实现我们要做的事情。

上面我们弄得东西是放在`hello-server`里面的，我们可以整体拷贝这个`proto`目录到`hello-client` ，代码是一样的，主要是里面的一些小东西调整，因为我们约束一致。



## 2. 服务端编写

- 创建gPRC Server对象，理解为Server端的抽象对象
- 将server （其包含的需要被调用的服务端接口）注册到gRPC Server 的内部注册中心
  - 这样可以在接收到请求时，通过内部的服务发现，发现该服务端接口并转接进行逻辑处理
- 创建Listen，监听TCP端口
- gRPC Server 开始 lis.Accept 直到Stop

### 2.1 编写代码

我们先从server那边 `grpc.pb.go` 文件里面留意两个东西，然后我们需要重新实现的

![image-20230217101356768](https://static.litetools.top/blogs/grpc/image-20230217101356768.png)

然后我们在main里面开启端口进行监听

```go
func main() {
	// 开启端口
	listen, _ := net.Listen("tcp", ":9090")
	// 创建grpc服务
	grpcServer := grpc.NewServer()
	// 在grpc服务端中注册我们自己编写的服务，这里在grpc那个pb.go 文件里都给我们写好了直接使用
	pb.RegisterSayHelloServer(grpcServer, &server{})
	// 启动服务
	err := grpcServer.Serve(listen)
	if err != nil {
		fmt.Println("创建服务失败...")
        return
	}
}
```

![image-20230217101924224](https://static.litetools.top/blogs/grpc/image-20230217101924224.png)

## 3. 客户端编写

- 创建与给定目标（服务端)的连接交互
- 创建server的客户端对象
- 发送PRC请求，等待同步响应，得到回调后返回响应结果
- 输出响应结果



### 3.1 编写代码

```go
package main

import (
	"context"
	"fmt"
	pb "gRPC/hello-server/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
)

func main() {
	// 我们先普通链接测试一下，仅用了安全传输，没有加密和验证
	conn, err := grpc.Dial("127.0.0.1:9090", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
		return
	}
	defer conn.Close() // 需要关闭

	// 和服务端创建链接
	client := pb.NewSayHelloClient(conn)

	// 执行rpc调用（服务端来实现并返回结果
	resp, _ := client.SayHello(context.Background(), &pb.HelloRequest{RequestName: "===heartfilia"})

	fmt.Println(resp.GetResponseMsg())

}

```

![image-20230217104208103](https://static.litetools.top/blogs/grpc/image-20230217104208103.png)

可以看到我们服务端运行一次 客户端调用一次



## 4. 安全传输[SSL/TLS]

gPRC是一个典型的C/S 模型，需要开发客户端和服务端，客户端与服务端需要达成协议，使用某一个确认的传输协议来传输数据，gRPC通常默认是使用protobuf来作为传输协议，当然也是可以使用其它自定义的协议的。

![image-20230217105118232](https://static.litetools.top/blogs/grpc/image-20230217105118232.png)

**gRPC认证**: 不是用户身份认证，而是指多个Server和多个client之间，如何识别对方是谁，并且可以安全的进行数据传入。下面是几种方案。

-  **SSL/TLS 认证方式(采用http2协议)**
- **基于Token的认证方式（基于安全链接)**
- 不采用任何措施的链接，这是不安全的链接(默认采用http1)
- 自定义的身份认证

客户端和服务端之间调用，我们可以通过加入证书的方式，实现调用的安全性.



TLS（Transport Layer Security 安全传输层）， TLS 是建立在传输层TCP协议之上的协议，服务于应用层，它的前身是SSL(Secure Socket Layer, 安全套接字层)，它实现了将应用层的报文进行加密后再交由TCP进行传输的功能。

TLS协议主要解决如下三个网络安全问题:

1. 保密(message privacy), 保密通过加密encryption实现，所有信息都加密传输，第三方无法嗅探;
2. 完整性(message integrity), 通过MAC校验机制，一旦被篡改，通信双方会立刻发现;
3. 认证(mutual authentication)，双方认证，双方都可以配备证书，防止身份被冒充;

> 生产环境可以购买证书或者一些平台发放的免费证书

key: 服务器上的私钥文件，用于对发送给客户端数据的加密，以及对从客户端接收到数据的解密

csr: 证书签名请求文件，用于提交给证书颁发机构(CA) 对证书签名

crt: 由帧数颁发机构(CA) 签名后的证书，或者是开发者自签名的证书，包含证书持有人的信息，持有人的公钥，以及签署者的签名等信息。

pem: 基于Base64编码的证书格式，扩展名包括PEM、CRT、CER。

我们可以参考这里查看更多: [聊聊HTTPS和SSL/TLS协议](https://www.kuangstudy.com/bbs/1604044550878703617)



### 4.1 SSL/TLS认证方式

我们需要通过`openssl` 生成证书和私钥

1. 下载工具

   - 如果有C语言工具可以通过官网下载下来自己编译(比较复杂): [官网链接](https://www.openssl.org/source/)
   - 也可以通过别人编译好的工具包来用: [便捷工具](http://slproweb.com/products/Win32OpenSSL.html)

2. 推荐便捷工具，一直下一步（我安装在了我自己喜欢放的目录）

   ![image-20230217114829177](https://static.litetools.top/blogs/grpc/image-20230217114829177.png)

3. 需要把安装好的目录里面`/bin`配置到环境变量

4. 装好了后新打开一个终端输入 `openssl` 测试一下，没有报错就是ok了

### 4.2 生成证书

> 这里生成的东西是给后面我们生成另外一套东西用的，这里的不引入代码

下面内容不用死记硬背，没意义，每次copy即可

```shell
# 1. 生成私钥         名字.key   名字随意
openssl genrsa -out server.key 2048

# 2. 生成证书，一直回车就好了，可以不填
openssl req -new -x509 -key server.key -out server.crt -days 36500
# 下面内容是敲了上面的后每个让你填写或者修改的操作
# 国家名称
Country Name （2 letter code) [AU]:CN
# 省名称
State or Provice Name (full name) [Some-state]:GuangDong
# 城市名称
Locality Name (eg, city) []:Guangzhou
# 公司组织名称
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Personal
# 部门名称
Organizational Unit Name (eg, section) []:go
# 服务器or网站名称
Common Name (eg. server FQDN or YOUR name) []:Heartfilia
# 邮件
Email Address []:xxxxx@qq.com

# 3.生成 csr   也可以一直回车下去
openssl req -new -key server.key -out server.csr
```

我们在项目中创建一个额外的目录`key`, 然后在这个目录下执行上面的操作

![image-20230217140828169](https://static.litetools.top/blogs/grpc/image-20230217140828169.png)

我们执行完了上面的`1` 后, `key` 目录下面会多一个 `server.key` 文件。

我们执行完了上面的`2` 后, `key` 目录下面会多一个 `server.crt` 文件。

我们执行完了上面的`3` 后, `key` 目录下面会多一个 `server.csr` 文件。



### 4.3 修改配置

```shell
# 更改openssl.cnf  (linux 是openssl.cfg)   在安装的openssl/bin 目录下
# 1. 复制一份已经安装好的 openssl.cnf 到项目所在目录
# 2. 找到[ CA_default ] 打开 copy_extensions = copy 把前面的 # 去掉
# 3. 找到[ req ] 打开 req_extensions = v3_req  # The extensions to add to a certificate request
# 4. 找到[ v3_req ], 添加 subjectAltName = @alt_names
# 5. 添加新的标签 [ alt_names ], 和标签字段
DNS.1 = *.yourdomain.com

# 这个下面可以写多个比如 以后访问必须要通过这个才可以访问代码 如果DNS.1 = *  那么就是所有都能访问不安全
DNS.2 = *.yourdomain2.com
DNS.3 = *.yourdomain3.com
```

1. ![image-20230217142727643](https://static.litetools.top/blogs/grpc/image-20230217142727643.png)
2. ![image-20230217142747346](https://static.litetools.top/blogs/grpc/image-20230217142747346.png)
3. ![image-20230217142832578](https://static.litetools.top/blogs/grpc/image-20230217142832578.png)
4. ![image-20230217142959904](https://static.litetools.top/blogs/grpc/image-20230217142959904.png)
5. ![image-20230217143125007](https://static.litetools.top/blogs/grpc/image-20230217143125007.png)



### 4.4 生成证书私钥

> 这里生成的东西才是我们代码里面用的

```shell
# 1. 生成证书私钥 test.key
openssl genpkey -algorithm RSA -out test.key

# 2. 通过私钥test.key 生成证书请求文件 test.csr （注意cfg和cnf 下面是官方默认写的openssl.cnf 我们要改成 cfg)
openssl req -new -nodes -key test.key -out test.csr -days 3650 -subj "/C=cn/OU=myorg/O=mycomp/CN=myname" -config ./openssl.cnf -extensions v3_req
# test.csr 是上面生成的证书请求文件。 ca.crt/server.key 是CA证书文件和key，用来对test.csr进行签名认证。这两个文件在第一部分生成

# 3. 生成SAN证书 pem  同理下面的 cnf 如果在windows也需要修改成 cfg
openssl x509 -req -days 365 -in test.csr -out test.pem -CA server.crt -CAkey server.key -CAcreateserial -extfile ./openssl.cnf -extensions v3_req
```

我们经过上面1.2.3 操作后生成了一堆文件

![image-20230217150053951](https://static.litetools.top/blogs/grpc/image-20230217150053951.png)

### 4.5 代码修改

1. server 端: 只需要增加两行代码

   ```go
   func main() {
   	fmt.Println("创建rcp服务中...")
   	//===================
   	// TLS认证
   	//===================
   	// 下面两个文件的路径最好用绝对路径不要用相对的
   	// 自签名证书文件和私钥文件
   	cred, _ := credentials.NewServerTLSFromFile(
   		"C:\\code\\mine\\GoCode\\src\\gRPC\\key\\test.pem",
   		"C:\\code\\mine\\GoCode\\src\\gRPC\\key\\test.key")
   	// 开启端口
   	listen, _ := net.Listen("tcp", ":9090")
   	// 创建grpc服务
   	grpcServer := grpc.NewServer(grpc.Creds(cred))
   	// 在grpc服务端中注册我们自己编写的服务，这里在grpc那个pb.go 文件里都给我们写好了直接使用
   	pb.RegisterSayHelloServer(grpcServer, &server{})
   	// 启动服务
   	err := grpcServer.Serve(listen)
   	if err != nil {
   		fmt.Println("创建服务失败...")
   		return
   	}
   }
   ```

   

2. 服务端: 这里也是我们只需要修改两行

   ```go
   func main() {
   	cred, _ := credentials.NewClientTLSFromFile(
   		"C:\\code\\mine\\GoCode\\src\\gRPC\\key\\test.pem",
   		"*.yourdomain.com") // 真实环境客户端这里要自动获取 不写死 这里必须得是我们之前配置文件里面dns.* = 域名 这里面的东西才可以校验通过
   	// 我们先普通链接测试一下，仅用了安全传输，没有加密和验证
   	//conn, err := grpc.Dial("127.0.0.1:9090", grpc.WithTransportCredentials(insecure.NewCredentials()))
   	// 这里是我们就要用安全的链接了
   	conn, err := grpc.Dial("127.0.0.1:9090", grpc.WithTransportCredentials(cred))
   	if err != nil {
   		log.Fatalf("did not connect: %v", err)
   		return
   	}
   	defer conn.Close() // 需要关闭
   
   	// 和服务端创建链接
   	client := pb.NewSayHelloClient(conn)
   
   	// 执行rpc调用（服务端来实现并返回结果
   	resp, _ := client.SayHello(context.Background(), &pb.HelloRequest{RequestName: "===heartfilia"})
   
   	fmt.Println(resp.GetResponseMsg())
   
   }
   ```

## 5. 安全传输[Token]

这里十分简单，gRPC给我们提供了一个接口，这个接口有两个方法，接口位于 credentials 包里面，这个接口需要由**客户端**来实现

```go
type PerRPCCredentials interface {
    GetRequestMetadata(ctx context.Context, uri ...string) (map[string]string, error)
    RequireTransportSecurity() bool
}
```

上面接口里面两个方法分别作用是:

1. 第一个方法--获取元数据信息，也就是客户端提供的key,value对， context用于控制超时和取消，uri是请求入口处的uri
2. 第二个方法--是否需要基于TLS认证进行安全传输，如果返回值是true,则必须加上TLS验证，返回值是false则不用。【结合操作的话这里改成true其他的和TLS那里设置流程一样的】



### 5.1 客户端代码

```go
package main

import (
	"context"
	"fmt"
	pb "gRPC/hello-server/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
)

type ClientTokenAuth struct {
}

func (c ClientTokenAuth) GetRequestMetadata(ctx context.Context, uri ...string) (map[string]string, error) {
	// 这里可以做实现操作 我们这是demo 直接返回
	return map[string]string{
		"appId":  "Heartfilia",
		"appKey": "666",
	}, nil
}

func (c ClientTokenAuth) RequireTransportSecurity() bool {
	return false // 我们这里不通过SSL/TLS 所以这里直接返回false
}

func main() {
	// 我们现在不通过TLS 我们验证token 所以这样子弄
	var opts []grpc.DialOption
	opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	opts = append(opts, grpc.WithPerRPCCredentials(new(ClientTokenAuth))) // 这里是需要弄我们自己实现的方法
	conn, err := grpc.Dial("127.0.0.1:9090", opts...)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
		return
	}
	defer conn.Close() // 需要关闭

	// 和服务端创建链接
	client := pb.NewSayHelloClient(conn)

	// 执行rpc调用（服务端来实现并返回结果
	resp, _ := client.SayHello(context.Background(), &pb.HelloRequest{RequestName: "===heartfilia"})

	fmt.Println(resp.GetResponseMsg())

}
```

### 5.2 服务端代码

因为我们用的是token校验，所以我们这里校验都在方法里校验

```go
package main

import (
	"context"
	"errors"
	"fmt"
	pb "gRPC/hello-server/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
	"log"
	"net"
)

type server struct {
	pb.UnimplementedSayHelloServer
}

// 业务逻辑在这里处理判断也在这里
func (s *server) SayHello(ctx context.Context, req *pb.HelloRequest) (*pb.HelloResponse, error) {
	// 获取元数据的信息
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, errors.New("未传输token")
	}
	var appId string
	var appKey string

	if v, ok := md["appid"]; ok {
		appId = v[0]
	}
	if v, ok := md["appkey"]; ok {
		appKey = v[0]
	}

	// 这里一般是查库啥的 我们这里写死
	if appId != "Heartfilia" || appKey != "666" {
		return nil, errors.New("token 不正确")
	}

	log.Println("当客户端访问这里将会被调用...")
	return &pb.HelloResponse{ResponseMsg: "hello" + req.RequestName}, nil
}

func main() {
	fmt.Println("创建rcp服务中...")
	// 开启端口
	listen, _ := net.Listen("tcp", ":9090")
	// 我们这里是去掉安全认证的
	grpcServer := grpc.NewServer(grpc.Creds(insecure.NewCredentials()))
	// 在grpc服务端中注册我们自己编写的服务，这里在grpc那个pb.go 文件里都给我们写好了直接使用
	pb.RegisterSayHelloServer(grpcServer, &server{})
	// 启动服务
	err := grpcServer.Serve(listen)
	if err != nil {
		fmt.Println("创建服务失败...")
		return
	}
}
```





# 总结

可以研究一下 `go-zero` ，上面的操作可以很轻松的帮我们实现上面的操作。有兴趣可以自己研究一下。
