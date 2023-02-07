---
title: 【泛型】go语言泛型编程
date: 2023-02-07 16:02:44
tags: go
categories: 摘要
toc: false
---



`go 1.18` 后面才有的内容

<!-- more -->

更详细的推荐下面这篇文章:

[Go 1.18 泛型全面讲解：一篇讲清泛型的全部](https://segmentfault.com/a/1190000041634906)



按照往常我们用`interface` 实现不同类型的参数接收，但是我们需要对它类型断言判断，如果有多种不同类型参数，那么我们就要多个`if` 判断，如下：

```go
package main

import "fmt"

func main() {
	printArray([]string{"hello", "world"})
	printArray([]int{1, 2})
}

// 按照以往操作 如果要对不同类型的数组或者切片遍历需要断言
func printArray(arr interface{}) {
	// 类型断言 x.(T) 其实就是判断T是否实现了x接口，如果实现了，就把x接口类型具体化为T类型
    // 如果传入的是string 那么我这里就要写string 如果其他的就要写其他的 就很麻烦
	for _, a := range arr.([]string) {   
		fmt.Println(a)
	}
    // 比如我这里只判断了string 那么上面传入的int类型的就会报错
}
```



现在我们多了**泛型**,可以大大的简化这个过程

```go
package main

import "fmt"

func main() {
	printArray([]string{"hello", "world"})
	printArray([]int{1, 2})
    printParam(3.14)
    printParam("666")
}

// 所以我们不限定它的类型，让调用者直接去定义类型： go1.18后才有这个泛型的
// 函数名后面加入中括号限定 arr的类型  我这里限定了只能传入string或者int
// 因为我这里是数组类型 所以传入形式类型 []T
func printArray[T string | int](arr []T) {
	for _, a := range arr {
		fmt.Println(a)
	}
}
// 这里是普通的单值类型 所以我们可以这样子 T
func printParam[T string | int | float64](p T) {
	fmt.Printf("%v %T\n", p, p)
}
// 这样子我们就可以对限定了类型的参数进行合并操作了
```



> 内置的泛型 `any` 和 `comparable`
>
> > `any`: 表示go里面所有的内置基本类型，等价于`interface{}`
> >
> > `comparable`: 表示go里面所有内置的可比较类型--> `int,uint,float,bool,struct,指针`等一切可以比较的类型

```go
func printArray[T any](arr []T) {
    for _, a := range arr {
        fmt.Println(a)
    }
}
```



> 总结：泛型的作用

泛型减少重复代码并提高类型的安全性



> 泛型最佳适配场合

- 需要针对不同类型书写同样的逻辑
- 使用泛型简化代码

