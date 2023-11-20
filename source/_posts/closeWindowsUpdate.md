---
title: 【windows】永久关闭这个烦人的自动更新
tags:
  - windows
  - 系统
categories: 教程
toc: true
date: 2023-11-20 17:50:08
---



是否已经厌烦了windows个人版经常自动更新，这个文章就是为了解决这个事！

<!-- more -->

# 一、为啥？

个人版的系统经常自动升级，本来好好的，挂了一些东西运行，但是，老是自动更新，然后还关闭不掉。那么下面是互联网上总结的一些经验



# 二、关闭这些

首先我们**打开终端**，这个开启方法很多，为了照顾很多非程序员的人，所以我会给很多示例，**随便选一个就好了**，我们今天要操作的事情，和终端的内容显示的没有关系，每个人的可能不一样，不过没有关系，我们输入的命令一样就好了~

## 0.打开终端

{% collapse 开启终端，任选其一 %}

1. 如果你有这个搜索窗口，或者是一个 放大镜的图标在任务栏，点一下，有个搜索，输入**cmd** 回车就好了。

   ![image-20231120164750311](https://static.litetools.top/blogs/windows/image-20231120164750311.png)

2. 这个是win11的位置，一样的其实，就是打开了 开始菜单后往上面输入**cmd**即可

   ![image-20231120165043293](https://static.litetools.top/blogs/windows/image-20231120165043293.png)

3. 随便打开一个资源目录文件夹，点击上面的 地址栏，然后这里输入**cmd**也可以

   ![image-20231120165159319](https://static.litetools.top/blogs/windows/image-20231120165159319.png)

4. 或者任意位置，**按住shift不放，然后右键鼠标**，会出来一个选项，我们点击 -- 在此处打开 Powershell 窗口，这个窗口样式和cmd的不太一样，但是和我们要进行的不影响

   ![image-20231120165525089](https://static.litetools.top/blogs/windows/image-20231120165525089.png)

5. 会开的人员随意

{% endcollapse %}



> 下面的命令，输入了之后，可能要等一段时间才会弹出来窗口，每个人的电脑性能不一样，耐心等一下~



## 1. services.msc

终端输入 `services.msc`

![image-20231120170000267](https://static.litetools.top/blogs/windows/image-20231120170000267.png)

在打开的窗口里面找到以下名称的东西：

![image-20231120170055856](https://static.litetools.top/blogs/windows/image-20231120170055856.png)

上面是未关闭的状态，我们要关闭这里！双击打开！

![image-20231120170207591](https://static.litetools.top/blogs/windows/image-20231120170207591.png)

服务状态：点击停止 >> 保证状态是 `已停止`

启动类型：改成`禁用`

操作完了先`应用`一下，然后点击上面的`恢复`,把第一次失败改成 `无操作`，然后`应用`之后`确定`退出

![image-20231120170401600](https://static.litetools.top/blogs/windows/image-20231120170401600.png)

>  除了终端，弹出来的关闭，这一步完成

## 2. gpedit.msc

 终端输入 `gpedit.msc`

![image-20231120170613356](https://static.litetools.top/blogs/windows/image-20231120170613356.png)

在**组策略编辑器**中里面找到以下名称的东西：**依次展开 计算机配置 -> 管理模板 -> Windows组件 -> Windows更新**

![image-20231120171132490](https://static.litetools.top/blogs/windows/image-20231120171132490.png)

1. 双击 `配置自动更新`

   选择 `已禁用` -> `确定` 

   ![image-20231120171259575](https://static.litetools.top/blogs/windows/image-20231120171259575.png)

2. 双击`删除使用所有Windows更新功能的访问权限`

   选择 `已启用` -> `确定` 

   ![image-20231120171404866](https://static.litetools.top/blogs/windows/image-20231120171404866.png)

>  除了终端，弹出来的关闭，这一步完成



## 3. taskschd.msc

 终端输入 `taskschd.msc`

![image-20231120171558777](https://static.litetools.top/blogs/windows/image-20231120171558777.png)

**在任务计划程序的设置界面，依次展开 任务计划程序库 -> Microsoft -> Windows -> WindowsUpdate**

![image-20231120171759187](https://static.litetools.top/blogs/windows/image-20231120171759187.png)

> 右边这个窗口里面，每个人的是不一样，右键选择 > 禁用 < 把能关闭的都关闭就好了，有的可能关闭不了，不用管就好了

![image-20231120171916972](https://static.litetools.top/blogs/windows/image-20231120171916972.png)

> 除了终端，弹出来的关闭，这一步完成



## 4. regedit

 终端输入 `regedit`

![image-20231120172108888](https://static.litetools.top/blogs/windows/image-20231120172108888.png)

有的人可能会弹出来这个，选择 **是**

![image-20231120172038417](https://static.litetools.top/blogs/windows/image-20231120172038417.png)

我们找到以下路径: **HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UsoSvc**

![image-20231120172320028](https://static.litetools.top/blogs/windows/image-20231120172320028.png)

点击一下，我们看到右边会这样子显示：

![image-20231120172421194](https://static.litetools.top/blogs/windows/image-20231120172421194.png)

1. 双击 `Start` 在弹出来的窗口:把数值改成 `4`

   ![image-20231120172545794](https://static.litetools.top/blogs/windows/image-20231120172545794.png)

2. 双击`FailureActions`:弹出来的窗口把图中左边对应的`10和18位置` ：这两右边圈主的第五组数字，原来是 两个 `01`  改成`00`

   ![image-20231120173804771](https://static.litetools.top/blogs/windows/image-20231120173804771.png)

**记得改了的都要确定保存哦**



好了，就这四个改了就好了，然后该关了的都可以关了~
