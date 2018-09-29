---
title: jquery学习笔记
date: 2018-04-04 16:47:56
tags: [前端, jquery]
category: 学习笔记
---

# jquery学习笔记

* jquery加载
    
将获取元素的语句写到页面头部，会因为元素还没有加载而出错，jquery提供了ready方法解决这个问题，它的速度比原声的window.onload更快。
```
    <script type="text/javascript">
    
    $(document).ready(function(){
        ....
    });
    
    </script>
```

<!-- more -->

可以简写为：

```
    <script type="text/javascript">
    
    $(function(){
        ...
    });
    
    </script>
```

* jquery选择器
    
jquery 用法思想
    选择某个网页元素，然后对它进行某种操作
jquery选择器
    jquery选择器可以快速地选择元素，选择规则和css样式相同，使用length属性判断是否选择成功
    
```
    $(document) //选择整个文档对象
    $('li')  //选择所有的li元素
    $('#myId') //选择id为myId的网页元素
    $('.myClass') //选择class为myClass的元素
    $('input[name=first]']  //选择name属性等于first的input元素
    $('#ul1 li span') //选择id为ul1元素下所有li下面的span元素

```
    
对选择集进行修饰过滤（类似CSS伪类）

```
    $('#ul1 li:first') //选择id为ul1元素下的第一个li
    $('#ul1 li:odd') //选择id为ul1元素下的li的奇数行
    $('#ul1 li:eq(2)') //选择id为ul1元素下的第3个li
    $('#ul1 li:gt(2)') // 选择id为ul1元素下的前三个之后的li
    $('#myForm :input') // 选择表单中的input元素
    $('div:visible') //选择可见的div元素
```

对选择集进行函数过滤

```
    $('div').has('p'); // 选择包含p元素的div元素
    $('div').not('.myClass'); //选择class不等于myClass的div元素
    $('div').filter('.myClass'); //选择class等于myClass的div元素
    $('div').first(); //选择第1个div元素
    $('div').eq(5); //选择第6个div元素
```
    
选择集转移

```
    $('div').prev('p'); //选择div元素前面的第一个p元素
    $('div').next('p'); //选择div元素后面的第一个p元素
    $('div').closest('form'); //选择离div最近的那个form父元素
    $('div').parent(); //选择div的父元素
    $('div').children(); //选择div的所有子元素
    $('div').siblings(); //选择div的同级元素
    $('div').find('.myClass'); //选择div内的class等于myClass的元素
```

jquery样式操作
    
    jquery用法思想二 
同一个函数完成取值和赋值

操作行间样式

```
// 获取div的样式
$("div").css("width");
$("div").css("color");
```

```
//设置div的样式
$("div").css("width","30px");
$("div").css("height","30px");
$("div").css({fontSize:"30px",color:"red"});
```

特别注意 
选择器获取的多个元素，获取信息获取的是第一个，比如：$("div").css("width")，获取的是第一个div的width。

操作样式类名

```
$("#div1").addClass("divClass2") //为id为div1的对象追加样式divClass2
$("#div1").removeClass("divClass")  //移除id为div1的对象的class名为divClass的样式
$("#div1").removeClass("divClass divClass2") //移除多个样式
$("#div1").toggleClass("anotherClass") //重复切换anotherClass样式
```
