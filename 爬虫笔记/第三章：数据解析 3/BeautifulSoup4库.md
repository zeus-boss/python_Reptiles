# BeautifulSoup4库

和 lxml 一样，Beautiful Soup 也是一个HTML/XML的解析器，主要的功能也是如何解析和提取 HTML/XML 数据。



## 安装和文档：

安装：
pip install bs4

中文文档：https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

## 几大解析工具对比：

![1554888897765](C:\Users\HP\AppData\Roaming\Typora\typora-user-images\1554888897765.png)

## 简单使用：

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html,'lxml')
print(soup.prettify())
```

## 常见的四种对象：

1. Tag：BeautifulSoup中所有的标签都是Tag类型，并且BeautifulSoup的对象其实本质上也是一个Tag类型。所以其实一些方法比如find、find_all并不是BeautifulSoup的，而是Tag的。
2. NavigableString：继承自python中的str，用起来就跟使用python的str是一样的。
3. BeautifulSoup：继承自Tag。用来生成BeaufifulSoup树的。对于一些查找方法，比如find、select这些，其实还是Tag的。
4. Comment：这个也没什么好说，就是继承自NavigableString。

## contents和children：

返回某个标签下的直接子元素，其中也包括字符串。他们两的区别是：contents返回来的是一个列表，children返回的是一个迭代器。

## string和strings、stripped_strings属性以及get_text方法

1. string：获取某个标签下的非标签字符串。返回来的是个字符串。如果这个标签下有多行字符，那么就不能获取到了。
2. strings：获取某个标签下的子孙非标签字符串。返回来的是个生成器。
3. stripped_strings：获取某个标签下的子孙非标签字符串，会去掉空白字符。返回来的是个生成器。
4. get_text：获取某个标签下的子孙非标签字符串，以普通字符串形式返回

## find_all的使用：

1. 在提取标签的时候，第一个参数是标签的名字。然后如果在提取标签的时候想要使用标签属性进行过滤，那么可以在这个方法中通过关键字参数的形式，将属性的名字以及对应的值传进去。或者是使用`attrs`属性，将所有的属性以及对应的值放在一个字典中传给`attrs`属性。
2. 有些时候，在提取标签的时候，不想提取那么多，那么可以使用`limit`参数。限制提取多少个。

## find与find_all的区别：

1. find：找到第一个满足条件的标签就返回。说白了，就是只会返回一个元素。
2. find_all:将所有满足条件的标签都返回。说白了，会返回很多标签（以列表的形式）。

## 使用find和find_all的过滤条件：

1. 关键字参数：将属性的名字作为关键字参数的名字，以及属性的值作为关键字参数的值进行过滤。
2. attrs参数：将属性条件放到一个字典中，传给attrs参数。

## 获取标签的属性：

1. 通过下标获取：通过标签的下标的方式。

   ```python
   href = a['href']
   ```

2. 通过attrs属性获取：示例代码：

   ```python
   href = a.attrs['href']
   ```



## CSS选择器：

### select方法：

使用以上方法可以方便的找出元素。但有时候使用`css`选择器的方式可以更加的方便。使用`css`选择器的语法，应该使用`select`方法。以下列出几种常用的`css`选择器方法：

#### （1）通过标签名查找：

```python
print(soup.select('a'))
```

#### （2）通过类名查找：

通过类名，则应该在类的前面加一个`.`。比如要查找`class=sister`的标签。示例代码如下：

```python
print(soup.select('.sister'))
```

#### （3）通过id查找：

通过id查找，应该在id的名字前面加一个＃号。示例代码如下：

```python
print(soup.select("#link1"))
```

#### （4）组合查找：

组合查找即和写 class 文件时，标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，二者需要用空格分开：

```python
print(soup.select("p #link1"))
```

直接子标签查找，则使用 > 分隔：

```python
print(soup.select("head > title"))
```

#### （5）通过属性查找：

查找时还可以加入属性元素，属性需要用中括号括起来，注意属性和标签属于同一节点，所以中间不能加空格，否则会无法匹配到。示例代码如下：

```python
print(soup.select('a[href="http://example.com/elsie"]'))
```

#### （6）获取内容

以上的 select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text() 方法来获取它的内容。

```python
soup = BeautifulSoup(html, 'lxml')
print(type(soup.select('title')))
print(soup.select('title')[0].get_text())

for title in soup.select('title'):
    print(title.get_text())
```