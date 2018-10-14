---
title: NoSQL笔记
date: 2017-06-26 22:55:03
tags: [NoSQL, linux, 运维]
category: 数据库
---

# NoSQL 简介

* NoSQL,全名为Not Only SQL，指的是非关系型数据库
* 随着访问量的上升，网站的数据库性能出现了问题，于是nosql被设计出来

优点/缺点
* 高可扩展性
* 分布式计算
* 低成本
* 架构的灵活性，半结构化数据
* 没有复杂的关系
缺点：
* 没有标准化
* 有限的查询功能
* 最终一致是不直观的程序

<!-- more -->

## 基本配置
* 在源文件/usr/local/redis目录下，文件redis.conf为配置文件
* 绑定地址：如果需要远程访问，可以将此行注释
    bind 127.0.0.1
* 端口，默认6379
    port 7379
    
* 是否以守护进程运行
    如果以守护进程运行，则不会在命令行阻塞
    如果以非守护进程运行，则当前终端被阻塞，无法使用
    推荐改为yes，以守护进程运行
    daemonize no|yes
    
* 数据文件
    dbfilename dump.rdb
* 数据文件存储路径
    dir的默认值为./,当前目录
    推荐改为：dir /var/lib/redis
    
## 使用配置文件启动
sudo redis-server /etc/redis/redis.conf

* 停止redis服务
    ps ajx | grep redis
    sudo kill -9 redis的进程id
    
## 数据操作
* redis是key-value的数据，所以每个数据都是一个键值对
* 键的类型是字符串
* 值得类型分为五种：
    字符串string
    哈希hash
    列表list
    集合set
    有序集合zset
* 数据操作的全部命令
## string
* string是redis最基本的类型
* 最大能存储512MB的数据
* string类型是二进制安全的，即可以为任何数据，比如数字、图片、序列化对象等

## 命令
设置键值：
    set key value
设置键值及过期时间，以秒为单位
    setex key seconds value
    
设置多个键值

MSET key value [key value ...]

## 获取
* 根据键获取值，如果不存在此键，则返回null
    GET key
* 根据多个键获取多个值
* MGET key [key ...]

## 运算
* 要求：值是数字
* 将key对应的value加1
    INCR key
* 将key对应的value加整数
    INCRBY key increment
* 将key对应的value减1
    DECR key
* 将key对应的value减整数
    DECRBY key decrement
    
## 其他
* 追加值
    APPEND key value
* 获取值长度
    STRLEN key 
    
## 键的命令
* 查找键，参数支持正则
KEYS pattern
* 判断键是否存在，如果存在返回1，不存在返回0
    EXISTS key [key ...]
    
* 查看键对应的value的类型
    TYPE key
* 删除键及对应的值
    DEL key [key ...]
    
* 设置过期时间，以秒为单位
* 创建时没有设置过期时间则一直存在，知道使用DEL移除
    EXPIRE key seconds
查看有效时间，以秒为单位
TTL key

## hash 
* hash 用于存储对象，对象的格式为键值对

## 命令
* 设置:
    设置单个属性
    HSET key field value
    设置多个属性
    HMSET key field value [field value...]
* 获取
    获取一个属性的值
    HGET key field
    获取多个属性的值
    HMGET key field [field ...]
    获取所有属性和值
    HGETALL key
    获取所有的属性
    HKEYS key
    返回包含属性的个数
    HLEN key
    获取所有值
    HVALS key

* 其他
    判断属性是否存在
    HEXISTS key field
    删除属性及值
    HDEL key field [field ...]
    返回值得字符串长度
    HSTRLEN key field 

## list
* 列表的元素类型为string
* 按照插入顺序排序
* 在列表的头部或者尾部添加元素

### 命令：
* 在头部插入数据
    PUSH key value [value ...]
* 在尾部插入数据
    RPUSH key value [value ...]
* 在一个元素的前|后插入新元素
    LINSERT key BEFORE|AFTER pivot value

* 设置指定索引的元素值
* 索引是基于0的下标
* 索引可以是负数，表示偏移量是从list尾部开始计算，如-1表示列表的最后一个元素
* LSET key index value
* 获取
    移除并且返回key对应的list的第一个元素
    LPOP key
* 移除并返回存于key 的list的最后一个元素

    RPOP key
* 返回存储在key的列表里指定范围内的元素
* start 和end偏移量都是基于0的下标
* 偏移量也可以是负数，表示偏移量是从list尾部开始计数，如-1表示列表的最后一个元素
    LRSNGE key start stop

* 其他：
    裁剪列表，改为原集合的一个子集
    start和end偏移量都是基于0的下标
    返回存储在key里的list的疮毒
    LLEN key
    返回列表里索引对应的元素
    LINDEX key index
    
## set 
* 无序集合
* 元素为string类型
* 元素具有唯一性，不重复

* 添加元素
    SADD key member [member ...]
    
* 获取
    返回key集合所有的元素
    SMEMBERS key
    返回集合元素个数
    SCARD key


