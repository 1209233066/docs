---
date: '2025-05-25T14:40:56+08:00'
draft: false
title: 'Echart'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  echart 是一个基于 JavaScript 的开源可视化库，用于创建各种类型的图表，如折线图、柱状图、饼图等。它提供了丰富的配置选项和交互功能，使得开发者可以轻松地将数据以直观的方式呈现给用户。
tags: ["echart"]
categories: ["echart"]
url: 2025-05-25/echart.html
author: "wangendao"
---

![](https://rpic.origz.com/api.php?category=photography)

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>ECharts</title>
    <!-- 引入刚刚下载的 ECharts 文件 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.2/echarts.min.js"></script>
  </head>
  <body>
    <!-- 为 ECharts 准备一个定义了宽高的 DOM -->
    <div id="main" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('main'));

      // 指定图表的配置项和数据
      var option = {
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      };

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    </script>
  </body>
</html>
```