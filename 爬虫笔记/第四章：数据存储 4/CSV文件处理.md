# CSV文件处理：


## CSV文件读取的两种方式：
```python
import csv

# 这种方式读取到的每一条数据是一个列表，所以需要通过下标的方式获取具体某一个值
# with open("stock.csv",'r',encoding='gbk') as fp:
#     reader = csv.reader(fp)
#     for x in reader:
#         print(x[3])

# 这种方式读取到的每一条数据是一个字典，所以可以通过列名获取数据
with open("stock.csv",'r',encoding='gbk') as fp:
    reader = csv.DictReader(fp)
    for x in reader:
        print(x['secShortName'])
```


## CSV文件的写入的两种方式：
```python
import csv

headers = ('name','age','height')
# students = [
#     ("张三",18,180),
#     ("李四",19,190),
#     ("王五",20,170)
# ]
students = [
    {"name":"张三","age":18,"height":180},
    {"name":"李四","age":19,"height":190},
    {"name":"王五","age":20,"height":170}
]

# with open("students.csv",'w',encoding='utf-8',newline='') as fp:
#     writer = csv.writer(fp)
#     writer.writerow(headers)
#     writer.writerows(students)


with open("students.csv",'w',encoding='utf-8',newline='') as fp:
    writer = csv.DictWriter(fp,headers)
    # 虽然DictWriter创建的时候有一个headers，但是想要写入数据进去，还是需要调用
    # writer.writeheader()方法，否则，表头数据写入不进去
    writer.writeheader()
    writer.writerows(students)
```