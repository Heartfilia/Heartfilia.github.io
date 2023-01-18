---
title: 【数据转换】python实现其它代码中轻易实现的逻辑
date: 2022-12-14 10:19:22
tags: python
categories: 代码
toc: true
---

一些在其它语言可以轻易实现的功能，但是在python中会有点误差的实现方案

这里的内容会持续更新，新增！

<!-- more -->

# JS板块


## 一. 浮点数转二进制

{% collapse 实现方案一 %}

```python
#十进制浮点数转二进制
def dectbin(num):
    # 判断是否为浮点数
    if num == int(num):
        # 若为整数
        integer = '{:b}'.format(int(num))
        return integer
    else:
        # 若为浮点数
        # 取整数部分
        integer_part = int(num)
        # 取小数部分
        decimal_part = num - integer_part
        # 整数部分进制转换
        integercom = '{:b}'.format(integer_part)  #{:b}.foemat中b是二进制
        # 小数部分进制转换
        tem = decimal_part
        tmpflo = []
        # for i in range(accuracy):
        A = True
        while A:
            tem *= 2
            tmpflo += str(int(tem))  #若整数部分为0则二进制部分为0，若整数部分为1则二进制部分为1 #将1或0放入列表
            if tem > 1 :   #若乘以2后为大于1的小数，则要减去整数部分
                tem -= int(tem)
            elif tem < 1:  #乘以2后若仍为小于1的小数，则继续使用这个数乘2变换进制
                pass
            else:    #当乘以2后正好为1，则进制变换停止
                break
        flocom = tmpflo
        return integercom + '.' + ''.join(flocom)

if __name__ == '__main__':
    number = 5
    result = dectbin(number)
    print(f'{number}的二进制数为：{result}')
```

{% endcollapse %}



{% collapse 实现方案二 %}

```python
import ctypes

def xor(x, y):
    x, y = ctypes.c_int32(x).value, ctypes.c_int32(y).value
    return ctypes.c_int(x ^ y).value


def unsigned_right_shift(x, y):
    x, y = ctypes.c_uint32(x).value, y % 32
    return ctypes.c_uint32(x >> y).value


def left_shift(x, y):
    x, y = ctypes.c_int32(x).value, y % 32
    return ctypes.c_int32(x << y).value


def right_shift(x, y):
    x, y = ctypes.c_int32(x).value, y % 32
    return ctypes.c_int32(x >> y).value


def dectbin(num):
    # 判断是否为浮点数
    if num == int(num):
        # 若为整数
        integer = '{:b}'.format(int(num))
        return integer
    else:
        # 若为浮点数
        # 取整数部分
        integer_part = int(num)
        # 取小数部分
        decimal_part = num - integer_part
        # 整数部分进制转换
        integercom = '{:b}'.format(integer_part)  #{:b}.foemat中b是二进制
        # 小数部分进制转换
        tem = decimal_part
        tmpflo = []
        # for i in range(accuracy):
        A = True
        while A:
            tem *= 2
            tmpflo += str(int(tem))  #若整数部分为0则二进制部分为0，若整数部分为1则二进制部分为1 #将1或0放入列表
            if tem > 1 :   #若乘以2后为大于1的小数，则要减去整数部分
                tem -= int(tem)
            elif tem < 1:  #乘以2后若仍为小于1的小数，则继续使用这个数乘2变换进制
                pass
            else:    #当乘以2后正好为1，则进制变换停止
                break
        flocom = tmpflo
        return integercom + '.' + ''.join(flocom)
```

{% endcollapse %}



{% collapse 实现方案三 %}

```python
def conversion_of_binary(number):
    global binary_integer_part, binary_fractional_part, binary_total, integer_part, fractional_part

    # 整数部分
    integer_part = int(number)
    binary_integer_part = bin(integer_part)[2:]  # a[2:]

    # 小数部分
    fractional_part = number - integer_part
    binary_fractional_part = conversion_of_fraction(fractional_part, 2)

    # 拼接
    binary_total = binary_integer_part + '.' + binary_fractional_part
    return binary_total


# CONVERSION TO FRACTION PART TO BINARY
def conversion_of_fraction(num, base):
    binary = ''
    while num != 0:
        num = num * base
        binary = binary + str(int(num))
        num = num - int(num)
    return binary

if __name__ == "__main__":
	result = conversion_of_binary(2.8)
```

{% endcollapse %}



## 二、逻辑运算转换

在 JavaScript 内部，数值都是以 64 位浮点数的形式储存，但是做位运算的时候，是以 32 位带符号的整数进行运算的，并且返回值也是一个 32 位带符号的整数。目的是使在 python 中的显示和 js 中的显示相同，就在 Python 中做一次从 uint32 到 int32 的转换。


### 1.逻辑符号 ^

{% collapse 实现方案一 %}

```python
import struct

num = 3988292384 ^ 127
print(num)                                           # 3988292447

print(struct.unpack('i', struct.pack('I', num))[0])  # -306674849
```

{% endcollapse %}



{% collapse 实现方案二 %}

```python
def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

print(int_overflow(3988292384 ^ 127))                # -306674849
```

{% endcollapse %}



### 2.无符号右移 >>>

这里目前还没有完美的方案，数据量非常大的时候可能需要加上 板块二 **逻辑符号 ^** 里面数据量过大情况进行数据修正，大概意思就是这个得出来的结果再套一层。

**示例**：采用逻辑符号 ^ 方案二 --> `int_overflow(这里就是无符号右移得出来的结果)`

{% collapse 实现方案一 %}

```python
def unsinged_right_shift(x, y):
    x = x & 0xffffffff
    signed = False
    if x < 0:
        signed = True
    x = x.to_bytes(4, byteorder='big', signed=signed)  # 有符号
    x = int.from_bytes(x, byteorder='big', signed=False)  # 无符号
    return x >> (y & 0xf)
```

{% endcollapse %}



{% collapse 实现方案二 %}

```python
import ctypes


def unsinged_right_shift(x, y):
    x,y = ctypes.c_uint32(x).value,y % 32
    return ctypes.c_uint32(x >> y).value
```

{% endcollapse %}



{% collapse 实现方案三 %}

```python
MAX32INT = 4294967295

def unsinged_right_shift(num, bit=0) -> int:
    # example: 
    #   javascript: -1 >>> 1 === python: right_without_sign(-1, 1)
    val = ctypes.c_uint32(num).value >> bit
    return (val + (MAX32INT + 1)) % (2 * (MAX32INT + 1)) - MAX32INT - 1
```

{% endcollapse %}



{% collapse 实现方案四-小小白提供 %}

```python
def unsinged_right_shift(signed, i=0):
    shift = signed % 0x100000000
    return shift >> i
```

{% endcollapse %}
