---
date: '2025-05-20T21:44:02+08:00'
draft: false
title: 'Groovy'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  groovy|jenkins
tags: ["jenkins","groovy"]
categories: ["devops"]
url: devops/groovy.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)


#### groovy 语法


##### 注释

```groovy
// 单行注释
```

```groovy
/*
多行注释
*/
```

```groovy
/*
* 文档注释
* 这个函数的使用方法
*/
```



##### 变量

```groovy
// 变量定义
def name="hello world!"
```

字符串

```groovy
str="中国"
```



```groovy
// 字符串拼接
str=str + "-beijing"
// 字符串分割 split() ,分割后生成数组
printf("我来自%s",str.split("-")[0])

//  首字符大写 capitalize()
printf("我来自%s",str.split("-")[1].capitalize())

// 大写 toUpperCase()
printf("我来自%s",str.toUpperCase())

// 大写 toLowerCase()
printf("我来自%s",str.toLowerCase())

// 字符串长度
str.size()

```



数字

数组

```groovy
//  数组
a_list=[1,2,3,4,5,6]
println a_list.getClass().getName() // 数据类型 java.util.ArrayList

for(i in a_list){
    println i
}
// 数据嵌套
b_list=[1,2,3,4,5,6,["a","b"]]

// 数组新增元素
b_list.add("新成员")
b_list.add(2,"在索引为2 的位置插入")
println b_list  //[1, 2, 在索引为2 的位置插入, 3, 4, 5, 6, [a, b], 新成员]

// 通过语法糖 追加元素
b_list << "hello world"
println b_list  //[1, 2, 在索引为2 的位置插入, 3, 4, 5, 6, [a, b], 新成员, hello world]


// 除了for之外遍历元素的方法，${it} 为内置变量
b_list.each{println "成员：${it}"}
```



map

```bash
// map
a_map=[name:"张三"]
println
a_map.getClass().getName()  // java.util.LinkedHashMap

// 调用方法和python 很类似
a_map.name
a_map["name"]
a_map.get("name")

// 添加元素
a_map["age"]=18

// 遍历元素
a_map.each{println"${it},分别获取可以和value: ${it.key}--${it.value}"}
```





##### 运算符

赋值运算符： `= += -= /= %=`

算数运算符： `+ - * / % ++ --`

关系运算符： `== != > < >= <=`

逻辑运算符： `&& || !`

位运算符： `& | ^ ~`

范围运算符：

```bash
def a=1..5
a.getClass().getName() //类型: groovy.lang.IntRange
a.get(1) // 按照索引取值
```



##### for while if switch 

**for** 

```groovy
for(def i=0;i<5;i++){
    println i
}
```

**for in**

```groovy
def a="123"
// a 是一个可迭代对象，和python类似
for(i in a){
    println i
}
```

**times**

```groovy
// 循环0 到9 
10.times{ i ->
    println i
}
```



```groovy
info = [
    ["id": 1, "name": "张三"],
    ["id": 2, "name": "李四"]
]
// 格式1：
for (i in info) {
    println i.name
}


newinfo=[]
for (i in 0..info.size() - 1) {
    newinfo << info[i].name
}

// 格式2

for(i=0;i<info.size();i++){
    println info[i]
}
```



**while**

```groovy
def conut=0
while(conut <5){
    println "${conut}"
    conut++
}
```



**if**

```groovy
def score=0
if (score<60){
    println "再接再厉"
}else{
    print  "恭喜你"
}
```

```bash
def score=60
if (score<60){
    println "再接再厉"
}else if(score==60){
	println "运气不错"
}else if(score>60 && score<=100){
	println "你太厉害了"
}
```

**switch** 

```groovy
def type = "linux"
switch(type) {
    case "linux":
        println "操作系统为linux"
        break
    case "windows":
        println "操作系统为windows"
        break
    default:
        println "其他操作系统"
        break
}
```



##### 函数

```groovy
def sum(){
    println "不带参数的函数"
}
sum()
```

```groovy
def sum(num1,num2){
    println "带参数的函数\n "
    println num1 + num2
}
sum(1,2)
```

```groovy
def sum(num1=1,num2=2){
    println "带参数的函数,设置了默认值\n "
    println num1 + num2
}
sum()
```

```bash
def sum(num1=1,num2=2){
    println "带参数的函数,设置了默认值和返回值\n "
    return num1 + num2
}
a=sum()
println a
```

##### 异常处理

```groovy
// 异常处理
// try catch finally
try {
    println  name
}catch(Exception e){
    println e
}finally {
    println "always"
}
```