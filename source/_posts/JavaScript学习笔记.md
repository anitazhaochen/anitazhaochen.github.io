---
title: JavaScript学习笔记
date: 2018-08-10 11:55:03
tags: [前端, JavaScript]
category: 学习笔记
---

# JavaScript

* 行间事件（主要用于事件）

` <input type="button" name="" onclick="alert('ok!');"> `
* 页面script标签嵌入
    
    ```
    <script type="text/javascript">
        var a = '你好';
        alert(a);
    </script>
    ```
* 外部引入
    ` <script type="text/javascript" src="js/index.js"></script> `
    
* javascript语句与注释

<!-- more -->

```
1.一条javascript语句应该以";"结尾
<script type="text/javascript">
    var a=123;
    var b='str';
    function fn(){
        alert(a);
    };
    fn();
</script>

2.javascript注释
<script type="text/javascript">
     //单行注释
     var a=123;
     /*
        多行注释
        1.。。。
        2.。。。
        3.。。。
    */
    
    var b = 'str';
</script>
```

* 变量

```
    JavaSciprt是一种弱类型语言，javascript的变量类型由它的值来决定。定义变量需要用关键字 'var'
    var a = 123;
    var b = 'asd';
    //同时定义多个变量可以用","隔开，公用一个‘var'关键字
    var c = 45,d='qwr',f='69';
    
    变量类型：
        5种基本数据类型：
            number、string、boolean、undefined、null
        1种复合类型：
        object
    变量、函数、属性、函数参数命名规范
        1.区分大小写
        2.第一个字符必须是字母、下划线、或者美元符号
        3.其他字符可以是字母、下划线、美元符号或者数字        
```
* 获取元素的方法一

```
可以使用内置对象document上的getElementById方法来获取页面上设置了id属性的元素，获取到的是一个html对象，然后将它赋值给一个变量，比如：
    <script type="text/javascript">
        var oDiv = document.getElementById('div1');
    </script>
    ...
    <div id="div1">这是一个div元素</div>
    
上面的语句，如果把javascript写在元素的上面，就会出错，因为页面上从上往下加载执行的，javascript去页面上获取元素div1的时候，元素div1还没有加载，解决方法有两种：
第一种方法：将javascript 放到页面最下边

    ...
    <div id="div1"> 这是一个div元素</div>
    ...
    
    <script type="text/javascript">
        var oDiv = document.getElementById('div1');
    <script>

第二种方法：将javascript语句放到window.onload触发的函数里面，获取元素的语句会在页面加载完后才执行，就不会出错了。
    <script type="text/javascript">
        window.onload = function(){
            var oDiv = document.getElementById('div1');
            
        }
    </script>
    ...

```
* 操作元素属性

```
获取的页面元素，就可以额对页面元素的属性进行操作，属性的操作包括属性的读和写。
操作属性的方法：
    1. "." 操作
    2. "[]"操作
属性写法：
    1.html的属性和js里面属性写法一样
    2.”class"属性写成“className”
    3.“style” 属性里面的属性，有横杠的改成驼峰式，比如：“font-size",改成"style.fontSize"
    通过"."操作属性：
    
    <script type="text/javascript">
        window.onload = function(){
            var oInput = document.getElementById('input1');
            var oA = document.getElementById('link1');
            //读取属性值
            var val = oInput.value;
            var typ = oInput.type;
            var nam = oInput.name;
            var links = oA.href;
            //写（设置）属性
            oA.style.color = 'red';
            oA.style.fontSize = val;
        }    
    </script>
    ...
    
    <input type="text" name="setsize" id="input1" value="20px">
    <a href="http://baidu.com" id="link1">百度</a>
    
    通过"[]"操作属性：
    
    <script type="text/javascript">
        window.onload = function(){
            var oInput1 = document.getElementById('input1');
            var oInput2 = document.getElementById('input2');
            var oA = document.getElementById('lin1');
            //读取属性
            var val1 = oInput1.value;
            var val2 = oInput2.value;
            //写（设置）属性
            // oA.style.val1 = val2; 没反应
            oA.style[val1] = val2;
        }
    </script>
    
    问题： 如果将oA.style[val1]改为oA.style.val1后；函数就失去作用了，why？
    
        一般情况下我们使用点调用属性的方式，但是当obj的某个属性是一个变量时，这种”."调用就行不通了，变量只能用[]调用。
        
```

* innerHTML

```
 innerHTML 可以读取或者写入标签包裹的内容
 
 <script type="text/javacript">
    window.onload = function(){
        var oDiv = document.getElementById('div1');
        //读取
        var txt = oDiv.innerHTML;
        alert(txt);
        //写入
        oDiv.innerHTML = '<a href="http://baidu.com"> baidu <a/>';
        
        ....
        <div id="div1"> 这是一个div元素</div>
    
    }
 
```

* 函数

```
函数定义与执行：

<script type="text/javascript">
    //函数定义
    function aa(){
        alert('hello!');
    }
    //函数执行
    aa();
</script>

变量与函数预解析
    JavaScript解析过程分为两个阶段，显示编译阶段，然后执行阶段，在编译阶段会将function定义的函数提前，并且将var定义的额变量声明提前，将它赋值为undefined
    
    <script type="text/javascript">
        aa();  //弹出 hello!
        alert(bb); //弹出 undefined
        function aa(){
            alert('hello!');
        }
        var bb = 123;
    </script>
    
提取行事件
    在html行间调用的时间可以提取到javascript中调用，从而做到结构与行行为分离。
    
    <!-- 行间事件调用函数 -->
    <script type=“text/javascript">
        function myalert(){
            alert('ok!');
        }
    </script>
    ....
    <input type="button" name="" value="弹出" onclick="myalert()">
    
    <!-- 提取行间事件  -->
    <script type="text/javascript">
    
        window.onload = function(){
            var oBtn = document.getElementById('btn1');
            oBtn.onclick = myalert;
            function myalert(){
                alert('ok!');
            }
        
        }
    </script>
    ...
    <input type="button" name="" value="弹出" id="btn1">
    
匿名函数

    定义的函数可以不给名称，这个叫匿名函数，可以将匿名函数直接给元素绑定的时间来完成匿名函数的调用。
    <script type="text/javascript">
    
        window.onload = function(){
            var oBtn = document.getElementById('btn1');
            /*
            oBtn.onclick = myalert;
            function myalert(){
                alert('ok!');
            }
            */
            //直接将匿名函数赋值给绑定的事件
            
            oBtn.onclick = function(){
                alert('ok!');
            }
        
        }
    </script>
    
函数传参

    <script type="text/javascript">
    function myalert(a){
        alert(a);
    }
    myalert(12345);
    </script>
    
函数‘return‘关键字
函数中‘return’关键字的作用：
    1.返回函数执行的结果
    2.结束函数的运行
    3.阻止默认行为
    
    <script type="text/javascript">
    function add(a,b){
        var c = a+b;
        return c;
        alert('here!');
    }
    
    var d = add(3,4);
    alert(d);  //弹出7
    </script>
    
```

* 条件语句

```
 if else语句:
 
    var a = 6;
    if (a==1)
    {
        alert('语文‘）；    
    }
    else if(a==2){
    alert('数学');
    }else if(a==3){
    alert('美术');
    }else{
    alert('Null');
    }
    
switch语句:

    switch(a){
        case 1:
            ....
            break;
        case 2:
            ....
            break;
        case 3:
            ....
            break;
        default:
            .... 
    }
```

* 数组及操作方法
    
```
在JavaScript中，数组里面的数据可以是不同类型的。

定义数组的方法：
    //对象的实例创建
    var aList = new Array(1,2,3);
    //直接创建
    var aList2 = [1,2,3,'asd'];
    
操作数组中数据的方法
    1.获取数组的长度：aList.length;
    
        var aList = [1,2,3,4];
        alert(aList.length);  //弹出4
        
    2.用下标操作数组的某个数据：aList[0];
        var aList = [1,2,3,4];
        alert(aList[0]);
    3.join()将数组成员通过一个分隔符合并成字符串
    
        var aList = [1,2,3,4]
        alert(aList.join('-')); //弹出 1-2-3-4
        
    4.push() 和 pop() 从数组最后增加成员或删除成员
    
        var aList = [1,2,3,4]
        aList.push(5);
        alert(aList);  //弹出 1，2，3，4，5
        aList.pop();
        alert(aList); //弹出1，2，3，4
        
    5.unshift()和shift()从数组前面增加成员或者删除成员
    
        var aList = [1,2,3,4];
        aList.unshift(5);
        alert(aList); //弹出 5，1，2，3，4
        aList.shift(aList);
        alert(aList); //弹出1，2，3，4
        
    6.reverse（） 将数组反转
        var aList = [1,2,3,4];
        aList.reverse();
        alert(aList); //弹出 4，3，2，1
        
    7. indexOf() 返回数组中元素第一次出现的索引值
        var aList = [1,2,3,4,1,3,4]
        alert(aList.indexOf(1));
        
    8. splice()在数组中增加或删除成员

        var aList = [1,2,3,4];
        aList.splice(2,1,7,8,9); //从第二个元素开始，删除1个元素，然后在此位置增加’7，8，9‘三个元素
        alert(aList); //弹出 1，2，7，8，9，4
        
多维数组
    多维数组指的是数组的成员也是数组的数组
    
    var aList = [[1,2,3],['a','b','c']];
    alert(aList[0][1]); //弹出2

```

* 获取元素的第二种方法


` document.getElementsByTagName(''),获取的是一个选择集，不是数组，但是可以用下标的方式操作选择集里面的dom元素 `

* 循环语句
```
    程序中进行有规律的重复性操作，用到循环语句。
    
    for 循环
    
        for(var i=0;i<len;i++)
        {
            ...
        }
        
    while 循环
        
        var i = 0;
        while(i<10){
            ...
            i++;
        }

    数组去重
    
        var aList = [1,2,3,4,4,3,2,1,2,3,4,5]
        
        var aList2 = [];
        
        for(var i=0;i<aList.length;i++){
            if(aList.indexOf(aList[i]==i){
                aList2.push(aList[i]);
            }
        
        }
        
        alert(aList2);
```      

## JavaScript组成
    1. ECMAscript JavaScript的语法
    2. DOM文档对象模型，操作html和css的方法
    3. BOM浏览器对象模型 操作浏览器的一些方法

* 字符串处理方法：
    1、字符串合并操作： “+”
    2、parseInt() 将数字字符串转化为整数
    3、parseFloat()将数字字符串转化为小数
    4、split() 把一个字符串分割成字符串组成的数组
    5、charAt() 获取字符串中的某一个字符
    6、indexOf() 查找字符串是否含有某字符
    7、substring() 截取字符串 用法：substring(start,end) (不包括 end）
    8、toUpperCase() 字符串转大写
    9、toLowerCase() 字符串转小写
    
    字符串反转
```
        var str = 'asdfj';
        var str2 = str.split('').reverse().join('');
        alert(str2)
```
        
* 调试方法

    1.alert
    2.console.log
    3.document.title
    
* 定时器

```
   定时器在javascript中的作用
   1.制作动画
   2.异步操作
   3.函数缓冲与节流
   
   定时器类型及语法：
    /*
        定时器：
        setTimeout 只执行一次的定时器
        clearTimeout 关闭只执行一次的定时器
        setInterval 反复执行的定时器
        clearInterval 关闭反复执行的定时器
    */
    
    var time1 = setTimeout(myalert,2000);
    var time2 = setTimeout(myalert,2000);
    /*
    clearTimeout(time1);
    clearTimeout(time2);
    */
    function myalert(){
        alert('ok!');
    }
    
```

* 定时器制作时钟

 ```
    <script type="text/javascript">
        window.onload = function(){
            var oDiv = document.getElementById('div1');
            function timego(){
                var now = new Date();
                var year = now.getFullYear();
                var month = now.getMonth()+1;
                var date = now.getDate();
                var week = now,getDay();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();
                var str = '当前时间是：' + year + '年'+month+'月'+date+'日'+toweek(week)+''+todou(hour)
            oDiv.innerHTML = str;
            }
            timego();
            setInterval(timego,1000);
        }
        
        function toweek(n){
            if (n==0){
                return '星期日';
            }
            else if (n==1){
                return '星期一';
            } else if (n==2){
                return '星期二';
            }
             else if (n==3){
                return '星期三';
            }
             else if (n==4){
                return '星期四';
            }
             else if (n==5){
                return '星期五';
            }
             else{
                return '星期六';
            }
        }
        
        function todou(n){
            if(n<10){
                return '0'+n;
            }else{
                return n;
            }
        }
    </script>
        
    定时器制作倒计时
        
        <script type="text/javascript">
            window.onload = function(){
                var oDiv = document.getElementById('div1');
                function timeleft(){
                    var now = new Date();
                    var future = new Date(2016,8,12,24,0,0);
                    var lefts = parseInt((future-now)/1000);
                    var day = parseInt(lefts/86400);
                    var hour = parseInt(lefts%86400/3600);
                    var min = parseInt(lefts%86400%3600/60);
                    var sec = lefts%60;
                    str = '距离2018年9月12日晚上24点还剩下'+day+'天'+hour+'时'+min+'分'+sec+'秒';
                    oDiv.innerHTML = str;
                    }
                timeleft();
                setInterval(timeleft,1000);
                }
            </script>
            ....
            <div id="div1"></div>
 ```
 
 * 类型转换
 
 ```
  1.直接转换 parseInt() 与 parseFloat()
    alert('12'+7) ; //弹出127
    alert(parseInt('12')+7); //弹出19
    ....
  2.隐式转换 “==”和“-”
  
    if('3'==3)
    {
        alert('相等');
    }
    //弹出 ‘相等’
    alert('10'-3);  //弹出7
    
  3.NaN 和 isNaN
  
    alert（parseInt('123abc')); //弹出123
    alert(parseInt('abc123')); //弹出NAN
 ```

 * 变量作用域
 
    1.全局变量：在函数之外定义的变量，为整个页面公用，函数内部都可以访问。
    2.局部变量：在函数内部定义的变量，只能在定义该变脸的函数的函数内部访问，外部无法访问。

 * 封闭函数
 
 ```
    封闭函数是JavaScript种匿名函数的另外一种写法，创建一个一开始就执行而不用命名的函数。
    一般定义的函数和执行函数：
    
        function changecolor(){
            var oDiv = document.getElementById('div1');
            oDiv.style.color = 'red';
        }
        changecolor();
        
    封闭函数：
        (function(){
            var oDiv = document.getElementById('div1');
            oDiv.style.color = 'red';
        })();
    还可以在函数定义前加上"~"和“！”等符号来定义匿名函数
    !function(){
        var oDiv = doucument.getDocumentById('div1');
        oDiv.style.color = 'red';
    }()
 ```

* 闭包

```
    函数嵌套函数，内部函数可以引用外部函数的参数和变量，参数和变量不会被垃圾回收机制收回
    
    function aaa(a){
        var b = 5;
        function bbb(){
            a++;
            b++;
            alert(a);
            alert(b);
        }
        return bbb;
    }
    var ccc = aaa(2)
    ccc();
    ccc();
    
    改写成封闭函数的形式：
        var ccc = (function(a){
            var b = 5;
            function bbb(){
                a++;
                b++;
                alert(a);
                alert(b);
            }
            return bbb;
        })(2);
        
        ccc();
        ccc();
    
    用处
    1.将一个变量长期驻扎在内存当中，可用于循环中存索引值
    
        <script type="text/javascript">
            window.onload = function(){
                var aLi = document.getElementsByTagName('li');
                for(var i=0;i<aLi.length;i++)
                {
                    (function(i){
                        aLi[i].onclick = function(){
                            alert(i);
                        }
                    })(i);
                
                }
            
            }
        </script>
        ......
        <ul>
            <li>111</li>
            <li>222</li>
            <li>333</li>
            <li>444</li>
            <li>555</li>
        </ul>
        2.私有变量计数器，外部无法访问，避免全局变量的污染
            <script type="text/javascript">
                
                var count = (function(){
                        var a=0;
                        function add(){
                            a++;
                            return a;
                        }
                        return add;
                    })()
                    
                count();
                count();
                var nowcount = count();
                alert(nowcount);
                </script>
                
```

* 内置对象
    
```
1.document
    document.referrer //获取上一个跳转页面的地址（需要服务器环境）
2.location
    window.location.href //获取或者重定url地址
    window.location.search //获取地址参数部分
    window.location.hash //获取页面锚点或者哈希值
3.Math
    Math.random 获取0-1的随机数
    Math.floor 向下取整
    Math.ceil 向上取整
```

* 面向对象
    
    ```
    1.面向过程：所有的工作都是现写现用
    2.面向对象：是一种编程思想，很多功能事先已经编写好了，在使用时，只需要关注功能的运行，而不需要这个功能的具体实现过程。
    
    javascript对象
        将相关的变量和函数组合成一个整体，这个整体叫做对象，对象中的变量叫属性，对象中的函数叫方法。javascript中的对象类似字典
        
    创建对象的方法
    1.单体
    
        <script type="text/javascript">
            var Tom = {
                name:'tom',
                age:18,
                showname:function(){
                    alert('我的名字叫'+this.name);
                },
                showage : function(){
                    alert('我的年龄为：'+this.age);
                },
            }
        </script>
        
    2.工厂模式
    
        <script type="text/javascript">
            function Person(name,age,job){
                var o = new Object();
                o.name = name;
                o.age = age;
                o.job = job;
                o.showname = function(){
                    alert('名字'+this.name);
                };
                o.showage = function(){
                    alert('年龄'+this.age);
                }
                o.showjob = function(){
                    alert('工作'+this.job);
                };
                return o;
            }
            
            var tom = Person('tom','18','程序员');
            tom.showname();
            </script>
            
    3.构造函数
    
        <script type="text/javascript">
            function Person(name,age,job){
                this.name = name;
                this.age = age;
                this.job = job;
                this.showname = function(){
                    alert('我的名字叫'+this.name);
                };
                this.showage = function(){
                    alert('年龄'+this.age);
                };
                this.showjob = function(){
                    alert('工作'+this.job);
                };
            }
            
            var tom = new Person('tom',18,'程序员');
            var jack = new Person('jack',19,'销售');
            alert(tom.showjob==jack.showjob);
            
    4.原型模式
        <script type="text/javascript">
            function Person(name,age,job){
                this.name = name;
                this.age = age;
                this.job = job;
            }
            
            Person.prototype.showname = function(){
                alert('名字'+this.name);
            }
            Person.prototype.showage = function(){
                alert('年龄'+this.age);
            }
            Person.prototype.showjob = function(){
                alert('工作'+this.job);
            }
            
            var tom = new Person('tom',16,'程序员');
            var jack = new Person（’jack',15,'销售');
            alert(tom.showjob==jack.showjob);
        </script>
        
    5.继承
        <script  type="text/javascript">
            function fclass(name,age){
                this.name = name;
                this.age = age;
            }
            fclass.prototype.showname = function(){
                alert(this.name);
            }
            fclass.prototype.showage = function(){
                alert(this.age);
            }
            function sclass(name,age,job)
            {
                fclass.call(this,name,age);
                this.job = job;
            }
            
            sclass.prototype = new fclass();
            sclass.prototype.showjob = function(){
                alert(this.job);
            }
            var tom = new sclass('tom',19,'工程师');
            tom.showname();
            tom.showage();
            tom.showjob();
    ```
    
    * 新选择器
```
    
        1. document.querySlector()
        2. document.querySlectorAll()
```
