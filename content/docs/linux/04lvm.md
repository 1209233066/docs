---
date: '2025-05-18T18:15:33+08:00'
draft: false
title: 'LVM (logical volume manager)'
linkTitle: 'LVM'
type: blog
toc_hide: false
hide_summary: true
weight: 4
description: >
  linux lvm
tags: ["linux", "lvm"]
categories: ["lvm"]
url: linux/lvm.html
---





**术语：**

:one:**物理卷PV**(Physical Volume):  通过 `pvcreate` 创建的物理设备（如磁盘或分区），是LVM的基础存储单元。

:two:**物理块PE**(Physical Extent) LVM管理的最小存储单元，默认大小为4MB

:three:**卷组VG**(Volume Group) 由多个PV组合而成，构成逻辑存储池。

:four:**逻辑卷LV**(Logical Volume) 从VG中划分的逻辑分区，可挂载使用。

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux-8-Configuring_and_managing_logical_volumes-en-US/images/31bd96635c4120abe3e771a423f61cd6/basic-lvm-volume-components.png)



### 环境准备

**创建pv**

```bash
root@lvm:~# pvcreate /dev/sd{c..g}
  Physical volume "/dev/sdc" successfully created.
  Physical volume "/dev/sdd" successfully created.
  Physical volume "/dev/sde" successfully created.
  Physical volume "/dev/sdf" successfully created.
  Physical volume "/dev/sdg" successfully created.
```

**创建vg**

```bash
root@lvm:~# vgcreate data /dev/sd{c..f}
  Volume group "data" successfully created
```

### 逻辑卷类型

{{< tabpane text=true right=false >}}
  {{% tab header="**逻辑卷类型**:" disabled=true /%}}
  {{% tab header="线性卷" lang="en" %}}

  ```bash
  lvcreate --name test-nomarl --size 1g data
  ```

  ```bash
  root@pc:~# lvs --select lv_name="test-nomarl" -o lv_name,vg_name,lv_size -o +seg_type
    LV          VG   LSize Type  
    test-nomarl data 1.00g linear
  ```
  {{% /tab %}}
  {{% tab header="条带化卷" lang="en" %}}

> --stripes 条带数量，不超过pv数量
>
> --stripesize  条带大小，超过该值的大小保存到下一个pv上

```bash
lvcreate --name test-stripes --stripes 4 --stripesize 64kb --size 1g  data
```

```bash
root@lvm:~# lvs --select lv_name="test-stripes" -o lv_name,vg_name,lv_size -o +seg_type
  LV           VG   LSize Type   
  test-stripes data 1.00g striped
```

  {{% /tab %}}

  {{% tab header="Raid卷" lang="en" %}}
> 包括 RAID0、RAID1、RAID4、RAID5、RAID6 和 RAID10


  - RAID 4 的校验集中在一个磁盘，RAID 5 和 6 的校验分散在所有磁盘。
  - RAID 6 有两份独立的校验（如 P+Q 或 Reed-Solomon 编码），可承受双磁盘故障。

  | RAID级别 | 校验方式                           | **写入性能特点**                                             | 容错能力             | 最小磁盘数 |
  | -------- | ---------------------------------- | ------------------------------------------------------------ | -------------------- | ---------- |
  | RAID 4   | **专用校验盘**（固定某个磁盘）     | **写入瓶颈**：所有校验数据写入专用盘，高负载时易成为性能瓶颈。 | 允许 **1块磁盘故障** | 3块        |
  | RAID 5   | **分布式校验**（校验块轮流分布）   | **较高并发**：校验分散，支持并行读写，但每次写操作需计算并更新校验块（读-改-写）。 | 允许 **1块磁盘故障** | 3块        |
  | RAID 6   | **双重分布式校验**（两套独立校验） | **较低写入速度**：相比 RAID 5，每次写入需计算两套校验，延迟更高（更高的 *写惩罚*）。 | 允许 **2块磁盘故障** | 4块        |




  + Raid0  
    > 最少2块pv, 2个条带

    ```bash
    lvcreate --name test-raid0 --type raid0 --stripes 4 --stripesize 64k --size 1g data
    ```

    ```bash
    root@pc:~# lvs --select lv_name="test-raid0" -o lv_name,vg_name -o +seg_type 
      LV         VG   Type 
      test-raid0 data raid0
    ```

  + raid4 ，raid5

    > 最少3块pv, 2个条带

    ```bash
    lvcreate --name test-raid4 --type raid4 --stripes 2 --stripesize 64k --size 1g data
    ```

    ```bash
    root@pc:~# lvs --select lv_name="test-raid4" -o lv_name,vg_name -o +seg_type 
      LV         VG   Type 
      test-raid4 data raid4
    ```

    
    raid5
    ```bash
    lvcreate --name test-raid5 --type raid5 --stripes 2 --stripesize 64k --size 100g data
    ```

    ```bash
    root@pc:~# lvs --select lv_name="test-raid5" -o lv_name,vg_name -o +seg_type 
      LV         VG   Type 
      test-raid5 data raid5
    ```

    raid6
    > 最少5块pv，3个条带

    ```bash
    lvcreate --name test-raid6 --type raid6 --stripes 3 --stripesize 64k --size 10g data
    ```

    ```bash
    root@pc:~# lvs --select lv_name="test-raid6" -o lv_name,vg_name -o +seg_type 
      LV         VG   Type 
      test-raid6 data raid6
    ```

  + raid1
    ```bash
    # lvcreate --type raid1 --mirrors MirrorsNumber --size Size --name LogicalVolumeName VolumeGroupName
    ```

    ```bash
    lvcreate --name raid1 --type raid1 --mirrors 1 --size 1g data 
    ```
  + raid10

    ```bash
    # lvcreate --type raid10 --mirrors MirrorsNumber --stripes NumberOfStripes --stripesize StripeSize --size Size --name LogicalVolumeName VolumeGroupName
    ```

    ```bash
    lvcreate --name raid10 --type raid10 --mirrors 1 --stripes 2 --stripesize 64k --size 1g data 
    ```

  {{% /tab %}}

  {{% tab header="精简卷" lang="en" %}}

  ```bash
  # lvcreate --type thin-pool --size PoolSize --name ThinPoolName VolumeGroupName
  ```

  ```bash
  lvcreate --name thinpool --type thin-pool --size 1g data
  ```

  ```bash
  # lvcreate --type thin --virtualsize MaxVolumeSize --name ThinVolumeName --thinpool ThinPoolName VolumeGroupName
  ```

  ```bash
  lvcreate --name test-thin --type thin --virtualsize 100g --thinpool thinpool data
  ```

{{% /tab %}}

{{< /tabpane >}}





### 场景举例
场景：磁盘空间马上要满


**第一步：创建分区或增加一块硬盘**

vmware 扩展磁盘分区


**第二步：给刚才扩展的磁盘分配一个分区**

查看磁盘有多少未分区空间

```bash
[root@lvm ~]# parted /dev/sda
GNU Parted 3.1
使用 /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print free
Model: VMware, VMware Virtual S (scsi)
Disk /dev/sda: 69.8GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  标志
        32.3kB  1049kB  1016kB           Free Space
 1      1049kB  1075MB  1074MB  primary  xfs          启动
 2      1075MB  21.5GB  20.4GB  primary               lvm
        21.5GB  64.4GB  42.9GB           Free Space
```

创建分区

```bash
[root@lvm ~]# fdisk /dev/sda
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition type:
   p   primary (2 primary, 0 extended, 2 free)
   e   extended
Select (default p): p
Partition number (3,4, default 3):
First sector (41943040-125829119, default 41943040):
Using default value 41943040
Last sector, +sectors or +size{K,M,G} (41943040-125829119, default 125829119):
Using default value 125829119
Partition 3 of type Linux and of size 40 GiB is set
Command (m for help): w

```

通知内核分区变动,否则需要重启操作系统

```bash
[root@lvm ~]# partprobe
```

**第三步：把分区转换为pv**

```bash
[root@lvm ~]# pvcreate /dev/sda3
  Physical volume "/dev/sda3" successfully created.
```



```bash
[root@lvm ~]# pvs
  PV         VG                                        Fmt  Attr PSize   PFree
  /dev/sda2  centos                                    lvm2 a--  <19.00g     0
  /dev/sda3                                            lvm2 ---   40.00g 40.00g
```

**第四步：扩展所在vg**

```bash
[root@lvm ~]# vgextend centos /dev/sda3
  Volume group "centos" successfully extended
```

```bash
[root@lvm ~]# vgs centos
  VG     #PV #LV #SN Attr   VSize  VFree
  centos   2   2   0 wz--n- 58.99g <40.00g
```

**第四步：调整lv的空间大小**

```bash
[root@lvm ~]# lvresize -L  +39g /dev/centos/root
  Size of logical volume centos/root changed from <17.00 GiB (4351 extents) to <56.00 GiB (14335 extents).
  Logical volume centos/root successfully resized
```

**第五步：通知文件系统调整文件系统大小**

```bash
[root@lvm ~]# xfs_growfs /dev/mapper/centos-root
meta-data=/dev/mapper/centos-root isize=512    agcount=4, agsize=1113856 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0 spinodes=0
data     =                       bsize=4096   blocks=4455424, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal               bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 4455424 to 14679040
```

**完成**

```bash
[root@lvm ~]# df -HT
文件系统                类型      容量  已用  可用 已用% 挂载点
devtmpfs                devtmpfs  1.5G     0  1.5G    0% /dev
tmpfs                   tmpfs     1.5G     0  1.5G    0% /dev/shm
tmpfs                   tmpfs     1.5G   11M  1.5G    1% /run
tmpfs                   tmpfs     1.5G     0  1.5G    0% /sys/fs/cgroup
/dev/mapper/centos-root xfs        61G   15G   46G   25% /
/dev/sda1               xfs       1.1G  224M  840M   22% /boot
tmpfs                   tmpfs     1.5G   25k  1.5G    1% /var/lib/ceph/osd/ceph-1
tmpfs                   tmpfs     1.5G   25k  1.5G    1% /var/lib/ceph/osd/ceph-0
tmpfs                   tmpfs     1.5G   25k  1.5G    1% /var/lib/ceph/osd/ceph-2
tmpfs                   tmpfs     297M   13k  297M    1% /run/user/42
tmpfs                   tmpfs     297M     0  297M    0% /run/user/0
```



```bash
[root@lvm ~]# lsblk -f /dev/sda
NAME            FSTYPE      LABEL UUID                                   MOUNTPOINT
sda
├─sda1          xfs               2698408f-1135-4c91-b11c-02892e5208f8   /boot
├─sda2          LVM2_member       eZESEK-nJJ1-UvCV-x3st-lJKM-m3Zx-JZNvWO
│ ├─centos-root xfs               e011e279-e5c9-4dfd-87e9-ecfc7e46bccd   /
│ └─centos-swap swap              e14f66e7-6647-486f-a9d7-acc044d455a1
└─sda3          LVM2_member       ugnjZw-FN0H-V8vi-acLb-D6sC-YB1f-CtZIF7
  └─centos-root xfs               e011e279-e5c9-4dfd-87e9-ecfc7e46bccd   /
```


参考
[红帽](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html-single/configuring_and_managing_logical_volumes/index)