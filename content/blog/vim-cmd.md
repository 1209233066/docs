---
date: '2025-07-09T08:34:29+08:00'
draft: false
title: 'exsi命令行工具'
type: blog
toc_hide: false
hide_summary: true
weight: 6
description: >
  通过命令行工具vim-cmd 对虚拟机启动、停止、克隆、销毁
tags: ["vim-cmd"]
categories: ["exis"]
url: 2025-07-09/vim-cmd.html
author: "wangendao"
---

| 功能           | 命令                                                         |
| -------------- | ------------------------------------------------------------ |
| 列出虚拟机     | `vim-cmd vmsvc/getallvms`                                    |
| 强制关闭虚拟机 | `vim-cmd vmsvc/power.off <Vmid> `                            |
| 正常关闭       | `vim-cmd vmsvc/power.shutdown <Vmid> `                       |
| 重启           | `vim-cmd vmsvc/power.reset <Vmid>`                           |
| 启动           | `vim-cmd vmsvc/power.on<Vmid> `                              |
| 查看电源状态   | `vim-cmd vmsvc/power.getstate <Vmid>`                        |
| 获取完整配置   | `vim-cmd vmsvc/get.config <Vmid>`                            |
| 查看摘要信息   | `vim-cmd vmsvc/get.summary <Vmid>`                           |
| 获取网络配置   | `vim-cmd vmsvc/get.networks <Vmid>`                          |
| 创建快照       | `vim-cmd vmsvc/snapshot.create <Vmid> "Snapshot Name" "Description"` |
| 列出快照       | `vim-cmd vmsvc/snapshot.get <Vmid>`                          |
| 恢复快照       | `vim-cmd vmsvc/snapshot.revert <Vmid> <SnapshotId>`          |
| 删除快照       | `vim-cmd vmsvc/snapshot.remove <Vmid> <SnapshotId>`          |
| 注册新虚拟机   | `vim-cmd solo/registervm </vmfs/volumes/datastore1/Clone_VM_DIR/VM_NAME.vmx>` |
| 取消注册       | `vim-cmd vmsvc/unregister 54`                                |



```bash
new_vm=mysql-uat04-s3
# 创建新虚拟机目录
mkdir /vmfs/volumes/data/${new_vm}/
cp -a /vmfs/volumes/data/mongodb-uat01-s3/* /vmfs/volumes/data/${new_vm}/ &

sed -i -e '/^displayName/c\displayName = "mysql-uat01-s3"' \
       -e '/^uuid\.bios/c\uuid.bios = ""' \
       -e '/^uuid\.location/c\uuid.location = ""' \
       -e '/^ethernet0\.generatedAddress =/c\ethernet0.generatedAddress = ""' \
       -e '/swap/d' \
       /vmfs/volumes/data/mysql-uat01-s3/mongodb-uat01-s3.vmx

vim-cmd solo/registervm /vmfs/volumes/data/mysql-uat01-s3/mongodb-uat01-s3.vmx

vim-cmd vmsvc/power.on 68
```







tidb 导出数据 dm 和 dumping

pump 组件的功能

tiup dmctl 命令的使用

br backup 命令的使用



```bash
# 创建新虚拟机目录
mkdir /vmfs/volumes/data/mongodb-uat02-s3/
cp -a /vmfs/volumes/data/mongodb-uat01-s3/* /vmfs/volumes/data/mongodb-uat02-s3/




mkdir /vmfs/volumes/data/mongodb-uat03-s3/
cp -a /vmfs/volumes/data/mongodb-uat01-s3/* /vmfs/volumes/data/mongodb-uat03-s3/


# 复制所有文件到克隆目录
find . -type f -exec cp --parents "{}" /vmfs/volumes/66f36c11-47342fc7-cae6-246e96cd12a4/vm-clone-49 \;
# 编辑克隆机的VMX文件
vi /vmfs/volumes/66f36c11-47342fc7-cae6-246e96cd12a4/vm-clone-49/源虚拟机名.vmx

# 修改以下关键参数：
displayName = "克隆虚拟机名"  # 更改虚拟机名称
uuid.bios = ""               # 清空BIOS UUID
ethernet0.generatedAddress = ""  # 清空MAC地址
scsi0:0.fileName = "克隆目录名/磁盘名.vmdk"  # 更新磁盘路径
```





### `vim-cmd` 主要命令空间解析

| 命令空间           | 功能描述           | 常用场景                  |
| :----------------- | :----------------- | :------------------------ |
| **`vmsvc/`**       | 虚拟机生命周期管理 | 启动/停止/重启/迁移虚拟机 |
| **`hostsvc/`**     | 主机系统管理       | 主机维护模式、服务控制    |
| **`hbrsvc/`**      | 基于主机的复制     | 虚拟机备份与复制          |
| **`proxysvc/`**    | 代理服务           | 网络和连接管理            |
| **`internalsvc/`** | 内部服务           | 高级调试和诊断            |
| **`solo/`**        | 独立操作           | 特定硬件操作              |
| **`vimsvc/`**      | vCenter 服务       | 集群和高级功能            |