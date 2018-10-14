---
title: java连接orcale数据库
date: 2017-04-19 23:27:18
tags: [java, oracle]
category: java
---





因为 oracle数据库这种东西，如果以前安装过的话，不容易卸载干净，又安装别的版本的数据库，会导致错误百出。建议清理完之后再安装本版本，避免浪费不必要的时间，实在不行，就重装系统吧，去年我的同学就这么干的。


<!-- more -->



我稍微提一下，如何卸载干净，毕竟重装系统损失还是很大的，通过实践，首先进入控制面板把oracle卸载，然后这个时候重启，否则文件夹删不掉，重启完毕之后删除残余的文件夹，就是你安装的目录，一定要删干净，然后 开始 运行 cmd 输入 regedit 进入之后，按CTRL+F 然后查找 输入ora 查找到一个，删除一个，然后继续循环执行，查找删除知道最后查找没有为止，然后重启一遍。 安装 oracle就好了，不要在安装路径里带有中文名字。

我说一下，这几天有同学问我，说还是不可以。我就提出两个比较关键的问题，

第一：你以前安装的oracle是否真的卸载干净了，打开注册表，查找，如果没有了，在查找，如果还没有则证明删除干净，有些注册表里 查找到的项目删除不了，可以跳过。

第二：你的lib包是否导入正确，请将oracle那个路径的jar文件复制，然后在你的项目中新建一个文件夹，然后点击那个文件夹，右键粘贴，然后在进行build path操作。



# 使用java代码连接oracle数据库教程

本教程适合安装 oracle精简版的用户。[下载地址](https://pan.baidu.com/s/1jIkfbQA)，也就200多兆，学习基本够用了，没必要安装完整版的。

1.在本地安装oracle数据库，下载完后，一路安装即可,记住你设置的密码 ，建议密码设为123456  下面要用。

安装完毕后打开任务管理器，选择服务，然后 打开服务，把ora开头的那一排服务全部开启，如果无法开启，单击属性选择自动，然后再次右键就可以开启服务了。

![](http://i2.muimg.com/567571/e8a50559b8ad571e.jpg)

![](http://i2.muimg.com/567571/c4f2287c2414d736.jpg)

![](http://i4.buimg.com/567571/3e032058bce9609d.png)



2.完成之后，重启电脑。

3.重启完毕之后 ，打开开始 运行 cmd  输入 sqlplus出现下图效果，表明数据库安装成功。

![](http://i2.muimg.com/567571/6f003f916f95cf37.png)

### 配置eclipse，myeclipse基本一样

第一步：导入oracle的驱动。，步骤：打开oracle安装目录：进入oracle\product\10.2.0\jdbc\lib ，复制ojdbc14.jar包。此包即为oracle的驱动包。打开eclipse ,在项目下新建一个Folder 取名为lib ，粘贴进ojdbc14.jar包。

第二步：右键项目，选中build path 再configure build path.然后如下图选择Libraries，右边选择Add JARs,，然后在出现的窗口中选择你刚才把包复制进的那个项目，选择刚才新建的lib文件夹，然后选中ojdbc14.jar，点击OK。

![](http://i1.piimg.com/567571/05974fd04903db51.png)

![](http://i4.buimg.com/567571/9ccf77c55f6b482e.png)





![](http://i4.buimg.com/567571/da0a7ceb3e88de52.png)



![](http://i2.muimg.com/567571/574717eedb75743e.png)



选择之后 ，ok  ok  就行了 。然后就配置好了， 接下来开始 打代码 试验是否成功

![](http://i4.buimg.com/567571/271fb555bfb96bca.png)



好了，我的成功了。 

## 下面附上测试的代码:

~~~
import java.sql.*;
public class Main {
	public static void main(String[] args) {
				String url="jdbc:oracle:thin:@127.0.0.1:1521:XE";
				String userName="system";
				String passWord="123456";  //改成你自己设置的密码
				Connection conn=null;
				try{
					Class.forName("oracle.jdbc.OracleDriver");
					conn=DriverManager.getConnection(url,userName,passWord);
					System.out.println("连接成功");
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		}
~~~

其中，注意 ，精简版的oracle url  ：

```
url="jdbc:oracle:thin:@127.0.0.1:1521:XE"  //精简版的oracle的名字为 XE  ，其他版本自己查询。
```



我看到很多人把ip地址设置成自己的网络的ip，这样很不好，因为并不一定每次你的IP地址都一样，设置成127.0.0.1 就表示 本机的地址。



# 补充

刚才给同学安装的时候，发现照此办法，仍然出现了一堆错误，经过紧张的十几分钟的google 发现了一个解决方法就是，因为 以前的老版本驱动存在bug ，所以，在新的jdk上面就禁止使用了老版本的驱动，同学jdk版本是 1.8 ，解决这个问题的办法是，到官网下载  **ojdbc6.jar**驱动，然后导入eclipse即可，[ojdbc6.jar链接](http://pan.baidu.com/s/1cL9hfw)

以下是错误的信息：

~~~
java.lang.NullPointerException
	at java.lang.String.<init>(Unknown Source)
	at oracle.sql.CharacterSet.AL32UTF8ToString(CharacterSet.java:1517)
	at oracle.jdbc.driver.DBConversion.CharBytesToString(DBConversion.java:589)
	at oracle.jdbc.driver.DBConversion.CharBytesToString(DBConversion.java:542)
	at oracle.jdbc.driver.T4CTTIoauthenticate.receiveOauth(T4CTTIoauthenticate.java:816)
	at oracle.jdbc.driver.T4CConnection.logon(T4CConnection.java:362)
	at oracle.jdbc.driver.PhysicalConnection.<init>(PhysicalConnection.java:414)
	at oracle.jdbc.driver.T4CConnection.<init>(T4CConnection.java:165)
	at oracle.jdbc.driver.T4CDriverExtension.getConnection(T4CDriverExtension.java:35)
	at oracle.jdbc.driver.OracleDriver.connect(OracleDriver.java:801)
	at java.sql.DriverManager.getConnection(Unknown Source)
	at java.sql.DriverManager.getConnection(Unknown Source)
	at Main.main(Main.java:10)
~~~



如果有什么问题，欢迎给我发[email](mailto:zhaochensy@gmail.com)，可以共同解决。


