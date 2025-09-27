---
date: '2025-05-21T16:08:09+08:00'
draft: false
title: 'Quitstart'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  quitstart|ansible
tags: ["ansible"]
categories: ["ansible"]
url: ansible/quitstart.html
author: "wangendao"
---



![](https://rpic.origz.com/api.php?category=photography)

*Ansible 是一个 IT 自动化工具,每年大约发布三到四次新的 Ansible 主要版本。*

文档使用版本2.9

### 概念

+ 控制节点： 安装了ansible 的主机，window主机不能作为控制节点
+ 被管理节点：受控制节点管理的主机
+ inventory :  被管理节点的主机清单
+ 模块：ansible 调用的python包
+ tasks: 要ansible执行的任务
+ playbook: 通过编排后的task集合，可以完成复杂任务

### 工作原理

+ 选择被管理节点
+ 通过ssh连接到节点
+ 将一个或多个模块复制到被管理节点执行





### 快速开始

```bash
yum install ansible-2.9.27-1.el7.noarch
# 2.9 开始支持补全功能
yum install epel-release
yum install python-argcomplete
ansible 127.0.0.1 -m ping
```



主配置文件: `/etc/ansible/ansible.cfg`

定义资产配置清单: `/etc/ansible/hosts`

{{< tabpane text=true right=false >}}
  {{% tab header="**资产配置清单**:" disabled=true /%}}
  {{% tab header="ini格式" lang="ini" %}}

```ini
# /etc/ansible/hosts
[master]
10.4.7.9
10.4.7.1[0:1]
[node]
node[1:15]
[all:vars]
ansible_ssh_user: root
```

  {{% /tab %}}
  {{% tab header="yaml格式" lang="yaml" %}}

```yaml
# /etc/ansible/hosts
all:
  children:
    master:
      hosts: "10.4.7.9,10.4.7.1[0:1]"  # 展开为 10.4.7.9, 10.4.7.10, 10.4.7.11
    node:
      hosts: "node[1:15]"              # 展开为 node1, node2, ..., node15
  vars:
    ansible_ssh_user: root             # 全局 SSH 用户设置为 root
```

  {{% /tab %}}
{{< /tabpane >}}



查询配置清单中的主机

```bash
ansible all --list-hosts
```

### 模块

##### ping  模块

```bash
ansible all -m ping
```

##### debug

```bash
ansible 127.0.0.1 -m debug -a "msg=hello world"
```



##### hostname

```bash
# 修改主机名
ansible 127.0.0.1 -m hostname -a "name=ansible-master"
```

##### fetch

```bash
# ansible-doc -s fetch 从远端拉取文件
ansible 127.0.0.1 -m fetch -a "src=/etc/hosts dest=/tmp"
```

##### file

```bash
# ansible-doc -s file  创建/删除 文件/目录/软连接
ansible 127.0.0.1 -m file -a "path=/tmp/a.log state=touch"

ansible 127.0.0.1 -m file -a "path=/tmp/a.log state=absent"

ansible 127.0.0.1 -m file -a "path=/tmp/a/b state=directory recurse=yes"

ansible 127.0.0.1 -m file -a "path=/tmp/a state=absent"

ansible 127.0.0.1 -m file -a "path=/tmp/a state=link src=/etc/hosts"
```

##### blockinfile

```bash
# ansible-doc -s blockinfile  按照标记添加/删除文件内容
# 插入内容
ansible 127.0.0.1 -m blockinfile -a "path=/tmp/a marker=#{mark}20220318 block='101.43.43.9  test.com'"

# 删除标记位置内容
ansible 127.0.0.1 -m blockinfile -a "path=/tmp/a marker=#{mark}20220318 state=absent"

# 在开头插入 BOF（begin of file）
ansible 127.0.0.1 -m blockinfile -a "path=/tmp/a marker=#{mark}20220318 block='10.43.43.9 test.com' insertbefore=BOF"

# 在结尾插入 EOF (end of file)
ansible 127.0.0.1 -m blockinfile -a "path=/tmp/a marker=#{mark}20220318 block='10.43.43.9 test.com' insertbefore=EOF"

# 在insertafter='^127.0.0.1' 之后插入
ansible 127.0.0.1 -m blockinfile -a "path=/tmp/a marker=#{mark}20220318 block='10.43.43.9 test.com' insertafter='^127.0.0.1'"
```

##### lineinfile

```bash
# sed -i 's/^10/#############/g' /tmp/a
# backrefs=yes 支持正则分组引用 ，当正则不匹配时不执行动作

ansible 127.0.0.1 -m lineinfile -a "path=/tmp/a regexp='^10' line='#############' backrefs=yes"
```



```bash
# sed -i 's/^#(.*)/\1g' /tmp/a
ansible 127.0.0.1 -m lineinfile -a "path=/tmp/a regexp='^#(.*)' line='\1' backrefs=yes
```

```bash
# sed - '/#############/d' /tmp/a
ansible 127.0.0.1 -m lineinfile -a "path=/tmp/a line='#############' state=absent"
```

```bash
# sed - '/^.*20220318$/d' /tmp/a
ansibel 127.0.0.1 -m lineinfile -a "path=/tmp/a regexp='^.*20220318$' state=absent"
```





##### find

```bash
# ansible-doc -s find
ansible 127.0.0.1 -m find -a "paths='/root' patterns='zookeeper.out' recurse=yes"
```



##### replace

```bash
# sed -i 's/^[a-Z]/##/g' /tmp/a
ansible 127.0.0.1 -m replace -a "path=/tmp/a regexp='^[a-Z]' replace='##'"
```



##### command

```bash
ansible 127.0.0.1 -m  command -a "chdir='/' ls -a"
```



##### shell

```bash
# 支持管道，command 不支持
ansible 127.0.0.1 -m  shell -a "chdir='/' ls -a|wc"
```



**script**

```bash
# /tmp/1.sh 在运维主机
ansible 127.0.0.1 -m  script -a "chdir='/' /tmp/1.sh"
```



##### cron

```bash
# 添加定时任务
# */5 * * * * usr/sbin/ntpdate ntpdate ntp.aliyun.com >/dev/null 2>&1

ansible 127.0.0.1 -m cron -a "minute=*/5 hour=* name='ntp date' job='/usr/sbin/ntpdate ntpdate ntp.aliyun.com >/dev/null 2>&1'"
```



```bash
# 启用注释的定时任务
ansible 127.0.0.1 -m cron -a "disabled=false name='ntp date' job='/usr/sbin/ntpdate ntpdate ntp.aliyun.com >/dev/null 2>&1'"
```



```bash
# 删除定时任务
ansible 127.0.0.1 -m cron -a "state=absent name='ntp date' backup=yes"
```



##### yum

```bash
# 安装
ansible 127.0.0.1 -m yum -a "name=rsync,vim,lrzsz state=present"
```

```bash
# 卸载
ansible 127.0.0.1 -m yum -a "name=rsync,vim,lrzsz state=absent"
```



##### systemd

```bash
ansible all -m systemd -a "name=network state=restarted enabled=yes"
```



##### group

```bash
# groupadd mysql
ansible all -m group -a "name=mysql state=present"
```



```bash
# groupadd mysql
ansible all -m group -a "name=db state=present"
```



##### user

```bash
# useradd -g mysql -G root,db  -M -s /bin/nologin mysql

ansible all -m user -a "name=mysql group=mysql groups=db,root create_home=no shell=/bin/nologin state=present"
```



##### template

```yaml
- hosts:
  - all
  tasks:
  - name: template
    template:	# 与copy类似，支持变量解析
      src: /tmp/nginx.conf.j2
      dest: /tmp/nginx.conf
```

### 剧本playbook

```bash
# 检查语法
ansible-playbook --syntax-check /etc/ansible/play.yml
```

```bash
# dry-run
ansible-playbook --check /etc/ansible/play.yml
```

```bash
# 执行剧本
ansible-playbook /etc/ansible/play.yml
ansible-playbook /etc/ansible/play.yml --list-hosts
ansible-playbook /etc/ansible/play.yml --list-tasks
ansible-playbook /etc/ansible/play.yml --limit 10.4.7.21
```



##### 基本语法tasks

```yaml
# /etc/ansible/play.yml
- hosts: all
  tasks:
  - name: ping host
    ping:
- hosts: 
  - 10.4.7.11
  - 10.4.7.12
  tasks:
  - name: fetch file
    fetch:
      src: /etc/services
      dest: /tmp
  - name: copy file
    copy:
      src: /etc/services
      dest: /tmp
```

##### 基本语法handlers

```yaml
# 通过notify 调用handlers
- hosts:
  - all
  tasks:
  - name: touch file
    file:
      path: /tmp/file.prom
      state: touch
    notify:
       wirte file

  handlers:
  - name: wirte file
    blockinfile:
      path: /tmp/file.prom
      block: 'this is first line'
  - name: remove file
    file:
      path: /tmp/file.prom
      state: absent
```



##### 基本语法meta

```yaml
- hosts:
  - all
  tasks:
  - name: touch file
    file:
      path: /tmp/file.prom
      state: touch
    notify:
       wirte file
  # python 按顺序执行，如果添加了meta: flush_handlers 对应的task完成后会直接触发handlers
  - meta: flush_handlers

  - name: ping
    ping:


  handlers:
  - name: wirte file
    blockinfile:
      path: /tmp/file.prom
      block: 'this is first line'
  - name: remove file
    file:
      path: /tmp/file.prom
      state: absent
```

##### 基本语法listen

```yaml
- hosts:
  - all
  tasks:
  - name: touch file
    file:
      path: /tmp/file.prom
      state: touch
    notify:
       group1

  handlers:
  - name: wirte file
    listen: group1
    blockinfile:
      path: /tmp/file.prom
      block: 'this is first line'
  - name: modify file
    listen: group1
    lineinfile:
       path: /tmp/file.prom
       regexp: '(.*)first(.*)'
       line: \1\2
       backrefs: true
```

##### 基本语法tags

```yaml
- hosts:
  - all
  tasks:
  - name: touch file
    file:
      path: /tmp/file.prom
      state: touch
    notify:
       group1
  - name: ping
    ping:
    tags: tag_ping
  handlers:
  - name: wirte file
    listen: group1
    blockinfile:
      path: /tmp/file.prom
      block: 'this is first line'
  - name: modify file
    listen: group1
    lineinfile:
       path: /tmp/file.prom
       regexp: '(.*)first(.*)'
       line: \1\2
       backrefs: true
```

```bash
# 查看有哪些tag
ansible-playbook --list-tags /etc/ansible/play.yml
 
 ansible-playbook --tags=tag_ping /etc/ansible/play.yml
ansible-playbook --skip-tags=tag_ping /etc/ansible/play.yml
# 所有任务都不会被执行
ansible-playbook --skip-tags all /etc/ansible/play.yml
#
ansible-playbook --tags tagged /etc/ansible/play.yml
#
ansible-playbook --tags untagged /etc/ansible/play.yml
# always 默认执行，除非明确指定--skip-tags
ansible-playbook --skip-tags always /etc/ansible/play.yml
# never 在不明确指定的情况下默认不执行
ansible-playbook --tags never /etc/ansible/play.yml
```

##### **循环**

```yaml
- hosts:
  - all
  tasks:
  - name: debug
    debug:
      msg: "{{ item }}"
    with_items:
    - first line
    - second line
```

```yaml
# 带索引的列表
- hosts:
  - all
  tasks:
  - name: debug
    debug:
      msg: "{{item.1}}"
    with_indexed_items:
    - first line
    - second line
```

````yaml
# range(1,10,3)
- hosts:
  - all
  tasks:
  - name: debug
    debug:
      msg: "{{ item }}"
    with_sequence:
      start=1
      end=10
      stride=3
````



```yaml
- hosts:
  - all
  tasks:
  - name: debug
    debug:
      msg: "{{ item.name }}{{ item.age }}"
    with_items:
    - {name: wangendao,age: 31}
    - {name: zhangsan,age: 18}
```





##### **判断**

+ **when**

```jinja2
- hosts:
  - all
  tasks:
  - debug:
    msg: "{{ansible_hostname}}"
    when:
    # 可以使系统变量或自定义变量
      ansible_hostname == "hdss7-200"
```



##### 变量

**一、系统变量：**

```bash
# cpu  核心数
ansible_processor_vcpus
```

```bash
# 主机名
ansible_hostname
```

```bash
# ip
ansible_host
```

```bash
# 内存
ansible_memtotal_mb
```

```bash
# ansible的版本信息
ansible_version
```

```bash
# ansible-play 1.yml --list-host
play_hosts
```

```bash
#
groups
```

```bash
# 系统发行版
ansible_distribution
```

```bash
# 系统版本号
ansible_distribution_major_version 
```

二、用户自定义变量

在资产清单中定义

```yaml
# /etc/ansible/hosts
all:
  hosts:
    10.4.7.11:
      name: wangendao
    10.4.7.12:
    10.4.7.200:
  vars:
    ansible_ssh_user: root 
    ansible_ssh_pass: 123
  children:
    k8s_node:
      hosts:
        10.4.7.21:
        10.4.7.22:
      vars:
        ansible_ssh_user: root 
        ansible_ssh_pass: 123
```


+ 主机变量

  ```ini
  [atlanta]
  host1 http_port=80 maxRequestsPerChild=808
  host2 http_port=303 maxRequestsPerChild=909
  ```

  ```yaml
  all:
    children:
      atlanta:
        host1:
          http_port: 80
          maxRequestsPerChild: 808
        host2:
          http_port: 303
          maxRequestsPerChild: 909
  ```

  ```ini
  [targets]
  # 指定连接方式
  localhost              ansible_connection=local
  other1.example.com     ansible_connection=ssh        ansible_user=myuser
  other2.example.com     ansible_connection=ssh        ansible_user=myotheruser
  ```

  此外还可以在`/etc/ansible/host_vars/主机名` 举例：

  ```bash
  tee /etc/ansible/host_vars/localhost <<EOF
  username=admin
  passwd=123
  ```

  

+ 组变量

  ```ini
  [atlanta]
  host1
  host2
  
  [atlanta:vars]
  ntp_server=ntp.atlanta.example.com
  proxy=proxy.atlanta.example.com
  ```

  ```yaml
  all:
    children:
      atlanta:
        hosts:
          host1:
          host2:
        vars:
          ntp_server: ntp.atlanta.example.com
          proxy: proxy.atlanta.example.com
  ```

  ```ini
  [atlanta]
  host1
  host2
  
  [raleigh]
  host2
  host3
  
  [southeast:children]
  atlanta
  raleigh
  
  [southeast:vars]
  some_server=foo.southeast.example.com
  halon_system_timeout=30
  self_destruct_countdown=60
  escape_pods=2
  
  [usa:children]
  southeast
  northeast
  southwest
  northwest
  ```

  ```yaml
  all:
    children:
      usa:
        children:
          southeast:
            children:
              atlanta:
                hosts:
                  host1:
                  host2:
              raleigh:
                hosts:
                  host2:
                  host3:
            vars:
              some_server: foo.southeast.example.com
              halon_system_timeout: 30
              self_destruct_countdown: 60
              escape_pods: 2
          northeast:
          northwest:
          southwest:
  ```

  此外还可以在`/etc/ansible/group_vars/分组名称/...` 举例：

  ini格式

  ```ini
  tee /etc/ansible/group_vars/db <<EOF
  username=root
  passwd=123
  EOF
  ```

  yaml格式

  ```yaml
  tee /etc/ansible/group_vars/db <<EOF
  username: root
  passwd: 123
  EOF
  ```

  

+ 指定别名

  ```ini
  jumper ansible_port=5555 ansible_host=192.0.2.50
  ```

  

  ```yaml
  all:
    hosts:
      jumper:
        ansible_port: 5555
        ansible_host: 192.0.2.50
  ```

playbook中定义

书写方式一：

```yaml
- hosts:
  - 127.0.0.1
  vars:
  - info: {'name': wangendao,'age':31}
  - filename: f1
  tasks:
  - name: touch file
    file:
      path: /tmp/{{filename}}
      state: touch
    tags: touch file

  - name: debug
    debug:
      msg: "name: {{ info.name }} age: {{ info.age }}"
```



书写方式二：

```yaml
# vars.yml
name: wangendao
age: 31
```

```yaml
- hosts:
  - all
  vars_files:
  - vars.yml
  tasks:
  - name: debug
    debug:
      msg: "{{ name }}{{age}}"
```



书写方式三：

```yaml
# 接收键盘输入
- hosts:
  - 127.0.0.1
  vars_prompt:
  - name: "name"
    prompt: "please input your name: "
     # 显示输入的信息，默认隐藏
    private: no
  - name: "age"
    prompt: "please input your age: "
    # 显示输入的信息，默认隐藏
    private: no
  tasks:
  - name: debug
    debug:
      msg: "{{ name }} {{ age }}"
```

书写方式四：

```yaml
- hosts:
  - 127.0.0.1
  tasks:
  - name: debug
    debug:
      msg: "{{ name }}"
```



```bash
-e ,--extra-vars

ansible-playbook  /etc/ansible/play_vars.yml  --extra-vars "name=wangendao"
ansible-playbook  /etc/ansible/play_vars.yml  -e "name=wangendao"
```



**变量注册**

```yaml
- hosts:
  - 127.0.0.1
  vars:
  - info: {'name': wangendao,'age':31}
  - filename: f1
  tasks:
  - name: touch file
    file:
      path: /tmp/{{filename}}
      state: touch
    # 把 touch file 的执行结果保存到变量AAA 中
    register: AAAA
    tags: touch file

  - name: debug
    debug:
      msg: "name: {{ info.name }} age: {{ info.age }} {{ AAAA }}"
```



### roles

下载roles的方法

1. ansible-galaxy install 

   + roles

   ```bash
   roles
     |- nginx
   	|- tasks
   		|- 定义任务列表
       |- handler
       	|- main.yml	定义handlers
       |- vars
       	|- main.yml	定义变量
       |- templates
       |- files
       |- meta
       	|- main.yml 作者、版本信息
       |- defaults
       	|- main.yml 定义变量的初始值
   ```

   

   ```bash
   # 在/tmp 下创建一个标准的roles目录结构
   ansible-galaxy init /tmp/nginx
   ```

   

   从互联网 现在roles

   ```bash
   # 查找仓库中的role
   ansible-galaxy search "k8s"
   # 查看仓库中role信息
   ansible-galaxy info 24_komal.ec2_k8s_master
   # 下载到/tmp/roles下
   ansible-galaxy install 24_komal.ec2_k8s_master -p /tmp/roles
   ```

   

2. 通过requirements.yml 文件下载

   requiremets.yml的格式如下:

   ```yaml
   # 从galaxy 官网下载http://galaxy.ansible.com/
   - src:
   # 从git下载
   - src: http://github.com/xxx/xxx.git
     scm: git
     version: 56200a54
     name: nginx-acme
   # 把roles 打包成tar.gz 上传到自检的http服务器后，要想从这个http服务器下载
   - src: http://127.0.0.1/my.tar.gz
     name: my
   ```

### 二进制命令
<span id=command>**二进制命令**</span >

| 名称             | 功能                | 举例                                     |
| ---------------- | ------------------- | ---------------------------------------- |
| ansible          | 用于临时执行命令    | `ansible all -m ping`                    |
| ansible-console  | 交互式命令          |                                          |
| ansible-vault    | 由于文件加密和解密  |                                          |
| ansible-galaxy   | 用于和roles仓库交互 | `ansible-galaxy  init`                   |
| ansible-playbook | 用于运行playbook    |                                          |
| ansible-doc      | 查询帮助            | `ansible-doc -l`<br/>ansible-doc -s ping |



```bash
# 加密 yml
bash-4.4# ansible-vault encrypt /etc/ansible/play1.yml
# 查看加密的 yml
bash-4.4# ansible-vault view /etc/ansible/play1.yml
# 编辑加密的 yml
bash-4.4# ansible-vault edit /etc/ansible/play1.yml
# 修改加密的密码
bash-4.4# ansible-vault rekey /etc/ansible/play1.yml
# 解密 yml
bash-4.4# ansible-vault decrypt /etc/ansible/play1.yml
```

### 参考
[*官方文档*](https://docs.ansible.com/ansible/latest/index.html)

[Ansible中文权威指南- 国内最专业的Ansible中文官方学习手册](http://www.ansible.com.cn/)

[Ansible Galaxy](https://galaxy.ansible.com/nn708/openwrt)

https://www.cnblogs.com/michael-xiang/p/10462749.html)

[欢迎来到 Jinja2 — Jinja2 2.7 documentation (jinkan.org)](http://docs.jinkan.org/docs/jinja2/)

[yaml官网](