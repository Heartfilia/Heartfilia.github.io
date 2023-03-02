---
title: 【pandas】结合xlsxwriter变得轻松一点
tags:
  - pandas
  - python
categories: 教程
toc: false
date: 2023-02-15 17:30:25
---




我这个地方是不讲数据处理的，只管内容的样式设置。核心使用pandas 辅助引擎采用 xlsxwriter，不会讲的很细，只会讲几个常用操作。

<!-- more -->

<a id="top"></a>

> 关于`xlsxwriter`的更多操作可以点击 [这里官方链接](https://xlsxwriter.readthedocs.io/worksheet.html)

# 一、基础操作

## 1. 无格式设置

按照常规数据来说，基本没有什么格式需求，所以我们可以直接采取最基础的操作：如下

```python
import pandas as pd

base_dict = {
    "a": [1, 2, 3],
    "b": ["一", "二", "三"]
}
df = pd.DataFrame(base_dict)
df.to_excel("基础样式.xlsx", freeze_panes=(1, 0), index=False)  #  我这里设置了冻结首行 关闭了内容序号标记
```

![image-20230215110221616](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215110221616.png)

## 2. 取消超链接

但是这样子应付基本的数据没有问题，如果内容是链接，问题就有了

```python
base_dict = {
    "a": ["http://www.baidu.com", "http://www.baidu.com"],
    "b": ["http://www.google.com", "http://www.google.com"]
}
```

![image-20230215110351452](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215110351452.png)

可以看到内容都是超链接格式，内容少问题不大，但是内容多了，那么一个xlsx文件就会巨大，而且生成也慢，而且又不好看。这时候我们就需要引入我们今天的主角了 ： `xlsxwriter`

这个是一个包来的，可以独立使用，也可以引入pandas引擎作为pandas的插件。

首先得保证我们有这个包

```bash
pip install xlsxwriter
```

然后我们导出内容的时候就不要直接`df.to_excel`了

```python
# 我们导出一个df的话 直接
df = pd.DataFrame(base_dict)
# 下面我们用 with 创建一个上下文管理器 writer出来 这里引擎有很多选择，我们这篇文章主要是xlsxwriter 所以后面都将用这个模板 
with pd.ExcelWriter("基础样式.xlsx", engine="xlsxwriter", engine_kwargs={"options": {"strings_to_urls": False}}) as writer:
    df.to_excel(writer, index=False, freeze_panes=(1, 0))
```

![执行了上面操作之后](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215111142907.png)

### 2.1引擎参数

上面我们看到我在后面 `engine_kwargs={"options": {}}` 设置了东西，那么这东西我们怎么能知道设置哪些呢？

我们可以跟进 `xlsxwriter` 的源码里面，我们进去就可以看到有个`class Workbook(xmlwriter.XMLwriter):` 的类，下面有个  `options = {}` 的操作，然后我们开启查找进行标记，可以看到有一堆参数我们进行修改的。



![image-20230215111723844](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215111723844.png)

我们刚才使用的 `strings_to_urls` 就是这里的一个参数，所以同理其他的也能这样子设置。





# 二、样式操作

这里才是我这里今天要讲的核心部分。

这里主要的样式操作啥的，其实还是有很多样式**没有写到**，我这里就**不多写**，额只弄常见的一些操作。

下面有两种表格样式 一是基础样式: `add_format` 还有一个插入表图: `add_chart`。这两个都是会返回一个样式对象。

**然后**我们通过

- `write_row/write (这个我们这里不常用，因为数据我们弄得一般是有了的)`

- `merge_range (这里是表格合并的时候可以添加的操作)`

- `set_column  (设置列的时候添加样式)` 

- `set_row (设置行的时候添加样式)` 

- `conditional_format (根据条件添加样式)` 

等等操作的时候添加那个样式对象的。

我们先逐步假设场景，然后来解决。

## 1. add_format

用于在工作表中创建一个新的格式对象来格式化单元格。

这个是可以**单独**添加样式的**主要**操作方式,大概可以设置的参数如下: 

> 如果出现 `是否` 两个字，表明设置值为 `True/False`

- `align` : 水平对齐方式
  - `left/center/right `
  - `不常用的:fill/justify/centre_across/distributed/justify_distributed`
- `valign`: 垂直对齐方式
  - `top/vcenter/bottom`
  -  `不常用的:vjustify/vdistributed`
- `border`:  边框
  - `0无边框  1外边框 ...`
- `bold`:  **是否**字体加粗
- `italic`: **是否**字体倾斜
- `font_name`: 字体
- `font_size`: 字体大小
- `font_color`: 字体颜色(这里用 #000000 这种格式的最好)
- `text_wrap`: **是否**自动换行

我们平时操作数据的时候，基本都是利用pandas 然后创建 `df = pd.DataFrame` ，pandas处理数据能力是非常牛逼，无其它包能敌的。但是美化这一点来说，可以说，基本没有美化。网上之前查询过很多设置pandas样式的操作，就改各种`css` 结果都不咋地，反正pands自带的一些美化是**有，但不多**。但是，我们可以利用`openpyxl` 或者 `xlsxwriter` 之类的对美化操作很方便的包来实现。但是两边的数据操作的类是不一样的，所以需要**进行转化**：

我们这里不讲`openpyxl`,这个工具也很强，但是我还是喜欢用`xlsxwriter`这里面。

最基础的demo如下：

```python
import pandas as pd

base_dict = {
    "姓名": ["张三", "李四", "王五"],
    "周一": ["09:00\n18:00", "09:00\n18:00", "09:00\n18:00"],
    "周二": ["10:00\n19:00", "10:00\n19:00", "10:00\n19:00"],
}
# 我们创建df的时候这里 也可以 是二维数组，然后 我们通过header添加标题

df = pd.DataFrame(base_dict)
with pd.ExcelWriter("进阶样式.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, freeze_panes=(1, 0))
```

![image-20230215113820170](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215113820170.png)

可以看到我们的内容，表格内的换行是没有了，那么我们这里就需要先利用`xlsxwriter`来对pandas的`df` 数据进行美化。

### 1.1 获取workbook和worksheet

> 声明: 下面是缩写描述

`workbook` : 是 `xlsxwriter`的文件对象

`worksheet` : 是利用`workbook` 来获取`sheet`的对象

在`pandas`里面我们利用了`xlsxwriter`引擎后，可以通过创建出来的`writer`对象获取到我们想要的

```python
with pd.ExcelWriter("进阶样式.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, freeze_panes=(1, 0))  # 这里就是我们基础的数据 无样式
    workbook = writer.book    # 这样就是一个workbook对象
    worksheet = writer.sheets["Sheet1"]  
    # 因为 writer.sheets 返回的是一个字典，这个地方我们要取值到需要操作的sheet， 我们这里只有一个df 默认这个df的sheet_name是Sheet1 所以这里需要写Sheet1，当然可以对需要操作的df设置想要设置的名称，然后这里也需要对应修改
```

### 1.2 内容换行

这里是接着上面内容写的，后面的展示内容均会这样子操作，因为我们设置样式是需要这两个对象的，然后我们只需要对这两个对象操作就好了。

![image-20230215115558078](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215115558078.png)

```python
wrap_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'top'})
worksheet.set_row(1, 30, wrap_format)   # 设置索引1号行的样式
worksheet.set_row(2, 30, wrap_format)   # 设置索引2号行的样式
worksheet.set_row(3, 30, wrap_format)   # 设置索引3号行的样式
```



这里是设置了行的属性，**如果要**设置列，更加简单

```python
worksheet.set_column("A:A", 30, wrap_format)   # 只修改A列的样式
worksheet.set_column("B:E", 30, wrap_format)   # 修改B-E列的样式
```



后面设置样式的时候，我均只写 `workbook` 和 `worksheet` 后面的内容！因为这里的`api`和普通的`xlsx` 包无差异。

我们设置了样式之后看看结果：

![image-20230215120145450](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215120145450.png)

我们上面设置了 `1, 2, 3` 行的内容样式 这个数据其实是对应了 我们注释了的 索引(`index=False` 这个设置隐藏了)的 `1,2,3` 。这里标题那一栏是`0` 我们没有设置而已。

可以看到内容已经设置了自动换行，然后我们还设置了一些对齐样式， 其实主要就是讲解这个`add_format`的一些附加属性操作。

### 1.3 单元格合并

这里我们就不讲获取相同内容值的操作了，我们主要讲一下参数。我们就按照上面那个表，我们想合并周一一样的内容和周二一样的内容，我这里举例子我就不把周一周二一起合并了，周一合并一块，周二合并一块

```python
merge_format = workbook.add_format({'text_wrap': True, "bold": True, 'align': 'center'})
worksheet.merge_range(1, 1, 3, 1, "xxxx\n换行后内容", merge_format)   # (开始行,开始列,结束行,结束列,合并后值,合并内容样式)  行列均0开始
worksheet.merge_range(1, 2, 3, 2, "yyyy\n换行后内容", merge_format)   # (开始行,开始列,结束行,结束列,合并后值,合并内容样式)  行列均0开始
```

![image-20230215154121126](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215154121126.png)

主要是这个`merge_range` 有五个参数，其中第五个位置样式可以不写。

## 2. add_chart

在这里我们先准备一些测试用的数据。

```python
import pandas as pd

base_data = [
    ["张三", 10, 13],
    ["李四", 20, 35],
    ["王五", 30, 21],
    ["赵六", 11, 15],
    ["钱七", 25, 20],
]
# 用这种数组格式一条表示一行数据
# headers 我这里模板没有用字典,所以我需要设置header来命名，如果不弄的话就会默认的标题0 1 2 .....
headers = ["姓名", "上次", "这次"]
df = pd.DataFrame(base_data)
with pd.ExcelWriter("表格示例.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="表格测试", header=headers, freeze_panes=(1, 0))
    workbook = writer.book
    worksheet = writer.sheets["表格测试"]
```

和上面一样 我后面操作均不缩进，均单独书写。

### 2.1 表格样式

| type可选参数 |     描述     |
| :----------: | :----------: |
|     area     | 面积样式图表 |
|     bar      | 条形样式图表 |
|    column    | 柱形样式图表 |
|     line     | 线性样式图表 |
|     pie      | 饼状样式图表 |
|   scatter    | 散点样式图表 |
|    stock     | 股票样式图表 |
|    radar     | 雷达样式图表 |

我们用柱形样式图表做一个demo~

```python
chart_column = workbook.add_chart({"type": "column"})   # 创建一个图表对象
#定义图像数据系列函数
# 下面这个每操作一次就相当于添加一组记录到表
chart_column.add_series({
    "name": "=表格测试!$B$1",         # 引用业务名称为 图例项 就是标注在旁边的标记
    "categories": "=表格测试!$A$2:$A$6",   # 这个是将什么作为 x 轴 A2到A6
    "values": "=表格测试!$B$2:$B$6",       # 这里是添加第 一 组数据
    "data_labels": {"value": True},       # 显示数字,默认不显示
    "line": {"color": "black"},           # 线条定义为 黑色
})
# 同理再添加第二条，如果数据量很多的话，可以单独写一个方法，然后循环操作
chart_column.add_series({
    "name": "=表格测试!$C$1",         # 引用业务名称为 图例项 就是标注在旁边的标记
    "categories": "=表格测试!$A$2:$A$6",   # 这个是将什么作为 x 轴 A2到A6
    "values": "=表格测试!$C$2:$C$6",       # 这里是添加第 二 组数据
    "data_labels": {"value": True},       # 显示数字,默认不显示
    "line": {"color": "black"},           # 线条定义为 黑色
})

chart_column.set_title({"name": "展示的标题"})
chart_column.set_x_axis({"name": "x 轴的描述"})
chart_column.set_y_axis({"name": "y 轴的描述"})
chart_column.set_table()   # 设置x轴为数据表格式 不写这个的话就不展示
chart_column.set_style(2)  # 设置直方图的类型，不设置就是默认类型
# 把直方图放到E2 表格位置，这里还可以设置一个{'x_offset': 10, 'y_offset': 5} 表示起点位置偏移量
worksheet.insert_chart("E2", chart_column)  
```

![image-20230215164159701](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215164159701.png)



## 3.下拉选择框

这里是通过 `worksheet.data_validation` 来实现的一些下拉框的选择操作。

```python
import pandas as pd


base_dict = {
    "姓名": ["张三", "李四"],
}
levels = ["炼气", "筑基", "金丹", "元婴", "化神", "炼虚", "合体", "大乘", "渡劫", "小天劫", "大天劫", "仙劫"]
df = pd.DataFrame(base_dict)
with pd.ExcelWriter("下拉框测试.xlsx", engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    worksheet.write("B1", "等级")
    # 可以利用 openpyxl.utils 工具包中提供的一个提供由数字转为 excel 中列号字母的方法: get_column_letter   传入数字得到字母
    # 注释的这里是引用已有数据的模板 当然我们可以像B3那样子主动插入
    # worksheet.write_row("D2", levels)   # 从D2位置开始写入多个数据
    # worksheet.data_validation('B2', {'validate': 'list', 'source': "=$D$2:$O$2"})  # 这里O 是我手动算的 其实有数字转excel上面序号的方法
    worksheet.data_validation('B3', {'validate': 'list', 'source': levels})  # 这里直接引用数据
```

从上面可以看到其实操作很简单 就只是一个方法而已。

![image-20230215171714443](https://static.litetools.top/blogs/pandasxlsxwriter/image-20230215171714443.png)



# 结语

暂时写这么一点点，其他的可以去查看最开始的链接。**点击[这里](#top)回到顶部**

