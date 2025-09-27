---
date: '2025-07-02T08:34:29+08:00'
draft: false
title: 'Stock'
type: blog
toc_hide: false
hide_summary: true
weight: 5
description: >
  通过akshare获取股票数据
tags: ["akshare"]
categories: ["股票"]
url: 2025-07-02/stock.html
author: "wangendao"
---

![](https://x0.ifengimg.com/ucms/2021_22/DF8F37DEB91E6A619D22FA250D02E6A52CF6CCE2_size37_w1024_h728.jpg)



写在前面的话：牛市不畏高，寻早龙头买入

### 基本概念

+ 股票是一个零和博弈么，为什么在牛市大家都挣钱而熊市基本都亏钱，挣得钱有谁出亏的钱又去了哪里？

+ **PB**(Price-to-Book Ratio, PB) ：`市净率 = 股价 / 每股账面值`也就是市值与总资产的比率

+ **PE** ：`市盈率=现时股价 / 公司盈利` 也就是市值与利润的比率

  往往只可以与同一行业或板块比较平；而且PE计算公司盈利时，往往基于上一年业绩，未必能够反映企业最新情况，例如当公司业务有变动或转型，这个计法就未必适合。

+ **货币政策-MLF**：（Medium-term Lending Facility）是指中央银行提供中期（三个月以上通常为一年）基础货币的货币政策工具，MLF的发放对象是符合监管要求的商业银行和政策性银行，发放方式为质押（质押物可以是：国债、央行票据、政策性金融债、高等级信用债等优质债券）方式。MLF利率会影响到LPR

  贷款市场报价利率（LPR）是指由各报价行按照公开市场操作利率加点形成的利率，由全国银行间同业拆借中心计算得出，为银行贷款提供定价参考。具体来说，LPR主要由中期借贷便利利率（MLF）加点形成，反映了市场资金成本和银行的加点成本。LPR包括1年期和5年期以上两个品种，分别用于不同期限的贷款定价。LPR的形成机制确保了其能够及时反映市场利率变化，为实体经济融资成本的降低提供政策引导

  

+ **货币政策-降息**

  | **操作**   | **资金流向** | **抵押品流向** | **目的**               |
  | :--------- | :----------- | :------------- | :--------------------- |
  | **逆回购** | 央行 → 市场  | 市场 → 央行    | **释放流动性**（放水） |
  | **正回购** | 市场 → 央行  | 央行 → 市场    | **回收流动性**（抽水） |



+ **k线**

+ **换手率**

  > 适用于A股大盘，创业板和北交所需要更高指标

  ![image-20250924164212547](C:\Users\pc\AppData\Roaming\Typora\typora-user-images\image-20250924164212547.png)

  \>5% 代表较为活跃，如果处于低位考虑建仓。

  \>15% 可能主力在吸筹，如果在低位震荡中出现考虑建仓 。

  

  \>20% 

+ **筹码峰**

+ **量价关系**

+ **股票质押和解除质押对股价的影响**

+ **如何看待涨停板：**

+ ​    极强	＞流通股本10%	主力锁仓，连板概率高
  ​    中等	3%~10%流通股本	需结合板块与资金流向判断，第二天上涨6%以上概率较大
  ​    弱势	＜3%流通股本	抛压风险大，易开板

  ​    **若换手率＞10%，即使封单量大，也可能存在主力对倒出货**

  **参考样本：**

  | 涨停时间       | 样本     | 临近收盘时买一占比                   | 换手率 |      |       |
  | -------------- | -------- | ------------------------------------ | ------ | ---- | ----- |
  | 20250924 11:15 | 中国宝安 | 买一1.23亿 流动股25.76亿 ，占比4.77% | 3.82%  | 首板 | 3.45% |
  | 20250924 11:00 | 彤程新材 | 买一0.92亿 流动股5.97亿 ，占比15.41% | 6.68%  | 首板 | 0%    |

  宁波海运 23.60%

  





1. 美联储预期9月中旬降息==》 美国降息25% 当天大跌，第二天延续跌至第四天止跌

2. 脑机接口--》 人工智能、智慧医疗

3. 8月12号美国启动新一轮关税战，延期90天至11月中旬

4. 养护翻新农村公路--》 基建

5. 铝、铜工业必须品

6. 2025规划中提出大力发展 智能网联新能源汽车、人工智能手机和电脑、智能机器人

7. 通货紧缩、产能过剩、美印关税冲突利好苹果供应链、钢铁、铝

8. 商业航天，中国星链、[海南卫星工厂投产](https://www.hainan.gov.cn/hainan/5309/202503/64a2bbd1b26e455d88d89e62f196d07c.shtml)  ==> 中国星网、中国卫通、3大运营商、后期带动物联网发展【选出2家公司】

9. 宇树科技ipo,关联投资方、上游供应商【选出2家公司】

   ![](https://mmbiz.qpic.cn/sz_mmbiz_png/sHms2rgVZUYTDokFftml1xuFDV6BYZHGUlJGdQITVxWIdUCd6VoyNqLJZuODZa3uGDibib8GJG247hcdpbnic0h0Q/640?wx_fmt=png&from=appmsg&watermark=1)



```bash
FROM python:3.11.12-alpine3.21

LABEL maintainer=1209233066@qq.com
RUN apk add gcc musl-dev linux-headers
RUN pip3 install akshare jupyter notebook pandas -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 80

WORKDIR /opt
CMD ["jupyter","notebook","--ip","0.0.0.0","--port","80","--allow-root"]
```

```bash
docker build . -t ak
docker run -d --name ak -v `pwd`:/opt -p 80:80  ak
```

```python
'''
1. 获取交易时间，排除非交易时间
2. 告警:
     每隔五分钟向dingtalk 发送一次
     涨跌超5%告警
     涨跌速超2%告警
'''


import akshare as ak
import pandas as pd


# 获取A股实时数据
data = ak.stock_zh_a_spot_em()

# 将数据转换为DataFrame
df = pd.DataFrame(data)

 
# 假设我们想要获取多个股票的实时数据，例如股票代码列表


stock_codes={"000001",
             "000009",
             "000547",
             "000792",
             "000821",
             "000938",
             "001333",
             "002085",
             "002340",
             "002607",
             "002642",
             "002803",
             "300498",
             "301091",
             "600089",
             "600062",
             "603191",
             "603650",
             "603982",
             "605366",
             "835985",
             "603315",
             "300085",
             "600536",
             "300397",
             "002122",
             "600876",
             "836826"
            }
# 筛选指定股票的实时数据
stock_data = df[df[f"代码"].isin(stock_codes)]
# # 选择我们想要展示的列
columns_to_display = ["代码", "名称", "最低","最新价","最高", "涨跌幅","涨速","5分钟涨跌","换手率","成交量","量比","年初至今涨跌幅"]

stock_data_display = stock_data[columns_to_display]
#print(stock_data_display)

# # 按照涨跌幅倒序排列
stock_data_sorted = stock_data_display.sort_values(by="5分钟涨跌", ascending=False)

# # # 打印结果
print("近期成交信条超过5%涨幅的考虑卖出，不追高！！！")
print(stock_data_sorted)
```







### prometheus指标



```dockerfile
FROM python:3.11.12-alpine3.21

LABEL maintainer=1209233066@qq.com
RUN apk add gcc musl-dev linux-headers
RUN pip3 install akshare pandas prometheus_client apscheduler -i https://mirrors.aliyun.com/pypi/simple/

ADD ./stock_metrics.py /opt/stock_metrics.py

EXPOSE 6500

CMD [" python3","/opt/stock_metrics.py"]
```





```python
#!/usr/bin/python3

"""
成交量占比{code="000001",name="平安银行"}
换手率{code="000001",name="平安银行"}
涨跌幅{code="000001",name="平安银行"}
年初至今涨跌幅{code="000001",name="平安银行"}
"""

from prometheus_client import start_http_server, Gauge
from apscheduler.schedulers.blocking import BlockingScheduler

import akshare as ak
import pandas as pd


# 暴露prometheus指标 http://xxxx:6500
start_http_server(6500)

g1=Gauge("stock_amount_rate","量比%",["code","name"])
g2=Gauge("stock_turnover_rate","换手率",["code","name"])
g3=Gauge("stock_price_change","涨跌幅",["code","name"])
g4=Gauge("stock_year_to_date_changed_rate","年初至今涨跌幅",["code","name"])

def get_data():
    # 获取A股实时数据
    data = ak.stock_zh_a_spot_em()

    # 将数据转换为DataFrame
    df = pd.DataFrame(data)


    # 假设我们想要获取多个股票的实时数据，例如股票代码列表


    stock_codes={"000001",
                 "000009",
                 "000547",
                 "000792",
                 "000821",
                 "000938",
                 "001333",
                 "002085",
                 "002340",
                 "002607",
                 "002642",
                 "002803",
                 "300498",
                 "301091",
                 "600089",
                 "600062",
                 "603191",
                 "603650",
                 "603982",
                 "605366",
                 "835985",
                 "688726",
                 "300085",
                 "600536",
                 "300397",
                 "002122",
                 "600876",
                 "836826",
                 "688366",
                 "600779","300024"
                }
    # 筛选指定股票的实时数据
    stock_data = df[df[f"代码"].isin(stock_codes)]
    # # 选择我们想要展示的列
    columns_to_display = ["代码", "名称", "最低","最新价","最高", "涨跌幅","涨速","5分钟涨跌","换手率","成交额","流通市值","量比","年初至今涨跌幅","量比"]

    stock_data_display = stock_data[columns_to_display]
    #print(stock_data_display)

    # # 按照涨跌幅倒序排列
    stock_data_sorted = stock_data_display.sort_values(by="5分钟涨跌", ascending=False)




    stock_data_list=stock_data_sorted.values.tolist()

    for item in stock_data_list:
        g1.labels(item[0],item[1]).set(item[13])
        g2.labels(item[0],item[1]).set(item[8])
        g3.labels(item[0],item[1]).set(item[5])
        g4.labels(item[0],item[1]).set(item[12])
        
    print("exec successfull!")

    
    
    
###############################################main
# 初次启动执行一次
get_data()
# 实例化定时任务        
scheduler = BlockingScheduler(timezone='Asia/Shanghai')

# 添加每日
# 1) 09:00-12:00
scheduler.add_job(
    get_data,
    'cron',
    day_of_week='mon-fri',
    hour='9-12',
    minute='8',
    second=0
)

# 2) 13:00-15:00
scheduler.add_job(
    get_data,
    'cron',
    day_of_week='mon-fri',
    hour='13-15',
    minute='8',
    second=0
)


print("定时任务已启动，将在每日下午3:05执行...")
print("按 Ctrl+C 退出")

try:
    # 启动调度器
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("\n定时任务已停止")
```

```bash
docker run -d -p6500:6500 stock_metrics
```







### 华润双鹤 19.49 留100股，60月均线16.5附近加仓。连续多天出现量价背离

### 拉普拉斯 51.5 清仓





### 盐湖24附近减仓



### 格林美 利好消息 ，开盘预计在3%成交量



中芯国际 81.6 清仓

温氏股份 19.4 清仓

机器人 21 清仓

拉普拉斯 借利好清仓 51.5

中国宝安 12.68 减仓2000

中国软件  52.8984 清仓

美芯晟  53.190清仓

领益智造 16.716 清仓

银之杰清仓

融创、航天、天和 回本清仓
