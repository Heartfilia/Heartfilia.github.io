---
title: 【lite-tools】一个python包的使用目录
date: 2022-11-17 18:31:35
tags: python
categories: 教程
toc: true
---

> 这个包是我搞的 方便日常工作中一些重复代码或者需要绕弯的代码压缩版本

<!-- more -->

# 安装
这里一般来说国内国外镜像都可以，不过我这个更新太随意了，有些时候国内镜像更新会慢几小时
`pip install lite-tools` 如果有其他需求可以`pip install lite-tools[all]`不过这个`all`版本我没有搞完，没时间，哈哈哈
# 命令行版块
这里我们可以直接 `lite-tools -h`获取一些详细的操作
> 如果遇到pip安装了之后 lite-tools还是命令行不可使用，那是你python的scripts目录不在环境变量里面,需要手动添加一下,因为不添加你的`scrapy``feapder`这些工具也不可以命令行使用，具体操作自己百度即可。


![命令行帮助](http://static.litetools.top/blogs/lite_tools/1.png)
## lite-tools fish
这是一个人生日历，没有搞农历节日那些东西，所以这里是标准的**上五休二**制度
## lite-tools say
这里基于 [熊与论道兽音](http://hi.pcmoe.net/roar.html) 版块修改算法改成python版本后实现的，并做了智能识别，大概操作如下
![兽语](http://static.litetools.top/blogs/lite_tools/2.png)
## lite-tools acg
这里我没有弄好，主要是这里需要一个自动校准数据这里我没有弄，后面再弄，不复杂，想提前体验可以终端输入自己试一下
## lite-tools news

1. 这里默认是获取国内新闻
2. `lite-tools news weibo` 这样子可以获取此时此刻的微博热榜榜单
3. `lite-tools news china/world`后面跟`china`或者`world`可以获取此时此刻中国或者世界上的最新的新闻
## lite-tools today

1. 默认获取今天的黄历，也可以获取今年的节假日，并看经过情况
2. `lite-tools today history`获取历史上的今天的信息
3. `lite-tools today oil`获取今天的油价
## lite-tools weather
默认根据当前请求IP获取当地的天气，当然有可能请求失败，然后会默认返回北京的天气
可以手动指定 **市区县 **然后获取对应地点的天气，后面不用写市区县，如下
> lite-tools weather 天河     获取天河区的天气，如果全国有同名的区就不知道是哪个地方了
> lite-tools weather 广州     这样子就可以获取广州市的 

## lite-tools trans
这里需要安装额外的包 `pip install lite-tools[all]`才可以实现以下功能。
**这里是比较复杂的，这里面很多功能我没有实现，目前我只搞了一个图片转pdf。**
**具体的操作可以看 **`**lite-tools trans -h**`
![转换操作](http://static.litetools.top/blogs/lite_tools/4.png)
这里`-i`或者`--input`后面必须要跟输入路径，这后面可以跟文件夹，也可以跟单个图片
`-o`或者`--output`后面是输入文件的位置，这里可以定义输出文件的名称，不写默认同输入文件的名字
示例:
![示例代码](http://static.litetools.top/blogs/lite_tools/11.png)
上面`-i`后面跟了这个文件夹路径  后面`-o`后面自定义了输出的文件名称 这里的`-o`要是不写后面输出的文件就是 和文件夹同名的一个`pdf`
> 这里有个问题，这里是一个图片一页纸 我没有做密度排版，那样子要做很多计算，太麻烦了，反正平时大多数图片都是一页一页的

# 代码里面使用

没有写 后面再写