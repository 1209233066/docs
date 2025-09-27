
---
date: '2025-05-20T22:13:52+08:00'
draft: false
title: 'redmine'
type: blog
toc_hide: false
hide_summary: true
weight: 2
description: >
  redmine|gitlab
tags: ["redmine"]
categories: ["devops"]
url: devops/redmine.html
author: "wangendao"
---
![](https://rpic.origz.com/api.php?category=photography)
依赖
Ruby 2.7, 3.0, 3.1, 3.2
SQLite3 (tested with SQLite 3.11)
MySQL (tested with MySQL 8)

redmine 是一个项目管理工具，使用ruby开发，支持sqlit3/mysql/postgresql 作为后端存储库。

### 部署安装
操作系统： *CentOS Linux release 7.9.2009 (Core)*
软件版本： *5.1.3*
ruby版本： *2.7.2*

---



ruby 环境安装

> gem 是ruby的包管理工具，可以理解为python的pip
>
> 设置gem 国内仓库地址：

```bash
# 安装ruby环境
ruby_version='3.1.0'
major_minor=${ruby_version%.*}
install_ruby(){
	if [ ! -f ruby-${ruby_version}.tar.gz ];then
		curl -q -# https://cache.ruby-lang.org/pub/ruby/${major_minor}/ruby-${ruby_version}.tar.gz -O
		tar xf ruby-${ruby_version}.tar.gz
		cd ruby-${ruby_version}
		./configure --disable-install-rdoc &&  make -j 8  && make install 
		ruby -v
		gem -v
	else
		tar xf ruby-${ruby_version}.tar.gz
		cd ruby-${ruby_version}
		./configure --disable-install-rdoc &&  make -j 8  && make install 
		ruby -v
		gem -v
    fi
}

install_bundler(){
	# 更新镜像源
    gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/
    gem sources --remove https://rubygems.org/
    # Bundler是一个Ruby库，用于管理Ruby应用程序的依赖
    gem install bundler --no-document --version '< 2'
    # 设置bundler的国内镜像地址
    bundle config set mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems/
    # 查看设置是否成功
    bundle config get mirror.https://rubygems.org
}

yum install gdbm-devel readline-devel zlib-devel openssl-devel -y
install_ruby
install_bundler
```



```bash
install_redmine(){
	
   	curl -q -#  https://www.redmine.org/releases/redmine-5.1.3.tar.gz -O

    tar xf redmine-5.1.3.tar.gz 
    cd redmine-5.1.3/
    echo -e "production:\n  adapter: sqlite3\n  database: db/redmine.sqlite3\n" >config/database.yml
    # 安装依赖
    bundle install --without development test
    # 生成secret
    bundle exec rake generate_secret_token
    # 生成数据库表结构
    bundle exec rake db:migrate RAILS_ENV="production"
    #
    useradd redmine -s /usr/sbin/nologin 
    chown -R redmine:redmine files log tmp public/plugin_assets
    chmod -R 755 files log tmp public/plugin_assets
    ruby bin/rails server -e production
}
install_redmine
```





> 

```bash
#!/bin/bash


   # gem 是ruby 的包管理工具，该命令安装了一个包bundler
   bundle install --without development test
   bundle exec rake db:migrate RAILS_ENV="production"
   bundle exec rake generate_secret_token
   useradd redmine
   chown -R redmine:redmine files log tmp public/plugin_assets
   chmod -R 755 files log tmp public/plugin_assets
    ruby bin/rails server -e production
}

```

```bash

yum install ncurses ncurses-devel libaio cpanminus -y
useradd -s /sbin/nologin -M mysql
wget https://downloads.mysql.com/archives/get/p/23/file/mysql-8.0.36-linux-glibc2.12-x86_64.tar.xz
tar xf mysql-8.0.36-linux-glibc2.12-x86_64.tar.xz -C /opt/
ln -svf /opt/mysql-8.0.36-linux-glibc2.12-x86_64 /opt/mysql
chown -R mysql.mysql /opt/mysql*

[root@localhost ~]# /opt/mysql/bin/mysqld  --initialize --user=mysql --basedir=/opt/mysql/ --datadir=/opt/mysql/data/
2024-06-29T10:10:23.688320Z 0 [Warning] [MY-011070] [Server] 'Disabling symbolic links using --skip-symbolic-links (or equivalent) is the default. Consider not using this option as it' is deprecated and will be removed in a future release.
2024-06-29T10:10:23.688422Z 0 [System] [MY-013169] [Server] /opt/mysql/bin/mysqld (mysqld 8.0.36) initializing of server in progress as process 7931
2024-06-29T10:10:23.699452Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2024-06-29T10:10:24.026657Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2024-06-29T10:10:25.693738Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: GJk1t)H)0Cug


/opt/mysql/bin/mysqld_safe --defaults-file=/opt/mysql/my.cnf --datadir=/opt/mysql/data --pid-file=/opt/mysql/mysql.pid

/opt/mysql/bin/mysqld_safe  --datadir=/opt/mysql/data --pid-file=/opt/mysql/mysql.pid
/opt/mysql/bin/mysql -uroot -p'hj2paRhqJl'
```

```
yum install mysql-devel
bundle install --without development test
```

create database redmine  set utf8 collate utf8_general_ci;

2. Create an empty utf8 encoded database: "redmine" for example

3. Configure the database parameters in config/database.yml
   for the "production" environment (default database is MySQL)

4. Install the required gems by running:
     bundle install --without development test

   Only the gems that are needed by the adapters you've specified in your
   database configuration file are actually installed (eg. if your
   config/database.yml uses the 'mysql2' adapter, then only the mysql2 gem
   will be installed). Don't forget to re-run `bundle install` when you
   change config/database.yml for using other database adapters.

   If you need to load some gems that are not required by Redmine core
   (eg. fcgi), you can create a file named Gemfile.local at the root of
   your redmine directory.
   It will be loaded automatically when running `bundle install`.

5. Generate a session store secret

   Redmine stores session data in cookies by default, which requires
   a secret to be generated. Under the application main directory run:
     bundle exec rake generate_secret_token

   Alternatively, you can store this secret in config/secrets.yml:
   http://guides.rubyonrails.org/upgrading_ruby_on_rails.html#config-secrets-yml

6. Create the database structure

   Under the application main directory run:
     bundle exec rake db:migrate RAILS_ENV="production"

   It will create all the tables and an administrator account.

7. Setting up permissions (Windows users have to skip this section)

   The user who runs Redmine must have write permission on the following
   subdirectories: files, log, tmp & public/plugin_assets.

   Assuming you run Redmine with a user named "redmine":
     sudo chown -R redmine:redmine files log tmp public/plugin_assets
     sudo chmod -R 755 files log tmp public/plugin_assets

8. Test the installation by running the Puma web server

   Under the main application directory run:
     ruby bin/rails server -e production

   Once Puma has started, point your browser to http://localhost:3000/
   You should now see the application welcome page.

9. Use the default administrator account to log in:
   login: admin
   password: admin

   Go to "Administration" to load the default configuration data (roles,
   trackers, statuses, workflow) and to adjust the application settings

== Database server configuration

When using MySQL with Redmine 5.1.1 or later, it is necessary to change
the transaction isolation level from the default REPEATABLE READ to
READ_COMMITTED. To modify this setting, either change the database
configuration file or alter the settings on your MySQL server.

To set the transaction isolation level in the database configuration file,
add transaction_isolation variable as below:

  production:
    adapter: mysql2
    database: redmine
    host: localhost
    [...]
    variables:
      transaction_isolation: "READ-COMMITTED"

More details can be found in https://www.redmine.org/projects/redmine/wiki/MySQL_configuration.

== SMTP server Configuration

Copy config/configuration.yml.example to config/configuration.yml and
edit this file to adjust your SMTP settings.
Do not forget to restart the application after any change to this file.

Please do not enter your SMTP settings in environment.rb.

== References

* http://www.redmine.org/wiki/redmine/RedmineInstall
* http://www.redmine.org/wiki/redmine/EmailConfiguration
* http://www.redmine.org/wiki/redmine/RedmineSettings
* http://www.redmine.org/wiki/redmine/RedmineRepositories
* http://www.redmine.org/wiki/redmine/RedmineReceivingEmails
* http://www.redmine.org/wiki/redmine/RedmineReminderEmails
* http://www.redmine.org/wiki/redmine/RedmineLDAP