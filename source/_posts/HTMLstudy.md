---
title: HTML学习笔记
date: 2017-04-20 16:47:56
tags: [前端, html]
category: 学习笔记
---
# HTML

```
通过 <h1>这是一级标题</h1>
    <h2> 这是二级标题</h2>
    <h3>这是三级标题</h3>
    <h4>这是四级标题</h4>
    ....
    <h6>这是六级标题</h6>


通过上面的6个标题，6种级别的标题表示文档的6级目录层级关系。搜索引擎会使用标题将网页的结构和内容编制索引，所以网页上使用标题是很重要的。
```
<!-- more -->

## html段落、换行与字符实体
* html段落

```
 <p> 标签定义一个文本段落，一个段落含有默认的上下间距，段落之间会用这种默认间距隔开，代码如下：
 
 <!DOCTYPE html>
 <html lang="en">
 <head>
    <meta charset="utf-8">
    <title>段落</title>
 </head>
 <body>
    <p>Hello</p>
    
    <p>world</p>
 </body>
 </html>
```

* html换行

```
    代码中成端的文字，直接在代码中回车换行，在渲染的网页的时候不认这种换行，如果真的想换行，可以在代码的段落中插入<br /> 来强制换行，代码如下：
    <p>
    hello <br />
    world <br />
    </p>
```

* html 字符实体
    
```
代码中成端的文字，如果文字间想空多个空格，在代码中空多个空格，在渲染成网页时，只会显示一个空格，如果想显示多个空格，可以使用空格的字符实体，代码如下：

<!-- 在段落前想缩进两个文字的空格，使用空格的字符实体: &nbsp;  -->
<p>
&nbsp;&nbsp;一个html文件就是一个网页。</p>

在网页上面显示“<" 和 ”>" 会被误认为是标签，想在网页上面显示他们，可以用它们的字符实体，比如：

<!-- "<" 和 “>" 的字符实体为 &lt; 和&gt; -->
<p>
    3 &lt; 5 <br>
    10 &gt; 5 
</p>

```

* html块
    
   1.div标签 块元素，表示一块内容，没有具体的语义。
   2.span标签行内元素，表示一行中的一小段内容，没有具体的语义

* 含样式和语义的标签
    
    1. em标签 行内元素，表示语气中的强调词
    2. i标签 行内元素，原本没有语义，w3c强加了语义，表示专业词汇
    3. b标签 行内元素，原本没有语义，w3c强加了语义，表示文档中的关键字或者产品名
    4. strong标签 行内元素，表示非常重要的内容

* 语义化的标签
    
    语义化的标签，就是在布局的时候多使用语义化的标签，搜索引擎在爬网的时候能认识这些标签，理解文档的结构，方便网站的收录。比如：h1标签是表示标题，p标签是表示段落，ul、li标签是表示列表，a标签表示链接，dl、dt、dd表示定义列等，语义化的标签不多。
    
* html图像、绝对路径和相对路径

```

 html 图像 
 <img> 标签可以在网页上面插入一张图片，它是独立的标签，通过”src“属性定义图片的地址，通过”alt“属性定义图片加载失败时候显示的文字，以及对搜索引擎和盲人读屏软件的支持。
 
 <img src="images/pic.jpg" alt="产品图片" />
 
```

* 绝对路径和相对路径
    
    ```
    像网页上插入图片这种外部文件，需要定义文件的引用地址，引用外部文件还包括引用外部样式表，javascript等等，引用地址分为绝对地址和相对地址。
    
    绝对地址：相对于磁盘的位置去定位文件的地址
    相对地址： 相对于引用文件本身去定位被引用的文件地址
    
    绝对地址在整体文件迁移时会因为磁盘和顶层目录的改变而找不到文件，相对路径就没有这个问题。相对路径的定义技巧：
    "./" 表示当前文件所在目录下，比如: "./pic.jpg" 表示当前目录下的 pic.jpg的图片，这个使用时可以省略。
    "../" 表示当前文件所在目录的上一级目录，比如 "../images/pic.jpg"表示当前目录下的上一级目录下的images文件夹中的pic.jpg的图片
    
    ```
    
* html链接

```
<a>标签可以在网页上定义一个链接地址，通过src属性定义跳转的地址，通过title属性定义鼠标悬停时弹出的提示文字框。

<a href="#">回到顶部 </a>   <!-- #表示链接到页面顶部  -->
<a href="http://www.baidu.com/" title="跳转到百度">"百度"</a>
<a href="2.html">测试页面2</a>

```

* 定义页面内滚动跳转

```
页面内定义了“id”或者“name"的元素，可以通过a标签链接到它的页面滚动位置，前提是页面要足够高，有滚动条，且元素不能再页面顶部，否则页面不会滚动。

<a href="#mao1"标题一 </a>
......
......
< h3 id="mao1"> 跳转到的标题</h3>
```

* html列表

```
有序列表：
    在网页上定义一个由编号的内容列表可以使用<ol>、<li>配合使用来实现，代码如下：
    
    <ol>
        <li>列表文字一</li>
        <li>列表文字二</li>
        <li>列表文字三</li>
    </ol>
    在网页上生成的列表，每条项目会被1、2、3编号，有序列表在实际开发中较少使用。
    
无序列表：
    在网页上定义一个无编号的内容列表可以用<ul>、<li>配合使用来实现，代码如下：
    
    <ul>
        <li>列表文字一</li>
        <li>列表文字二</li>
        <li>列表文字三</li>
    </ul>
    在网页上生成的列表，每条项目上都有一个小图标，这个小图标在不同浏览器上显示效果不同，所以一般会用样式去掉默认的小图标，如果需要图标，可以用样式自定义图标，从而达到在不同浏览器上显示的效果相同，实际开发中一般用这种列表。
   
定义列表:
    定义列表通常于术语的定义。<dl>标签标示列表的整体。<dt>标签定义术语的题目。
    <dd>标签是术语的解释。一个<dl>中可以又多个题目和解释，代码如下：
    
        <h3>前端</h3>
        <dl>
            <dt>html</dt>
            <dd>负责页面的结构</dd>
            
            <dt>css</dt>
            <dd>负责页面的表现</dd>
            
            <dt>javascript</dt>
            <dd>负责页面的行为</dd>
        </dl>
    
```

* html表格

```
table常用标签
    1.table标签：声明一个表格
    2.tr标签：定义表格中的一行
    3.td和th标签：定义一行中的一个单元格，td代表普通单元格，th表示表头单元格
    
table常用属性：
    1.border 定义表格的边框
    2.cellpadding 定义单元格内内容与边框的距离
    3.cellspacing 定力单元格与单元格之间的距离
    4.align 设置单元格中内容的水平对齐方式，设置值又：left|center|right
    5.valign 设置单元格中内容的垂直对齐方式 top | middle | bottom
    6.colspan 设置单元格水平合并
    7.rowspan 设置单元格垂直合并

传统布局：
    传统的布局方式就是使用table来做整体页面的布局，布局的技巧归纳为如下几点：
        1.定义表格狂傲，将border、cellpadding、cellspacing全部设置为0
        2.单元格里面嵌套表格
        3.单元格中的元素和嵌套的表格用align和valign设置对齐方式
        4.通过属性或者css样式设置单元格中元素的样式

传统布局目前应用：
    1.快速制作用于演示的html页面
    2.商业推广EDM制作（广告邮件）
    有兴趣可以查  table布局实例
    
表格常用样式属性
    border-collapse 设置边框合并，制作一像素宽的变现的表格

```

* html表单
    
    ```
    表单用于搜集不同类型的用户输入，表单由不同类型的标签组成，实现一个特定功能的表单区域（比如：注册），首先应该用<form>标签来定义表单区域的整体，在此变迁中再使用不同的表单空间实现不同类型的信息输入，代码如下：
    
    <!-- from 定义一个表单区域，action属性定义表单数据提交的地址，method属性定义提交的方式。-->
    <form action="http://www..." method="get">
    <!-- label 标签定义表单控件的文字标注，input类型为text定义了一个单行文本框输入-->
    <p>
    <label>姓名：</label><input type="text" name="username" />
    </p>
    
    <! -- input 类型为password定义了一个密码输入框 -->
    <p>
    <label>密码：</label> <input type="password" name="password" />
    </p>
    
    <!-- input 类型为radio定义了单选框 -->
    <p>
    <label>性别：</label>
    <input type="radio" name="gender" value="0" /> 男
    <input type="radio" name="gender" value="1" /> 女
    </p>
    
    <!-- input 类型为checkbox定义了复选框 -->
    <p>
    <label>爱好：</label>
    <input type="checkbox" name="like" value="sing" /> 唱歌
    <input type="checkbox" name="like" value="run" /> 跑步
    <input type="checkbox" name="like" value="swiming" /> 游泳
    </p>
    
    <!-- input类型为file定义上传照片或文件等资源 -->
    <p>
    <label>照片:</label>
    <input type="file" name="person_pic">
    </p>
    
    <!-- textarea定义多行文本输入 -->
    <p>
    <label>个人描述：</label>
    <textarea name="about"></textarea>
    </p>
    
    <!-- select 定义下拉列表选择 -->
    <p>
    <label>籍贯:</label>
    <select name="site">
        <option value="0">北京</option>
        <option value="1">上海</option>
        <option value="2">广州</option>
        <option value="3">深圳</option>
    </select>
    </p>
    
    <!-- input 类型为submit定义提交按钮
        还可以用图片控件代替submit按钮提交，一般会导致提交两次，不建议使用。如
        <input type="image" src="xxx.gif">
    -->
    <p>
    <input type="submit" name="" value="提交">
    
    <!-- input 类型为reset定义重置按钮 -->
    <input type="reset" name="" value="重置">
    </p>
    
    </form>
    
    
    ```
    
    * html 内嵌框架
    
    ```
     <iframe>标签会创建包含另一个html文件的内联框架（即行内框架），src属性来定义另一个html文件的引用地址，frameborder属性定义边框，scrolling属性定义是否有滚动条，代码如下：
     <iframe src="http://www...." frameborder="0" scrolling="no"> </iframe>
     内嵌框架与a标签配合使用
        a标签的target属性可以将连接到的页面直接显示在当前页面的iframe中，代码如下：
        <a href="01.html" target="myframe">页面一</a>
        <a href="02.html" target="myframe">页面二</a>
        <a href="03.html" target="myframe">页面三</a>
        <iframe src="01.html" frameboder="0" scrolling="no" name="myframe"></iframe>
    ```

    

