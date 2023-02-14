---
title: 【反射】go-reflect基本理解
date: 2023-02-14 14:46:58
tags: go
categories: 摘要
toc: false
---



这个东西一般是**搞框架或者通用工具包**的时候可能会用的多，一般开发基本很少用到，只做了解~如果初学**不用着重**学习这里

<!-- more -->

# 变量的内在机制

首先我们了解一下空接口为啥可以接收任意类型的变量。

**Go语言中的变量是分为两部分：**

- 类型信息：预先定义好的元信息
- 值信息：程序运行过程中可动态变化的信息。

# 反射



## 一、介绍

反射是指在程序运行期间对程序本身进行访问和修改的能力。程序在编译时，变量被转换为内存地址，变量名不会被编译器写入到可执行部分。在运行程序时，程序无法获取自身的信息。（意思就是：变量名什么的是给我们人看的，方便我们编程使用。程序编译后，这些信息就没有了，都变成内存地址了。）

支持反射的语言可以在程序编译期间将变量的反射信息，如**字段名称、类型信息、结构体信息等整合到可执行文件中**，并给程序提供接口访问反射信息，这样就可以在程序运行期间获取类型的反射信息，并且有能力修改它们。



## 二、reflect

Go程序在运行期间使用`内置的reflect包`访问程序的反射信息。Go语言的反射机制中，任何接口值都是由`一个具体类型` 和`具体类型的值` 两部分组成(任意接口值在反射中都可以理解为由 `reflect.Type` 和 `reflect.Value` 两部分组成)。并且，reflect 包提供了这两个函数来获取任意对象的`Value` 和 `Type`。









### 1. TypeOf

在Go语言中，使用`reflect.TypeOf()` 函数可以活得任意值的类型对象(`reflect.Type`),程序通过类型对象可以访问任意值的数据类型信息。

![image-20230213101117492](https://static.litetools.top/blogs/goreflect/image-20230213101117492.png)



> type name 和 type kind

在反射中关于类型还划分为两种: `类型(Type)` 和 `种类(Kind)` 。因为在Go语言中我们可以使用type关键字构造很多自定义类型，而`种类(Kind)` 就是指底层的类型，但在反射中，当需要区分指针、结构体等大品种的类型时，就会用到`种类(Kind)` 。举个例子，我们定义了两个指针类型和两个结构体类型，通过反射查看他们的类型和种类。

```go
package main

import (
	"fmt"
	"reflect"
)

type myInt int64

func ReflectType(x interface{}) {
	t := reflect.TypeOf(x)
	fmt.Printf("Param: %v  Name: %v  Kind: %v \n", x, t.Name(), t.Kind())
}

func main() {
	var a *float32 // 指针
	var b myInt    // 自定义类型
	var c rune     // 类型别名
    var d map[string]int
	ReflectType(a)
	ReflectType(b)
	ReflectType(c)
	ReflectType(d)
}

/* 输出结果
Param: <nil>  Name:   Kind: ptr
Param: 0  Name: myInt  Kind: int64
Param: 0  Name: int32  Kind: int32
Param: map[]  Name:   Kind: map
*/
```

**可见**： 稍微测试一下，Go语言的反射中像数组、切片、Map、指针等类型的变量，他们的`.Name()` 返回都是`空`

下图是在`reflect` 包里面定义的一些`Kind` 类型。

![image-20230213105827216](https://static.litetools.top/blogs/goreflect/image-20230213105827216.png)



### 2. ValueOf

`reflect.ValueOf()` 返回的是`reflect.Value` 类型，其中包含了原始值的值信息。`reflect.Value` 与原始值之间可以相互转换。

`reflect.Value` 类型提供的获取原始值的方法如下:

|           方法           |                             说明                             |
| :----------------------: | :----------------------------------------------------------: |
| Interface() interface {} | 将值以 interface{} 类型返回，可以通过类型断言转换为指定类型  |
|       Int() int64        |     将值以 int 类型返回，所有有符号整型均可以此方式返回      |
|      Uint() uint64       |     将值以 uint 类型返回，所有无符号整型均可以此方式返回     |
|     Float() float64      | 将值以双精度（float64）类型返回，所有浮点数（float32、float64）均可以此方式返回 |
|       Bool() bool        |                     将值以 bool 类型返回                     |
|     Bytes() []bytes      |               将值以字节数组 []bytes 类型返回                |
|     String() string      |                     将值以字符串类型返回                     |

#### 通过反射获取值

```go
package main

import (
	"fmt"
	"reflect"
)

func getReflectValue(x interface{}) {
	v := reflect.ValueOf(x)
	k := v.Kind()
	switch k {
	case reflect.Int64:
		// v.Int()从反射中获取整型的原始值，然后通过int64()强制类型转换
		fmt.Printf("type: int64, value is %d \n", int64(v.Int()))
	case reflect.Float32:
		// v.Float()从反射中获取浮点型的原始值，然后通过float32()强制类型转换
		fmt.Printf("type: float32, value is %f \n", float32(v.Float()))
	case reflect.Float64:
		// v.Float()从反射中获取浮点型的原始值，然后通过float64()强制类型转换
		fmt.Printf("type: float64, value is %f \n", float64(v.Float()))
	}
}

func main() {
	var a float32 = 3.14
	var b int64 = 111
	getReflectValue(a)
	getReflectValue(b)
	// 将 int类型的原始值转换为 reflect.Value 类型
	c := reflect.ValueOf(10)
	fmt.Printf("type c: %T \n", c)
}
/* 结果
type: float32, value is 3.140000
type: int64, value is 111
type c: reflect.Value
*/
```

#### 通过反射设置变量的值

想要在函数中通过反射修改变量的值，需要注意函数参数传递的是值拷贝，必须传递变量地址才能修改变量值。而反射中使用专有的`Elem()`方法来获取指针对应的值。

```go
package main

import (
	"fmt"
	"reflect"
)

func setReflectValue1(x interface{}) {
	// 错误的修改方式demo
	v := reflect.ValueOf(x)
	if v.Kind() == reflect.Int64 {
		v.SetInt(200) // 修改的是副本，reflect包会引发panic
	}
}

func setReflectValue2(x interface{}) {
	v := reflect.ValueOf(x)
	// 反射中使用 Elem()方法获取指针对应的值
	if v.Elem().Kind() == reflect.Int64 {
		v.Elem().SetInt(200)
	}
}

func main() {
	var a int64 = 100
	//setReflectValue1(a) // panic: reflect: reflect.Value.SetInt using unaddressable value
	setReflectValue2(&a) // 200   这里需要传入指针
	fmt.Println(a)
}
```

### 3. isNil() 和 isValid()

> `IsNil()`常被用于判断指针是否为空；`IsValid()`常被用于判定返回值是否有效。

#### isNil()

`IsNil()`返回v持有的值是否为nil。v持有的值的分类必须是通道、函数、接口、映射、指针、切片之一；否则IsNil函数会导致panic。

```go
// 源码
func (v Value) IsNil() bool
```



#### isValid()

`IsValid()`返回v是否持有一个值。如果v是Value零值会返回假，此时v除了IsValid、String、Kind之外的方法都会导致panic。

```go
// 源码
func (v Value) IsValid() bool
```



#### 使用示例

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	// *int 类型空指针
	var a *int
	fmt.Println("var a *int IsNil:", reflect.ValueOf(a).IsNil())
	fmt.Println("nil      IsValid:", reflect.ValueOf(nil).IsValid())

	// 实例化一个匿名结构体
	b := struct{}{}
	// 尝试从结构体中查找 "abc" 字段
	fmt.Println("不存在的结构体成员:", reflect.ValueOf(b).FieldByName("abc").IsValid())
	// 尝试从结构体中查找 "abc" 字段
	fmt.Println("不存在的结构体成员:", reflect.ValueOf(b).MethodByName("abc").IsValid())

	// map
	c := map[string]int{}
	// 尝试从map中查找一个不存在的键
	fmt.Println("map中不存在的键:", reflect.ValueOf(c).MapIndex(reflect.ValueOf("heartfilia")).IsValid())
}
/* 结果
var a *int IsNil: true
nil      IsValid: false
不存在的结构体成员: false
不存在的结构体成员: false
map中不存在的键: false
*/
```



### 4. 结构体反射

#### 与结构体相关的方法

任意值通过`reflect.TypeOf()`获得反射对象信息后，如果它的类型是结构体，可以通过反射值对象（`reflect.Type`）的`NumField()`和`Field()`方法获得结构体成员的详细信息。

`reflect.Type`中与获取结构体成员相关的的方法如下表所示。

|                            方法                             |                             说明                             |
| :---------------------------------------------------------: | :----------------------------------------------------------: |
|                  Field(i int) StructField                   |          根据索引，返回索引对应的结构体字段的信息。          |
|                       NumField() int                        |                   返回结构体成员字段数量。                   |
|        FieldByName(name string) (StructField, bool)         |       根据给定字符串返回字符串对应的结构体字段的信息。       |
|            FieldByIndex(index []int) StructField            | 多层成员访问时，根据 []int 提供的每个结构体的字段索引，返回字段的信息。 |
| FieldByNameFunc(match func(string) bool) (StructField,bool) |              根据传入的匹配函数匹配需要的字段。              |
|                       NumMethod() int                       |                返回该类型的方法集中方法的数目                |
|                     Method(int) Method                      |                返回该类型方法集中的第i个方法                 |
|             MethodByName(string)(Method, bool)              |              根据方法名返回该类型方法集中的方法              |

#### StructField类型

`StructField`类型用来描述结构体中的一个字段的信息。定义如下：

```go
type StructField struct {
    // Name是字段的名字。PkgPath是非导出字段的包路径，对导出字段该字段为""。
    // 参见http://golang.org/ref/spec#Uniqueness_of_identifiers
    Name    string
    PkgPath string
    Type      Type      // 字段的类型
    Tag       StructTag // 字段的标签
    Offset    uintptr   // 字段在结构体中的字节偏移量
    Index     []int     // 用于Type.FieldByIndex时的索引切片
    Anonymous bool      // 是否匿名字段
}
```

#### 结构体反射示例

当我们使用反射得到一个结构体数据之后可以通过索引依次获取其字段信息，也可以通过字段名去获取指定的字段信息。

```go
package main

import (
	"fmt"
	"reflect"
)

type Data struct {
	Detail []string `json:"detail"`
}

type More struct {
	Hobby string  `json:"hobby"`
	Tall  float32 `json:"tall"`
	Data  `json:"data"`
}

type student struct {
	Name  string `json:"name"`
	Score int    `json:"score"`
	More  `json:"more"`
}

func main() {
	stu1 := student{
		Name:  "Heartfilia",
		Score: 99,
		More: More{
			Hobby: "eat",
			Tall:  3.14,
			Data: Data{
				Detail: []string{"a", "b", "c"},
			},
		},
	}
	t := reflect.TypeOf(stu1)
	fmt.Println(t.Name(), t.Kind())
	// 通过for循环遍历结构体的所有字段信息
	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		fmt.Printf("name:%s index:%d type:%v json tag:%v\n", field.Name, field.Index, field.Type, field.Tag.Get("json"))
	}
	// 通过字段名获取指定结构体字段信息
	if scoreField, ok := t.FieldByName("Score"); ok {
		fmt.Printf("name:%s index:%d type:%v json tag:%v\n", scoreField.Name, scoreField.Index, scoreField.Type, scoreField.Tag.Get("json"))
	}
}
/*结果
student struct
name:Name index:[0] type:string json tag:name
name:Score index:[1] type:int json tag:score
name:More index:[2] type:main.More json tag:more
name:Score index:[1] type:int json tag:score
*/
```

## 三、总结

这东西一般开发的时候**很少用到**，可能在需要写一些**框架，通用工具**的时候才会用到，增加兼容性~

反射是一个强大并富有表现力的工具，能让我们写出更灵活的代码。但是反射不应该被滥用，原因有以下三个。

1. 基于反射的代码是极其脆弱的，反射中的类型错误会在真正运行的时候才会引发panic，那很可能是在代码写完的很长时间之后。
2. 大量使用反射的代码通常难以理解。
3. 反射的性能低下，基于反射实现的代码通常比正常代码运行速度慢一到两个数量级。



> 本文参考李文周的博客

- [-] [Go语言基础之反射](https://www.liwenzhou.com/posts/Go/reflect/)
