---
title: Linux磁盘管理
tags: [Linux]
category: Linux
date: 2018-12-1
---

内存中每读取一次数据，数据就没了，就需要再次充电增压，以保持数据存在。

每个硬件上面会注册内核提供的一个或几个端口，内核使用16bit大小的空间，可以保存65536 个。称为 I/O Ports 。 I/O 设备地址



Linux 文件类型：

​	块设备：，block，存取单位“块”

​	字符设备： char，存取单位“字符”，键盘

​	设备文件： 关联至一个设备驱动程序，进而能够与之对应硬件进行通信，即数据的输入输出。

设备号码：

​	主设备好： major number，标识设备类型

​	次设备号：minor number，标识同一类设备下的不同设备

/dev/DEV_FILE 是磁盘设备的命名方式

硬盘接口类型：

并行：

​	IDE    133MB/s  (大写的 b，是 byte 的意思)

​	SCSI    640 MB/s 

需要降低线缆之间的信号干扰

串口：

​	SATA  6Gbps

​	SAS	6Gbps

​	USB  480MB/s

上面的速率都是接口速率，而不是硬件速率，实际传输速率会低很多。



按柱面划分来分区

0磁道0扇区： 512 bytes

MBR：主引导分区记录

​	446bytes： boot loader

​	64 bytes：分区表

​		16 bytes： 标识一个分区（只能有4个主分区，但是可以通过逻辑分区来有多个分区）（UEFI 除外）

​	2 bytes： 55AA

MBR 是无法识别 2T 的空间的，需要使用 GPT。



分区工具：

​	fdisk， parted， sfdisk

​	fdisk： 对于一块硬盘来讲，最多只能管理15块分区

​	fdisk -l



Linux 文件系统管理：

​	Linux 文件系统： ext2，ext3，ext4， xfs， btrfs， reiserfs， jfs， swap

swap： 交换分区，把硬盘格式化成内存的格式，来供在物理内存不足时 使用。



文件系统的组成部分：

​	内核中的模块： ext4, xfs, vfat

​	用户空间的管理工具：mkfs.ext4, mkfs.xfs, mkfs.vfat



Linux 的虚拟文件系统：VFS， 来规避底层的差异。

创建文件系统：

​	mkfs.FS_TYPE /dev/DEVICE