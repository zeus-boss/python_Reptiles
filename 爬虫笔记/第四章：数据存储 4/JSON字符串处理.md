# JSON字符串处理：

## 什么是JSON字符串：
JSON(JavaScript Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。它基于 ECMAScript (w3c制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。更多解释请见：https://baike.baidu.com/item/JSON/2462549?fr=aladdin
JSON支持数据格式：
对象（字典）：使用花括号。
数组（列表）：使用方括号。
字符串类型：字符串必须要用双引号，不能用单引号）。
整形、浮点型、布尔类型还有null类型。
多个数据之间使用逗号分开。
**注意：json本质上就是一个字符串。**


## 将Python对象dump成JSON字符串：
1. dumps：把Python对象转换成JSON格式的字符串。
2. dump：把Python对象转换成JSON格式的字符串，并且还可以接收一个文件指针fp参数，可以写入到文件中。

这两个方法都有一个`ensure_ascii`参数，默认情况下这个参数的值是True，也就是说转换后的JSON字符串是只能存储ascii格式的，不能存储中文，如果想要存储成中文，那么可以将他设置为False。


## 将JSON字符串load成Python对象：
1. loads：将JSON字符串转换成Python对象。
2. load：将JSON字符串转换成Python对象，并且是直接从文件中获取JSON字符串。
