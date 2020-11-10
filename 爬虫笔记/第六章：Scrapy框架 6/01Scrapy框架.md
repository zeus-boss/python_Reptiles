# Scrapy框架：
写一个爬虫，需要做很多的事情。比如：发送网络请求、数据解析、数据存储、反反爬虫机制（更换ip代理、设置请求头等）、异步请求等。这些工作如果每次都要自己从零开始写的话，比较浪费时间。因此Scrapy把一些基础的东西封装好了，在他上面写爬虫可以变的更加的高效（爬取效率和开发效率）。因此真正在公司里，一些上了量的爬虫，都是使用Scrapy框架来解决。


## 安装Scrapy框架：
1. pip install scrapy。
2. 可能会出现问题：
    * 在ubuntu下要先使用以下命令安装依赖包：`sudo apt-get install python3-dev build-essential python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`，安装完成后再安装`scrapy`。
    * 在windows下安装可能会提示`No module named win32api`，这时候先使用命令：`pip install pypiwin32`，安装完成后再安装`scrapy`。
    * 在windows下安装Scrapy可能会提示`twisted`安装失败，那么可以到这个页面下载`twisted`文件：`https://www.lfd.uci.edu/~gohlke/pythonlibs/`，下载的时候要根据自己的Python版本来选择不同的文件。下载完成后，通过`pip install xxx.whl`

## Scrapy框架架构：
1. Scrapy Engine（引擎）：Scrapy框架的核心部分。负责在Spider和ItemPipeline、Downloader、Scheduler中间通信、传递数据等。
2. Spider（爬虫）：发送需要爬取的链接给引擎，最后引擎把其他模块请求回来的数据再发送给爬虫，爬虫就去解析想要的数据。这个部分是我们开发者自己写的，因为要爬取哪些链接，页面中的哪些数据是需要的，都是由程序员自己决定。
3. Scheduler（调度器）：负责接收引擎发送过来的请求，并按照一定的方式进行排列和整理，负责调度请求的顺序等。
4. Downloader（下载器）：负责接收引擎传过来的下载请求，然后去网络上下载对应的数据再交还给引擎。
5. Item Pipeline（管道）：负责将Spider（爬虫）传递过来的数据进行保存。具体保存在哪里，应该看开发者自己的需求。
6. Downloader Middlewares（下载中间件）：可以扩展下载器和引擎之间通信功能的中间件。
7. Spider Middlewares（Spider中间件）：可以扩展引擎和爬虫之间通信功能的中间件。


## 创建Scrapy项目：
1. 创建项目：`scrapy startproject [项目名称]`.
2. 创建爬虫：`cd到项目中->scrapy genspider [爬虫名称] [域名]`.

## 项目文件作用：
1. `settings.py`：用来配置爬虫的。
2. `middlewares.py`：用来定义中间件。
3. `items.py`：用来提前定义好需要下载的数据字段。
4. `pipelines.py`：用来保存数据。
5. `scrapy.cfg`：用来配置项目的。


## CrawlSpider爬虫：
1. 作用：可以定义规则，让Scrapy自动的去爬取我们想要的链接。而不必跟Spider类一样，手动的yield Request。
2. 创建：scrapy genspider -t crawl [爬虫名] [域名]
3. 提取的两个类：
    * LinkExtrator：用来定义需要爬取的url规则。
    * Rule：用来定义这个url爬取后的处理方式，比如是否需要跟进，是否需要执行回调函数等。

## Scrapy Shell：
在命令行中，进入到项目所在的路径。然后：
`scrapy shell 链接`
在这个里面，可以先去写提取的规则，没有问题后，就可以把代码拷贝到项目中。方便写代码。

## 使用twisted异步保存mysql数据：
1. 使用twisted.enterprise.adbapi来创建一个连接对象：
    ```python
    def __init__(self,mysql_config):
        self.dbpool = adbapi.ConnectionPool(
            mysql_config['DRIVER'],
            host=mysql_config['HOST'],
            port=mysql_config['PORT'],
            user=mysql_config['USER'],
            password=mysql_config['PASSWORD'],
            db=mysql_config['DATABASE'],
            charset='utf8'
        )

    @classmethod
    def from_crawler(cls,crawler):
        # 只要重写了from_crawler方法，那么以后创建对象的时候，就会调用这个方法来获取pipline对象
        mysql_config = crawler.settings['MYSQL_CONFIG']
        return cls(mysql_config)
    ```
2. 在插入数据的函数中，使用`runInteraction`来运行真正执行sql语句的函数。示例代码如下：
    ```python
    def process_item(self, item, spider):
        # runInteraction中除了传运行sql的函数，还可以传递参数给回调函数使用
        result = self.dbpool.runInteraction(self.insert_item,item)
        # 如果出现了错误，会执行self.insert_error函数
        result.addErrback(self.insert_error)
        return item

    def insert_item(self,cursor,item):
        sql = "insert into article(id,title,author,pub_time,content,origin) values(null,%s,%s,%s,%s,%s)"
        args = (item['title'],item['author'],item['pub_time'],item['content'],item['origin'])
        cursor.execute(sql,args)

    def insert_error(self,failure):
        print("="*30)
        print(failure)
        print("="*30)
    ```

## Scrapy下载图片：
1. 解析图片的链接。
2. 定义一个item，上面有两个字段，一个是image_urls，一个是images。其中image_urls是用来存储图片的链接，由开发者把数据爬取下来后添加的。
3. 使用scrapy.pipelines.images.ImagesPipeline来作为数据保存的pipeline。
4. 在settings.py中设置IMAGES_SOTRE来定义图片下载的路径。
5. 如果想要有更复杂的图片保存的路径需求，可以重写ImagePipeline的file_path方法，这个方法用来返回每个图片的保存路径。
6. 而`file_path`方法没有`item`对象，所以我们还需要重写`get_media_requests`方法，来把`item`绑定到`request`上。示例代码如下：
    ```python
    class ImagedownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        media_requests = super(ImagedownloadPipeline, self).get_media_requests(item,info)
        for media_request in media_requests:
            media_request.item = item
        return media_requests


    def file_path(self, request, response=None, info=None):
        origin_path = super(ImagedownloadPipeline, self).file_path(request,response,info)
        title = request.item['title']
        title = re.sub(r'[\\/:\*\?"<>\|]',"",title)
        save_path = os.path.join(settings.IMAGES_STORE,title)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        image_name = origin_path.replace("full/","")
        return os.path.join(save_path,image_name)
    ```
7. 在创建文件夹的时候，要注意一些特殊字符是不允许作为文件夹的名字而存在的，那么我们就可以通过正则表达式来删掉。`r'[\\/:\*\?"<>\|]'`。


## 下载器中间件：
下载器中间件是引擎和下载器之间通信的中间件。在这个中间件中我们可以设置代理、更换请求头等来达到反反爬虫的目的。要写下载器中间件，可以在下载器中实现两个方法。一个是process_request(self,request,spider)，这个方法是在请求发送之前会执行，还有一个是process_response(self,request,response,spider)，这个方法是数据下载到引擎之前执行。

1. process_request(self,request,spider)方法：
    这个方法是下载器在发送请求之前会执行的。一般可以在这个里面设置随机代理ip等。
    1. 参数：
        * request：发送请求的request对象。
        * spider：发送请求的spider对象。
    2. 返回值：
        * 返回None：如果返回None，Scrapy将继续处理该request，执行其他中间件中的相应方法，直到合适的下载器处理函数被调用。
        * 返回Response对象：Scrapy将不会调用任何其他的process_request方法，将直接返回这个response对象。已经激活的中间件的process_response()方法则会在每个response返回时被调用。
        * 返回Request对象：不再使用之前的request对象去下载数据，而是根据现在返回的request对象返回数据。
        * 如果这个方法中抛出了异常，则会调用process_exception方法。

2. process_response(self,request,response,spider)方法：
    这个是下载器下载的数据到引擎中间会执行的方法。
    1. 参数：
        * request：request对象。
        * response：被处理的response对象。
        * spider：spider对象。
    2. 返回值：
        * 返回Response对象：会将这个新的response对象传给其他中间件，最终传给爬虫。
        * 返回Request对象：下载器链被切断，返回的request会重新被下载器调度下载。
        * 如果抛出一个异常，那么调用request的errback方法，如果没有指定这个方法，那么会抛出一个异常。

## Scrapy中设置代理：
1. 设置普通代理：
    ```python
    class IPProxyDownloadMiddleware(object):
        PROXIES = [
         "5.196.189.50:8080",
        ]
        def process_request(self,request,spider):
            proxy = random.choice(self.PROXIES)
            print('被选中的代理：%s' % proxy)
            request.meta['proxy'] = "http://" + proxy
    ```
2. 设置独享代理：
    ```python
    class IPProxyDownloadMiddleware(object):
        def process_request(self,request,spider):
            proxy = '121.199.6.124:16816'
            user_password = "970138074:rcdj35xx"
            request.meta['proxy'] = proxy
            # bytes
            b64_user_password = base64.b64encode(user_password.encode('utf-8'))
            request.headers['Proxy-Authorization'] = 'Basic ' + b64_user_password.decode('utf-8')
    ```

3. 代理服务商：
    * 芝麻代理：http://http.zhimaruanjian.com/
    * 太阳代理：http://http.taiyangruanjian.com/
    * 快代理：http://www.kuaidaili.com/
    * 讯代理：http://www.xdaili.cn/
    * 蚂蚁代理：http://www.mayidaili.com/
    * 极光代理：http://www.jiguangdaili.com/


### 分布式爬虫：

#### redis配置：
1. 在ubuntu上安装redis：sudo apt install redis-server
2. 连接reids服务器：redis-cli -h [ip地址] -p [端口号]
3. 在其他电脑上连接本机的redis服务器：在/etc/redis/redis.conf中，修改bind，把redis服务器的ip地址加进去。示例如下：
    ```shell
    bind 192.168.175.129 127.0.0.1
    ```
4. vim：有可能没有。那么通过sudo apt install vim就可以安装了。
5. 虚拟机安装：vmware+ubuntu16.04.iso来安装。安装的时候，设置root用户的密码，用`useradd`命令来创建一个普通用户。后期方便通过xshell来连接。ubuntu不允许外面直接用root用户链接，那么我们可以先用普通用户连接，然后再切换到root用户。


### 爬虫部署：
1. 在服务器上安装scrapyd：`pip3 install scrapyd`。
2. 从`/usr/local/lib/python3.5/dist-packages/scrapyd`下拷贝出`default_scrapyd.conf`放到`/etc/scrapyd/scrapyd.conf`。
3. 修改`/etc/scrapyd/scrapyd.conf`中的`bind_address`为自己的IP地址。
4. 重新安装`twisted`：
    ```
    pip uninstall twisted
    pip install twisted==18.9.0
    ```
    如果这一步不做，后期会出现intxxx的错误。
4. 在开发机上（自己的window电脑上）安装`pip install scrapyd-client`。
5. 修改`python/Script/scrapyd-deploy`为`scrapyd-deploy.py`
6. 在项目中，找到`scrapy.cfg`，然后配置如下：
    ```python
    [settings]
    default = lianjia.settings

    [deploy]
    # 下面这个url要取消注释
    url = http://服务器的IP地址:6800/
    project = lianjia
    ```
7. 在项目所在的路径执行命令生成版本号并上传爬虫代码：`scrapyd-deploy`。如果一次性想要把代码上传到多个服务器，那么可以修改`scrapy.cfg`为如下：
    ```python
    [settings]
    default = lianjia.settings

    [deploy:服务器1]
    # 下面这个url要取消注释
    url = http://服务器1的IP地址:6800/
    project = lianjia

    [deploy:服务器2]
    # 下面这个url要取消注释
    url = http://服务器2的IP地址:6800/
    project = lianjia
    ```
    然后使用`scrapyd-deploy -a`就可以全部上传了。
8. curl for windows下载地址：`https://curl.haxx.se/windows/`，解压后双击打开bin/curl.exe即可在cmd中使用了。
9. 在cmd中使用命令运行爬虫：
    ```
    curl http://服务器IP地址:6800/schedule.json -d project=lianjia -d spider=house
    ```
10. 如果后期修改了爬虫的代码，那么需要重新部署，然后服务器的scrapyd服务重新启动一下。
11. 更多的API介绍：https://scrapyd.readthedocs.io/en/stable/api.html

