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


![命令行帮助](https://static.litetools.top/blogs/lite_tools/1.png)
## 🧮 lite-tools fish
这是一个人生日历，没有搞农历节日那些东西，所以这里是标准的**上五休二**制度
## 🧮 lite-tools say
这里基于 [熊与论道兽音](http://hi.pcmoe.net/roar.html) 版块修改算法改成python版本后实现的，并做了智能识别，大概操作如下
![兽语](https://static.litetools.top/blogs/lite_tools/2.png)

新增了 morse --》 可以通过` lite-tools say -h`  查看使用方法

## 🧮 lite-tools acg
这里我没有弄好，主要是这里需要一个自动校准数据这里我没有弄，后面再弄，不复杂，想提前体验可以终端输入自己试一下
## 🧮 lite-tools news

1. 这里默认是获取国内新闻
2. `lite-tools news weibo` 这样子可以获取此时此刻的微博热榜榜单
3. `lite-tools news china/world`后面跟`china`或者`world`可以获取此时此刻中国或者世界上的最新的新闻
3. `lite-tools news paper` 这个和直接输入`lite-tools news`效果一样，只不过这个数据源是**澎湃新闻**，默认是**环球网**
## 🧮 lite-tools today

1. 默认获取今天的黄历，也可以获取今年的节假日，并看经过情况
2. `lite-tools today history`获取历史上的今天的信息
3. `lite-tools today oil`获取今天的油价

## 🧮 lite-tools dict

全程通过输入对应的数字可以查找汉字的拼音，因为拼音你会打就会查，但是不会打的就可以尝试我这个看看。

## 🧮 lite-tools weather
默认根据当前请求`IP`获取当地的天气，当然有可能请求失败，然后会默认返回北京的天气
可以手动指定 **市区县 **然后获取对应地点的天气，后面不用写市区县，如下

> lite-tools weather 天河     获取天河区的天气，如果全国有同名的区就不知道是哪个地方了
> lite-tools weather 广州     这样子就可以获取广州市的 

## 🧮 lite-tools trans
这里需要安装额外的包 `pip install lite-tools[all]`才可以实现以下功能。
**这里是比较复杂的，这里面很多功能我没有实现，目前我只搞了一个图片转pdf。**
**具体的操作可以看 **`**lite-tools trans -h**`
![转换操作](https://static.litetools.top/blogs/lite_tools/4.png)
这里`-i`或者`--input`后面必须要跟输入路径，这后面可以跟文件夹，也可以跟单个图片
`-o`或者`--output`后面是输入文件的位置，这里可以定义输出文件的名称，不写默认同输入文件的名字
示例:
![示例代码](https://static.litetools.top/blogs/lite_tools/11.png)
上面`-i`后面跟了这个文件夹路径  后面`-o`后面自定义了输出的文件名称 这里的`-o`要是不写后面输出的文件就是 和文件夹同名的一个`pdf`

> 这里有个问题，这里是一个图片一页纸 我没有做密度排版，那样子要做很多计算，太麻烦了，反正平时大多数图片都是一页一页的

# 代码里面使用

## 📋 get_lan / get_wan

因为python自带的socket获取内网地址没有那么好用，我自己通过正则写了一个

```python
get_lan()   # 获取内网ip 国内服务器问题不大 英文版本我没有兼容
get_wan()   # 获取外网ip 依赖网络
```



## 📋 get_b64d / get_b64e

就是base64加解密

```python
get_b64d(string)    # 解密base64字符串 可以选择解密模式 
get_b64e(string)    # 加密字符串成base64 可以选择加密模式
```



## 📋 try_get / try_key / FlattenJson / WrapJson

### 📋 try_get

用`jspath` 的方法提取`json串`或者`字典` 

```python
a = {"a": {"b": [0, {"c_123":[0, 1, [3, 4, [{"a": 666}]]]}]}}
print(try_get(a, "a.b[1].c_123[2][2][0].a"))

# try_get(源可以是json字符串可以是字典, 匹配规则, 没有匹配上的时候默认返回的值, expected_type=(int, str))  还有其它参数可以直接看源代码里面的注释
# 可以读取文件,可以读取json字符串,可以把字典转换成json字符串,可以通过`|` 写多个规则
```

{% alertbox warning "注意事项" %}

{% collapse 正常使用的话就不用看了 %}

1. 数组在前的时候不能不加`.` 作为分割

   - 如`a.b[1][2].c` ，**不能** 写成`a.b[1][2]c` 
2. 有几个字符如果是键里面的元素的话，需要加上转义符号

   - 符号有 `.` 、 `[ `、  `]`、  `|`  这四个是键的话要转义

   - 如`{"a|b": [0, {"c.d[]": 666}]}` 解析需要写 `a\|b[1].c\.d\[\]`
3. 如果要提取的键是**整型**或者**浮点型**就不要用我这个方法了
- 如 `{6: {3.14: 666}` 这种我的方法解析不了，主要是我懒得处理这些逻辑 还要判断写在字符串里面的内容是啥类型

{% endcollapse %}



### 📋 try_key

这个结果是列表，因为可以匹配出来多个结果，通过**一个键** 来匹配多个值，或者**一个确定的值** 匹配它的键

```python
a = {"a": {"b": 123}, "c": {"b": 666}}
print(try_key(a, 'b'))  # 这里是匹配 键 为 `b` 的值 [123, 666]
print(try_key(a, 666, mode='value'))  # 通过值666来找键  "b"  
# 同样这里可以设置期望要的类型 但是只适合键取值
options = {"filter": {"equal": {"key1": "value1", "key2": "value2"}, "unequal": {"key1": "value1"}}}
# 上面参数的意思就是 设置过滤器 但是这个过滤器只适合匹配 兄弟元素关系 如 key1 和 key2 在同一个作用域这种     
```



### 📋 FlattenJson

这里是扁平化json,就是把一个很大的`json` 可以变成一元的,然后也可以通过jspath的方法取值那些

```python
a = {"a": {"b": [666, [777, 888]]}, "c": 123}
app = FlattenJson(a)
app.show()   # 这个没有返回值,直接打印出来扁平化的内容 
# {'a.b[0]': 666, 'a.b[1][0]': 777, 'a.b[1][1]': 888, 'c': 123}
for key, value in app.get_all():  # 迭代器
    pass   # 可以拿到每个路径 和 值
for key in app.path(value):
    pass   # 可以拿到每个值的路径
print(app.get(key, default=None))  # 通过路径获取对应的值 没有返回默认值
print(app.exists(key))  # 判断路径是否存在
```



### 📋 JsJson

这个我没有搞完,反正大概意思就是从html啥的文本里提取json出来,目前这里没啥用



### 📋 WrapJson

折叠json, 把一个很大的json或者字典按照想要的格式进行压缩

```python
a = {"a": "666", "b": {"c": [123], "d": 777}, "e": 3.14}
app = WrapJson({"a": str, "b": {"c": list}, "e": ...})  # 这里传入的是模板,就是想要获得的结果模板

print(app.get_all(a)) --> {'a': '666', 'b': {'c': [123]}, 'e': 3.14}
```

{% alertbox danger "使用注意事项" %}

{% collapse WrapJson的使用注意点 open %}

1. `...` 只适用于 基本类型`str, int, float, bool` 的模糊匹配, 数组类型的`tuple, dict, list, set` 不适用
2. 如果是数组类型,必须指明,如上面`c` 的情况
3. 如果获取结果的值和模板匹配不上 将会返回空数组类型 `{} / []` 

{% endcollapse %}



## 📋 get_md5 / get_sha / get_sha3

这里没啥好说的 就是如命加密 都有可以指定类型的参数,直接看方法就知道转啥了



## 📋 get_time / time_count / time_range

### 📋 get_time

时间转换, 方法都可以组合使用

```python
get_time()   # 默认获取当前时间时间戳  10位
get_time(unit='ms')  # 获取13位的时间戳
get_time(instance=float)  # 获取浮点类型的时间戳
get_time(fmt=True)     # 获取 YYYY-mm-dd HH:MM:SS 格式的时间
get_time(fmt="%Y%m")   # 手动指定获取YYYYmm 格式的时间
get_time(1656546540, fmt=True)     # 将指定时间戳转换为默认时间格式
get_time(1656546540000, fmt="%Y%m")   # 将指定时间戳转换为指定格式的时间格式 这里可以13位或者10位 兼容了的
get_time("2022-10-11")             # 将时间格式转换为时间戳 默认匹配了 年月日/.///- 其它格式需要自己手动指定 
get_time("2022/12/12 10:11", fmt="%Y/%m/%d %H:%M")    # 没有内置的格式 需要手动指定格式 转换位时间戳 
get_time("2022-10-11", unit='ms')   # 转换出来的时间戳为13位
```



### 📋 time_count 

获取函数运行时间的装饰器



### 📋 time_range

获取起止时间的时间戳范围

```python
# (年,月,日,时,分,秒) 开始时间不可以比结束时间大 不写的位置默认为当前值最小值 如 (2022, 11) 只写了年月,那么日 时分秒是  1, 00:00:00
time_range((2022,11), (2022,12,6))              # (1667232000, 1670256000)
time_range((2022,11), (2022,12,6), unit='ms')   # (1667232000000, 1670256000000)
```



## 📋 try_catch

捕获异常的装饰器, 支持**同步**和**异步**

```python
@try_catch     # 不加参数默认正常捕获
# 下面是我随便写一些值来理解,都可以不写都有默认值
@try_catch(
    log=False,  # 不打印日志                默认打印
    retry=5,    # 如果异常了再重试 最多运行5次 默认1次
    default=666,  # 捕获完了还是异常给的默认值 默认None
    timeout=10,   # 异常了等10秒再重试或者10秒后再推出 默认不等待
    err_callback=send_dingding,  # 如果最后报错了触发这个函数 默认没有 如果有参数需要加下面那个
    err_args=("xxx失败了",)       # 这里只能是序列 列表 元组都行 但是得对应上面回调函数的参数
    except_retry=(TimeoutException, ValueError)  # 如果是碰到了这两种异常 直接就不重试了 直接返回默认值
    ignore_retry=KeyError,    # 和上面参数一样可以单写,可以多写 但是这里是如果碰到了这种异常,直接跳过等待继续重试
    catch=False,              # 默认就是False 这里是捕获异常的原因,一般不建议设置为True的时候不要和其它写一起
)  
```



## 📋 get_ua

获取user-agent 真实版本号

```python
get_ua()                # 随机获取一个 基本都是chrome的
get_ua('pc')            # 可以从ie edge firfox chrome 里面随机取 太随机了
get_ua('mobile')        # 随机获取一个手机ua
get_ua('chrome', 'ie')  # 随机从chrome/ie里面获取一个ua
```



## 📋 MySql / MySqlConfig / SqlString

描述复杂 这是给我自己使用方便的 如果你们要用的话 最好用 `MySqlConfig` 配置了传入MySql创建一个属于自己的

可以设置返回值的类型 在配置文件里面 有一个 `cursor`参数 默认`tuple`,可以设置为`dict` ，这里是**字符串**哦.

下面所有的`where` 都可以写字典和字符串 字典只有等值, 字符串就是你想写啥规则就是啥规则

```python
mysql = MySql(MySqlConfig(database="test", host="xxx", user="aaaaa", password="xxxx", port=6666), table_name="t1")  
# 还有其它参数自己看接口
# 增
mysql.insert({"a": 123})
# 删 
mysql.delete({"a": 666})
# 改
mysql.update({"a": 888}, {"b": 111})
# 查
for a, b in mysql.select("SELECT a, b FROM xxxx WHERE ..."):  # 可以选择的fetch模式有 one all many 设置many的话 可以设置buffer=1000  默认就是1000
    pass  # a, b 对应后面sql语句查出的个数 不确定的话 for xxx in  一个参数就行 是个元组

# 大量的数据建议用这个
for a, b in mysql.select_iter("SELECT a, b FROM xxxx WHERE ...", "这里写主键用来记录游标位置的"):
    pass  # a, b 对应后面sql语句查出的个数 不确定的话 for xxx in  一个参数就行 是个元组

# 统计
count = mysql.count()  # 不写统计全部 可以写规则
e = mysql.exists({"a": 66})  # 判断a=66是否存在 
```

```python
# 假如返回字典格式的
mysql = MySql(MySqlConfig(database="test", host="xxx", user="aaaaa", password="xxxx", cursor='dict', port=6666)) 
# 这里其实可以不写 表名 ，只实例化一次 后续可以在每个操作位置单独指定表名

# --------------------
# 注意：实例化位置和下面方法的位置 至少有一个地方写表名 两个地方都写 优先采取方法位置的表名来进行操作
# -------------------

# 如 增
mysql.insert({"a": 123}, ignore=True, table_name="这里可以单独指定表名")  # 所以程序里可以只实例化一次 插入同一个库的不同表

# 批量插入  批量插入支持以下两个形式 字段都要对应 长度也要对应
items1 = {
	"_id": ["0015", "0016", "0017", "0018"],
	"api": ["5", "6", "7", "8"],
	"platform": ["a", "b", "c", "d"],
	"status_code": [1, 1, 6, 9]
}
items2 = [
	{"_id": "1111", "api": "11", "platform": "aaa", "status_code": 5}, 
	{"_id": "2222", "api": "22", "platform": "bbb", "status_code": 7},
	{"_id": "3333", "api": "33", "platform": "ccc", "status_code": 7},
	{"_id": "4444", "api": "44", "platform": "ddd", "status_code": 8},
]
mysql.insert_batch(itemsX)  # 直接操作 如果碰到主键重复 这一堆会插入异常 会提示错误
mysql.insert_batch(itemsX, duplicate="ignore")   # 去重模式选择 ignore 那么重复的主键将会跳过 不会修改原值
mysql.insert_batch(items, duplicate="update", update_field=["status_code"], table_name="表名")
# 插入模式采用更新，如果有主键重复的数据 会更新 update_field 里面的字段的数据


# 批量更新 这个 目前 暂时 只支持 上面 items1 的格式 更新域和条件长度的一致
mysql.update_batch({"a": [1, 2, 3], "b": ["x", "y", "z"]}, {"c": ["aa", "bb", "cc"]}, table_name="同理这里不写就得全局写 二选一")
# 上面的意思是 把 "c" 值等于"aa"的内容的 "a" 更新为 1, "b" 更新为 "x" 
# 上面的意思是 把 "c" 值等于"bb"的内容的 "a" 更新为 2, "b" 更新为 "y" 
# 上面的意思是 把 "c" 值等于"cc"的内容的 "a" 更新为 3, "b" 更新为 "z" 
```



## 📋 match_case

可以让你的if-else 更加好看

```python
@match_case
def main(x):
    return "默认值"

@main.register(666)
def when_x_666(x):
    return "当x为666的时候走这里逻辑"

@main.register_all(["asd", 444])
def when_x_other(x):
    return "当x为 上面列表里面两种情况的时候走这里逻辑"
```



## 📋 CleanString

可能不好用 就是清理字符串的字符的



## 📋 clean_html
采用了米乐大佬的 `usepy` 的包实现的
```python
clean_html(html文本, white_tags=["p"])
```



## 📋 color_string

返回一个有颜色的字符串

```python
print(color_string("你好", "红"))   # 可以写 红,红色,red, R  其它颜色同理
print(color_string("哈哈", {"b": "黑", "f": "y", "v": "bold"}))  # 对应backgroud front view
```



## 📋 x_timeout

{% alertbox primary "TODO" %}

需要兼容同步和异步,所以这里有问题,这个也是不可用的状态



## 📋 Singleton

单例模式装饰器



## 📋 Buffer

一个队列,配合V神的vthread使用有奇效, 如果一个地方设置`name` 对应的其它的都需要设置对应的name

```python
import vthread
from lite_tools import Buffer

@vthread.pool(1, gqueue=1)  # 任务线程
@Buffer.task                # 声明这个任务 可以加名称
def task():
    yield 1                 # 任务全部通过yield推送到队列
    
@vthread.pool(10, gqueue=2)  # 消耗线程
@Buffer.worker              # 声明消耗任务的 名称需要和任务的名称对应 默认名称都是default 可以设置 @Buffer.worker(name="设置了名字其它的所有功能都需要创建这个名字才可以对应起来")
def run():
    # 这里不需要写循环 这个worker会自动循环取队列
    item = Buffer.seed()   # 这里返回的内容是和上面的yield对应 如果yield a, b  那么这里建议  a, b = Buffer.seed() 
    print(item)

if __name__ == "__main__":
    task()
    for _ in range(10): run()
        
# 此外还有好几个方法
Buffer.reset()  # 重置统计的数据
Buffer.size()   # 获取当前队列里面剩余任务
Buffer.count()  # 获取跑了多少个任务
Buffer.sow(666)  # 放一个新的数据进队列 << 一般不建议用这个 可能会造成队列阻塞
```



## 📋count_lines

统计文件行数

```python
print(count_lines("文件路径", encoding='不写的话默认系统对应的格式'))
```



## 📋LiteLogFile

创建一个日志记录 采用循环记录 同一个位置只会存在10000条最多 超了从0开始记录 在用户目录下`.lite_tools/logs/xxx`下面可以找到记录

```python
log_file = LiteLogFile('主目录', '日志名称')
log_file.dump("这里是一条日志")
```



## js相关的

{% alertbox primary "TODO" %}

主要是js里面 进制转换 比如36进制啥的 大部分代码由 `小小白` 提供
```python
# 两种引用方式
from lite_tools import atob, btoa, to_string_36, xor, unsigned_right_shift, left_shift, dec_to_bin

# 或者
from lite_tools.tools.js import atob, btoa, to_string_36, xor, unsigned_right_shift, left_shift, dec_to_bin

# 是一样的 就是方法区分功能 和不管区分与否的 差别
```

### 📋atob/ btoa  base64功能


### 📋to_string_2

### 📋to_string_16

### 📋to_string_36 

```python
# >>>>>>>> 但是这个还没有实现浮点数的转换操作
# js>>> (123456789).toString(36)
to_string_36(5615)   # 将数字转换为 36 进制
```

### 📋xor

```python
# js>>> 656616 ^ 516565
# 数字都是我随便写的 这个和python的区别在于精度不同 python 的 ^ 数字小的时候没问题 数字大就不对了
xor(565646, 98486)
```

### 📋unsigned_right_shift

```python
# js>>> 555 >>> 1
# 主要是实现js的上面操作  数字我乱写的
unsigned_right_shift(555, 1)
```

### 📋left_shift

```python
# 主要是解决和python的精度差别问题
# js>>>   555 << 2
left_shift(555, 2)
```

### 📋 dec_to_bin 

同上面的 >>>  to_string_2

```python
# 主要是解决 十进制 浮点数 转 二进制 的精度 问题
# js>>> (56.541).toString(2)
dec_to_bin(56.541)
```

