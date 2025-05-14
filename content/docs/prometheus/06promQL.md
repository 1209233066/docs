---
title: "PromeQL"
linkTitle: "PromeQL"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 6
description: >
  PromeQL|prometheus

tags: ["prometheus","PromeQL",]
categories: ["prometheus","监控"]
url: prometheus/promeql.html
---


[promQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) 是prometheus时序数据库的查询语言，可以类比为关系数据库中的SQL。

### 指标类型：

---



+ gauge: 是一个状态的瞬时快照，值可增可减。配合 `changes` `delta` `predict_linear` `deriv`

+ counter: 是一个累加的指标，自metrics启动以后该值一直累加。 配合 `rate` ` irate` `increase`

+ summary: 摘要可以展示数据分布 ,允许计算百分位数

  ```bash
  count
  sum
  quantitle
  ```

  

+ histogram: 直方图可以展示数据分布，按照桶把数据分布投递到不同桶中。直方图的数值是累计的，后一个包含前一个桶中的数据。`histogram_quantile`

  ```
  count
  sum
  le
  histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
  ```
  
  



### 查询结果数据类型：

---



- 即时矢量: 一组时间序列，其中包含每个时间序列的单个样本，所有时间序列共享相同的时间戳
- 范围向量: 一组时间序列，其中包含每个时间序列随时间变化的数据点范围
- 标量: 一个简单的数字浮点值
- 字符串: 一个简单的字符串值;



### 查询语句:

---

**基本语法**

示例格式一：
```bash
http_requests_total{code="200",method="get"}
					    !=
					    =~ 选择正则表达式与提供的字符串匹配的指标
					    !~ 选择正则表达式与提供的字符串不匹配的指标
```
示例格式二：
```bash
{job=~".+"}
{job=~".*",method="get"} 
```

示例格式3：
```bash
{__name__="http_requests_total"}
{__name__=~".*total$"}
```
示例格式4：
```bash
http_requests_total @ 1609746000
sum(http_requests_total{method="GET"} @ 1609746000)
```

示例格式5:
```bash
http_requests_total offset 5m
sum(http_requests_total{method="GET"} offset 5m)
```
示例格式6:
```bash
{__name__="http_requests_total"}[1m]
								  ms
								  s
								  m
								  h
								  d
								  w
								  y
```



**标签表达式**


| 表达式 | 释义               | 示例                                                         |
| ------ | ------------------ | ------------------------------------------------------------ |
| **=**  | 精确匹配给定的值   |                                                              |
| **!=** | 精确不匹配给定的值 |                                                              |
| **=~** | 正则匹配给定的值   | `http_requests_total{environment=~"staging|testing|development", method!="GET"}` |
| **!~** | 正则不匹配给定的值 |                                                              |

**聚合操作：**

1. 基于标签聚合

|              |              |                                |                                                      |
| ------------ | ------------ | ------------------------------ | ---------------------------------------------------- |
| 聚合操作分组 | by           |                                | `sum by(code) (method_code:http_errors:rate5m)`      |
|              | without      |                                | `sum without(code) (method_code:http_errors:rate5m)` |
| 聚合操作符   | sum          | 求和                           |                                                      |
|              | count        | 计数                           |                                                      |
|              | avg          | 平均值                         |                                                      |
|              | max          | 最大值                         |                                                      |
|              | min          | 最小值                         |                                                      |
|              | topk         | 按样本值计算的最大 k 个元素    | `topk(2,method_code:http_errors:rate5m)`             |
|              | bottomk      | 按样本值排列的最小 k 个元素    |                                                      |
|              | quantile     | 计算φ分位数（0 ≤ φ ≤ 1）的尺寸 |                                                      |
|              | count_values | 计算具有相同值的元素数         |                                                      |
|              | stddev       | 标准偏差                       |                                                      |
|              | stdvar       | 标准与维度的方差               |                                                      |
|              | group        | 结果向量中的所有值均为 1       |                                                      |

2. 基于时间聚合

   `_over_time` 可以做到保留标签

**运算符：**

+ 算术运算

  <sub>作用范围：（浮点数与浮点数	浮点数与瞬时向量		瞬时向量与瞬时向量），瞬时向量间标签k,v必须保持完全一致</sub>

  |      |        |      |
  | ---- | ------ | ---- |
  | +    | 添加   |      |
  | -    | 减法   |      |
  | *    | 乘法   |      |
  | /    | 取商   |      |
  | %    | 取余数 |      |
  | ^    | 幂     |      |

  

+ 比较运算符

  <sub>作用范围：（浮点数与浮点数	浮点数与瞬时向量		瞬时向量与瞬时向量）</sub>

  |      |          |      |
  | ---- | -------- | ---- |
  | ==   | 等于     |      |
  | !=   | 不相等   |      |
  | >    | 大于     |      |
  | <    | 小于     |      |
  | >=   | 大于等于 |      |
  | <=   | 小于等于 |      |

  

+ 逻辑运算符

  > <font color=red>逻辑运算两边的标签保持一致</font>
  
  |        |                       |      |
  | ------ | --------------------- | ---- |
  | and    | 交集                  |      |
  | or     | 并集                  |      |
  | unless | 补集,左侧有右侧没有的 |      |
  
  



向量匹配
+ one-to-one
+ many-to-one and group_left
+ many-to-many

<span id='xiangliangpipei'>**向量匹配**</span>

> 必须具有相同的标签，如果一方标签过多可以使max by 保留指定标签

```bash
--collector.textfile --collector.textfile.directory="."
```

```bash
vi httpcod.prom

#输入示例：
method_code:http_errors:rate5m{method="get", code="500"}  24
method_code:http_errors:rate5m{method="get", code="404"}  30
method_code:http_errors:rate5m{method="put", code="501"}  3
method_code:http_errors:rate5m{method="post", code="500"} 6
method_code:http_errors:rate5m{method="post", code="404"} 21

method:http_requests:rate5m{method="get"}  600
method:http_requests:rate5m{method="del"}  34
method:http_requests:rate5m{method="post"} 120
```



**One-to-one:** 两侧如果具有相同的标签和键  => 则匹配。**on** 在指定标签上进行匹配，**ignoring**则忽略指定标签 

语法：

```bash
<vector expr> <bin-op> ignoring(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) <vector expr>
```

事例:

```bash
# method_code:http_errors:rate5m{method="get", code="500"}  24
# method_code:http_errors:rate5m{method="post", code="500"} 6

# method:http_requests:rate5m{method="get"}  600
# method:http_requests:rate5m{method="post"} 120
method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m
```

结果

```bash
{method="get"}  0.04            //  24 / 600
{method="post"} 0.05            //   6 / 120
```



**Many-to-one** and **one-to-many** :  在向量的一侧可以找到多个与之对应的记录

少的一次都能在多的一侧找到对应的 指标。

使用 group_left 和 group_right 指定哪一侧位多的一侧

使用on 和 ignore 指定参照哪个标签进行运算

语法：

```bash
<vector expr> <bin-op> ignoring(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> ignoring(<label list>) group_right(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_right(<label list>) <vector expr>
```

事例:

```bash
#group_left 和 group_right 参照 one-to-many 的many 一侧
method_code:http_errors:rate5m / ignoring(code) group_left method:http_requests:rate5m
```

结果

```bash
{method="get", code="500"}  0.04            //  24 / 600
{method="get", code="404"}  0.05            //  30 / 600
{method="post", code="500"} 0.05            //   6 / 120
{method="post", code="404"} 0.175           //  21 / 120
```

### 函数

|                                    |                                                              |                                        |
| ---------------------------------- | ------------------------------------------------------------ | -------------------------------------- |
| up                                 | 服务是否存活                                                 |                                        |
| absent                             | 即时向量指标存在什么都不返回，不存在返回1                    |                                        |
| abs                                | 绝对值                                                       |                                        |
| absent_over_time                   | 用于判断范围向量`absent_over_time(up1[10m])`                 |                                        |
| ceil                               | 四舍五入                                                     |                                        |
| floor                              | 舍小数取整                                                   |                                        |
| time                               | 返回时间戳                                                   |                                        |
| changes                            | 记录变化的次数，比如一个任务从up 变为down 后又变为up  此时应该返回2 | `changes(up[5m])>0`                    |
| increase<sub>【用于counter】</sub> | 截取 counter 类型一个时间段的增量                            | `increase(node_cpu_secound_total[1m])` |
| irate <sub>【用于counter】</sub>   | 每秒变化量                                                   |                                        |
| rate <sub>【用于counter】</sub>    | 每秒变化量                                                   |                                        |
| sort                               |                                                              |                                        |
| sort_desc                          |                                                              |                                        |
| topk                               |                                                              |                                        |
| bottomk                            |                                                              |                                        |
| delta                              | 截取 counter 类型一个时间段的增量                            | `delta(node_cpu_seconds_total[10m])`   |



1. label_replace
   
   > 替换标签和内容


   **语法**

   ```bash
   label_replace(__input_vector__,"__dst__","__replacement__","__src__","__regex__")
   ```

   **举例**

   ```bash
   label_replace(lv_pool_total,"lv_name_new","$1","lv_name","(.*)")
   ```

2. label_join
   
   
   **语法**

   **举例**
