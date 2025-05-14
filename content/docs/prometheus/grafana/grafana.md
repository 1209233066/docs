---
title: "quitstart"
linkTitle: "quitstart"
date: 2025-05-14
toc_hide: false
hide_summary: true
weight: 52
description: >
  quitstart|grafana|prometheus

tags: ["prometheus","grafana"]
categories: ["prometheus","grafana"]
url: prometheus/grafana/quitstart.html
---

### 部署安装

> 测试版本7.5.17 、9.5.21、 10.4.14

+ **docker方式安装grafanna**

  ```bash
  docker pull grafana/grafana:7.5.17
  docker pull grafana/grafana:9.5.21
  docker pull grafana/grafana:10.4.14
  
  docker pull grafana/grafana-enterprise:7.5.17
  docker pull grafana/grafana-enterprise:9.5.21
  docker pull grafana/grafana-enterprise:10.4.14
  ```

  ```bash
  docker run -d -p 3000:3000 --name=grafana \
  --volume /data/grafana:/var/lib/grafana \
  grafana/grafana-enterprise:10.4.14
  ```

+ **rpm 包安装grafana**

  ```bash
  yum install -y https://dl.grafana.com/enterprise/release/grafana-enterprise-10.4.14-1.x86_64.rpm
  systemctl enable grafana-server.service --now
  ```

### 配置优化

> /etc/grafana/grafana.ini

- [x] 修改默认语言

  ```ini
  [users]
  # 默认语言改为简体中文
  default_language = zh-Hans
  ```

- [x] 修改配置支持nginx代理

  ```ini
  [server]
  # 支持（http, https, h2, socket)
  protocol = http
  # 绑定的服务ip,默认所有
  http_addr =
  # 绑定的服务port
  http_port = 3000
  # 服务绑定的域名
  domain = localhost
  # 当访问时与指定的域名不一致时，拒绝访问。默认关闭
  enforce_domain = false
  # 定义服务的url
  root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana
  # 从root_url 的配置路径中加载
  serve_from_sub_path = true
  # 开启gzip 用于节省带宽
  enable_gzip = false
  ```

  ```nginx
  server {
          listen       80;
          root         /usr/share/nginx/html;
          location /grafana {
                  proxy_set_header Host $host;
                  proxy_set_header X-Forwarded-For $remote_addr;
                  proxy_pass http://172.16.0.3:3000;
          }
  ```

  

  <table>
      <tr>
          <td>如图所示，是由于grafana跨域请求问题。可以在nginx代理中正确配置<td>
          <td><image src="/docs/prometheus/grafana/img/grafana.png"><td>
      </tr>
  </table>

  

- [x] 修改报表支持嵌入

  ```ini
  [security]
  # 允许将grafana报表嵌入到 <frame>, <iframe>, <embed> or <object> 等html中，默认不允许
  allow_embedding = true
  ```

  ```ini
  [auth.anonymous]
  # 开启匿名访问,默认禁用
  enabled = true
  # 匿名访问用户所属组织
  org_name = Main Org.
  # 匿名用户拥有的角色
  org_role = Viewer
  # 对于为匿名用户隐藏版本号
  hide_version = false
  ```

  语法：

  ```html
  <html>
      <!-- 单个图表嵌入语句-->
      <iframe src="http://10.4.7.10:3000/d/a666a82f-47a1-4467-8e3f-c5d142f33927/new-dashboard?orgId=1&viewPanel=1" width="450" height="200" frameborder="0"></iframe>
      
      <!-- 整个Dashboard嵌入语句-->
      <iframe src="http://10.4.7.10:3000/d/a666a82f-47a1-4467-8e3f-c5d142f33927/new-dashboard?orgId=1" width="100%" height="100%" frameboader="0"></iframe>
  </html>
  ```

- [x] 配置安装启动时拥有的数据源

  

  ```ini
  # 配置文件开启该配置
  [paths]
  # 开启该配置
  provisioning = conf/provisioning
  ```

  ```yaml
  # vi /usr/share/grafana/conf/provisioning/datasources/prometheus.yml
  apiVersion: 1
  datasources:
    # 第一个数据源
    - name: prometheus01
      type: prometheus
      access: proxy
      url: http://localhost:9090/prom
      editable: true
      isDefault: true
    # 第二个数据源 
    - name: prometheus02
      type: prometheus
      access: proxy
      url: http://127.0.0.1:9090/prom
      editable: true
  ```

  ```bash
  systemctl restart grafana-server.service 
  ```

  

- [x] 配置安装启动时拥有的报表

  ```ini
  # 配置文件开启该配置
  [paths]
  # 开启该配置
  provisioning = conf/provisioning
  ```

  

  ```yaml
  #  /usr/share/grafana/conf/provisioning/dashboards/node-exporter.yaml
  apiVersion: 1
  
  providers:
   - name: 'node-exporter'
     orgId: 1
     folder: 'k8s'
     folderUid: ''
     type: file
     options:
       path: /var/lib/grafana/dashboards
  ```

  ```bash
  mkdir /var/lib/grafana/dashboards
  # vi /var/lib/grafana/dashboards/node-exporter.json 文件格式为导出的报表格式
  ```

  ```bash
  systemctl restart grafana-server.service 
  ```

  

- [x] 设置默认首页

  > 登录http://prometheus.pytc.com:3000/grafana 时自动跳转到设定的页面

  ```ini
  [users]
  # 设置首页
  # http://prometheus.pytc.com:3000/grafana/d/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m
  home_page = /d/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m
  ```

  

- [ ] 安装必要插件




### 配置文件

> 可以通过修改配置文件或 环境变量的方式修改默认配置

```ini
# 运行在生产模式
app_mode = production
# 实例名
instance_name = ${HOSTNAME}
[paths]
# 定义存放临时文件、session、sqllit
data = /var/lib/grafana
# 临时文件存放24h后删除
temp_data_lifetime = 24h
# 日志文件
logs = /var/log/grafana
# 插件文件
plugins = /var/lib/grafana/plugins
#  /usr/share/grafana/conf/provisioning 定义启动时加载配置，例如数据源、报表等
provisioning = conf/provisioning


[server]
# 支持（http, https, h2, socket)
protocol = http
# 绑定的服务ip,默认所有
http_addr =
# 绑定的服务port
http_port = 3000
# 服务绑定的域名
domain = localhost
# 当访问时与指定的域名不一致时，拒绝访问。默认关闭
enforce_domain = false
# 定义服务的url
root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana
# 从root_url 的配置路径中加载
serve_from_sub_path = true
# 开启gzip 用于节省带宽
enable_gzip = false

[database]
# Either "mysql", "postgres" or "sqlite3", it's your choice
type = sqlite3
# 数据库名
name = grafana
# 数据文件名称
path = grafana.db


[security]
# 第一次启动时不创建用户
disable_initial_admin_creation = false
# 默认管理员用户
admin_user = admin
# 默认密码
admin_password = admin
# 默认邮件
admin_email = admin@localhost
# 签名秘钥，例如： 对密码 admin 字符串执行加盐后保存和验证，防止通过数据库看到原始密码
secret_key = SW2YcwTIb9zpOOhoPsMm
# 加密算法
encryption_provider = secretKey.v1

# 允许将grafana报表嵌入到 <frame>, <iframe>, <embed> or <object> 等html中，默认不允许
allow_embedding = true

[users]
allow_sign_up = true
# 允许普通用户创建organizations
allow_org_create = true
# 自动为新用户分配一个组织
auto_assign_org = true
# 自动为新用户分配一个组织，该组织id为1，需要开启 auto_assign_org = true
auto_assign_org_id = 1
# 自动为新用户分配一个角色
auto_assign_org_role = Viewer
# 不要求有邮箱认证
verify_email_enabled = false
# 默认主题为深色
default_theme = dark
# 默认语言改为简体中文
default_language = zh-Hans
# 设置首页
home_page =
# 不允许 viewers 角色执行编辑动作
viewers_can_edit = false
# 不允许 editors 角色执行管理动作
editors_can_admin = false

[auth.anonymous]
# 开启匿名访问,默认禁用
enabled = true
# 匿名访问用户所属组织
org_name = Main Org.
# 匿名用户拥有的角色
org_role = Viewer
# 对于为匿名用户隐藏版本号
hide_version = false
```







### 插件

+ **agenty-flowcharting-panel** Flowcharting is a Grafana plugin. Use it to display complexe diagrams using the online graphing library draw.io like a vsio

  + **安装插件**
  
    ```bash
    grafana-cli plugins install agenty-flowcharting-panel
    ```
  
    ```
    [root@lavm-ioreaqndwv ~]# grafana-cli plugins ls
    installed plugins:
    agenty-flowcharting-panel @ 0.9.1
    ```
  
    ```bash
    systemctl restart grafana-server.service
    ```
  
  

### 实用需求

+ **dashbaord 定义动态变量**

  ```bash
  label_values(promethues表达式,需要取值的label名称)
  举例：
  label_values(up{job="node-exporter"},instance)
  ```

+ **标签转换**

  问题描述： 在标签中存在 `node01:9100` 的字样。而现在只需要保留 `node01`

  解决办法：Transform(转换) --> `Rename by regex`  

  

  

[Grafana OSS 和企业 |Grafana 文档](https://grafana.com/docs/grafana/latest/)

[Download ](https://grafana.com/grafana/download/9.0.0)

https://grafana.com/docs/grafana/latest/cli/#plugins-commands

[Restricting Access with HTTP Basic Authentication | NGINX Documentation](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)
