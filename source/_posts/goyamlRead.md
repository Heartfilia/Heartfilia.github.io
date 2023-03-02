---
title: 【yaml】go里面两种yaml文件读取比较
tags:
  - go
  - yaml
categories: 摘要
toc: false
date: 2023-02-22 09:47:17
---




# 前言

我们平时读取配置文件大多都是`json, ini, conf, yaml ...` 这一些文件，各有各的方便之处。现在我这里浅浅的记录一下`go` 语言**读取**`yaml`文件。



> 这个文章只讲 读取 文件 的demo



首先我这里会说到两种方案，和网上的基本其它教程一样的：

- `gopkg.in/yaml.v3`
- `github.com/spf13/viper`





现在我们简单说一下我这里的目录结构

```te
$GOPATH/src/YamlTest
   |____________config.yaml     目标文件
   |____________yamlV3.go       第一种方式
   |____________vipeRead.go     第二种方式
```

这个测试的配置文件

```yaml
name: Heartfilia
age: 666
next:
  test1: 111
  test2: 222
  test3: 333
more:
  -
    - 666
    - 777
    - 888
  -
    - 000
    - 111
    - 222
```



# yaml.v3

这个包是谷歌官方推荐的，很快，不一定方便。

> 安装

```bash
go get -u gopkg.in/yaml.v3
```

用这个包，我们得已知目录结构，然后创建映射关系。

> 代码

```go
package main

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"os"
)

type Next struct {
	Test1 int `json:"test1"`
	Test2 int `json:"test2"`
	Test3 int `json:"test3"`
}

type Config struct {
	Name string  `json:"name"`
	Age  int     `json:"age"`
	Next Next    `json:"next"`
	More [][]int `json:"more"`
}

func main() {
	dataBytes, _ := os.ReadFile("config.yaml")

	config := Config{}
	yaml.Unmarshal(dataBytes, &config)

	name := config.Name
	more := config.More[0][1]
	fmt.Println(name, " : ", more)
}
```



因为这个后面读取内容和普通的变量属性操作没有任何差别，这里不再赘述。



# viper

> 安装

```bash
go get -u "github.com/spf13/viper"
```



这个在读取一般文件的时候非常方便，然后可以读取各种类型的配置文件，如果不配置后面的一个**文件格式**的属性，那么就会按照优先级依次读取。

优先级如下:

```bash
json > toml > yaml > yml > properties > props > hcl > tfvars > dotenv > env > ini
```

 也就是如果如果配置文件格式那里不写格式，同一个目录下有 `config.json` 和`config.yaml` 那么会优先读取`json` 格式的。

 

> 代码

这个包整体模板都差不多的，我这里先写一个基础格式 然后细说后面的一些操作

```go
package main

import (
	"fmt"
	viper2 "github.com/spf13/viper"
	"strings"
)

func Get(filePath, searchKey string) interface{} {
	// 文件          搜索路径
	basePathArray := strings.Split(filePath, "\\")
	fileName := basePathArray[len(basePathArray)-1]
	index := strings.Index(fileName, ".")
	fileNameString := fileName[:index]
	key := fileName[index+1:]
	viper := viper2.New()
	viper.SetConfigName(fileNameString)         // 配置文件名，不需要后缀名，我这里是自动获取
	viper.SetConfigType(key)                            // 配置文件格式, 我这里弄得自动获取
    // 下面添加路径的是可以添加多个环境的，如果放在某个目录可以再添加一下
	viper.AddConfigPath("$GOPATH/src/YamlTest")         // 查找配置文件的路径
	viper.AddConfigPath(".")                            // 查找配置文件的路径
	if err := viper.ReadInConfig(); err != nil {
		panic(err.Error())
	}
	return viper.Get(searchKey)
}
```

然后基本的键值对提取数据很简单，按照我这模板只需要如下写都可以

```go
func main() {
	result := Get("C:\\code\\mine\\GoCode\\src\\SqlTest\\YamlTest\\config.yaml", "next.test1")  // 写绝对路径 提取多层的数据
    fmt.Println(result)  
	result = Get("config.yaml", "next.test1")     // 写相对路径 提取多层的数据
	fmt.Println(result)
    result = Get("config.yaml", "name")     // 写相对路径 提取单层的数据
	fmt.Println(result)
}
```

到目前来都很简单，这也是大多数配置文件这样子写的，但是我这例子里面有一个嵌套的二维数组，我这里尝试提取 `more[0][1]` 的数据。这里才是我这里要讲的核心点。



这里我们先尝试获取`more` 的数据查看一下类型及结果

```go
func main() {
	result := Get("config.yaml", "more")
	fmt.Printf("%T  %v\n", result, result)
}
/* 运行结果
[]interface {}  [[666 777 888] [0 111 222]]
*/
```

所以可以说获取到了是一个 接口的集合值，我们现在需要对它进行遍历一下

```go
func main() {
	result := Get("config.yaml", "more")
	switch reflect.TypeOf(result).Kind() {
	case reflect.Slice, reflect.Array:
		s := reflect.ValueOf(result)
		for i := 0; i < s.Len(); i++ {
			key := s.Index(i).Interface()
			s1 := reflect.ValueOf(key)
			fmt.Printf("%T %v\n", s1, s1)
		}
	}
}
/* 运行结果
reflect.Value [666 777 888]
reflect.Value [0 111 222]
*/
```

可以看到我们运行了一次后 里面还有一层 但是是 `reflect.Value` 类型的，我们最终其实是想要里面的数据 比如我们设置成 `int`类型的 所以我们这里最好得创建一个变量来接收这个结果

```go
func main() {
	result := Get("config.yaml", "more")
	var res [2][3]int
	switch reflect.TypeOf(result).Kind() {
	case reflect.Slice, reflect.Array:
		s := reflect.ValueOf(result)
		for i := 0; i < s.Len(); i++ {
			key := s.Index(i).Interface()
			s1 := reflect.ValueOf(key)
			for i1 := 0; i1 < s1.Len(); i1++ {
                val := s1.Index(i1).Interface().(int)   // 核心是这里
				res[i][i1] = val
			}
		}
	}
	fmt.Println(res)
	fmt.Println(res[0][1])
}
/* 运行结果
[[666 777 888] [0 111 222]]
777
*/
```

 每一个 `reflect.Value` 属性的值都会有`Interface()` 的方法，然后就可以转换成想要的结果 我们这里数组默认是`int` 。我们要是后面不跟着`.(int)`，那么这个val是不可以给res赋值过去的，因为它会说 我们这个`Interface()` 返回的结果类型是`Any` ，不是`int` 。 虽然我们单个取值查看类型`Interface()` 返回的就是`int` ，但是我们如果要给其它`res`使用，这里就得指定一下，它返回的就是`int`。所以才不会有什么问题的。

```go
// 如果写下面内容 val 编译不过的报错示例
val := s1.Index(i1).Interface()
res[i][i1] = val

// val 编译报错结果
Cannot use 'val' (type any) as the type int   
var val any = s1.Index(i1).Interface()
// cannot use val (variable of type any) as int value in assignment: need type assertion
```

 所以我们这里一定要转换一下 然后就可以提取想要的结果了

# 总结

效率来说`yaml.v3` 运行效率很高，启动没有那么快，操作便捷性一般。[github](https://github.com/go-yaml/yaml)



`viper` 这个只要不搞我上面比较复杂的那种数组读取之类的，还是很简单的，也可以赋值给已经创建好了的结构体，也可以上手即用，运行效率比`yaml.v3` 慢一丢丢，但是好用啊，比如我这里只是**读取**操作，这个东西写起来也很方便，但是我这里就不用了，因为一般的配置文件都是我们外面写好的，就不赘述了，写的自己去查官网啥的。 [github](https://github.com/spf13/viper)



