---
title: Mac通过brew安装MongoDB时Mongo无法连接
date: 2020-08-03 14:04:42
tags: [MongoDB]
category: Mac
---

最近，升级了一下 MongoDB之后，突然发现在 终端中输入 mongo，报错如下：

```shell
Failed global initialization: InvalidSSLConfiguration: Error enumerating certificates: The specified item could not be found in the keychain.
```

但是使用 Navicat 竟然可以连接，说明有可能是 mongo 这个命令的问题，或者系统的一些设置问题。

看了下报错信息，应该是和 SSL 有关，本来本地的这个 MongoDB 也只是作为开发使用，监听在 127.0.0.1， 感觉也没有必要去大动干戈，去配置一下 SSL。

显示搜了下报错信息，然后搜了下 MongoDB 的 SSL，配 SSL 觉得有点麻烦，暂时还用不到。于是在 stackoverflow 上找到了答案。

[[Error when trying to obtain a certificate: The specified item could not be found in the keychain](https://stackoverflow.com/questions/16845169/error-when-trying-to-obtain-a-certificate-the-specified-item-could-not-be-found)](https://stackoverflow.com/questions/16845169/error-when-trying-to-obtain-a-certificate-the-specified-item-could-not-be-found/19160225#19160225)

报错信息不太一样，但是问题是同一个问题。

这里直接拿出来正确操作方法：

1. 打开钥匙串
2. 选择系统，然后看一下有没有一个叫做:  Apple Worldwide Developer Relations Certification Authority 的证书。
3. 然后确保证书图标右下角有个小 + 号，即信任的意思，我就是因为这个证书虽然在那里，但是我没有信任他，导致一系列麻烦。
4. 如果还没有信任，双击点开然后选择  信任---- 使用此证书时： 选择始终信任，也会让你输入密码验证。 
5. 证书信任之后，重新打开终端，然后输入 mongo 就可以了，确保MongoDB 服务已经启动。

