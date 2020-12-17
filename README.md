# 异步B站视频下载

## 目录

```bash
|-- spiderFrame
	|-- run.py			# 启动程序
        |-- add_url.py		        # 添加url到redis
	|-- web_server.py		# 网页服务
	|-- parse_.py			# 解析网页
	|-- config.py			# 常量存放位置
	|-- working.json	        # 控制程序启动与停止
	|-- redisConnect.py	        # redis连接
	|-- create_folder.py		# 创建文件夹
	|-- download_scheduler.py	# 视频下载调度
	|-- download_stream_file.py	# 流文件下载
	|-- merge_stream_file.py	# 流文件合成
	|-- ffmpeg			# 视频合成工具
	|-- Download			# 下载文件存放位置
	|-- requirements.txt		# 项目所需模块导出文件
        |-- ImagesFolderReadme          # Readme图片
```





## 思路

**该项目整体思路如下：**

- 首先获取 **url**，并添加到 **redis** (循环操作)，
- 搭建 **web** 服务，用于从 **redis** 中提取 **url**，
- 爬虫程序调度器访问 **web** 服务请求到 **url**，并获取到流文件的详情(大小、链接、名称等)，
- 进而调用程序 `download_stream_file.py` 进行下载，
- 将文件进行分割，以 **10MB** 为单位，即文件有 **100MB**，则分成10个文件来下载，
- 下载完成后将文件进行合并，并删除合并之前的文件。
- 将下载成功和下载失败的 **url** 分别进行数据持久化处理。



---



借助 搭建 **web** 服务来实现多台机器同时抓取，

主要在于：

- 不漏爬，
- 不重爬，
- 多台机器一起爬(不同一片局域网)，
- 通过读取文本形式来决定程序的启动和停止，避免资源浪费，
- 带宽越好，下载速度越快，



## 使用环境

### 安装所需模块

```bash
# 项目中所使用模块及其版本已导出为 requirements.txt文本

# 使用 pip 安装 
pip install -r requirements.txt
```



## 如何使用

在你的电脑上需要启动 **redis** 数据库，如果不懂安装请点击这里：[**Redis** 安装](https://www.runoob.com/redis/redis-install.html)



看到 `working.json` 文件，

-  **stop** 为 **0** 或 **1**，代表程序 `停止` 和 `运行` ，
-  **count** 为 **1** 或 **N**，代表同时跑多少个视频，

```json
{
  "stop": 1,
  "count": 1,
}
```



首先启动 **`add_url.py`**，以确保 有 **url** 可进行请求，

```python
>>> python add_url.py
```

接下来动 **`web_server.py`** ，启动网页服务，

```python
>>> python web_server.py
```

最后启动 **`run.py`** ，开始进行下载。

```python
>>> python run.py
```



现在程序已经运行起来了。



## 运行截图

可参考：[**B站视频** ：https://www.bilibili.com/video/BV1Wz4y1r7jj](https://www.bilibili.com/video/BV1Wz4y1r7jj)

后面再插入



## 已知问题

1. 文件名称不可以包含  **`[?*/\\|.:><]`** 该些字符串，会报错：**Errno 22\] Invalid argument**

2. 同时跑多个视频会报错，问题应该是出在网络上，[Response payload is not completed](https://github.com/aio-libs/aiohttp/issues/2954#)

   ```bash
   # aiohttp作者的回复如下
   
   Everything works fine on my laptop.
   Maybe you have network issues.
   ```

3. ......



## Todo

- ~~**redis** 中没有 **url** 后，休眠一段时间再继续工作，~~
- 对出现的错误进行捕捉并处理，
- 将成功的和失败的 **url** 都存储到 **redis**，
- 从 **redis** 读取失败的 **url** ，进行再次下载，
- 失败的 **url**  再次下载时候，不重复下载之前已经下载过的流文件片段，
- 若是视频有多个分 **P**，下载全部分 **P**，
- 输入 **up主** 的 **id**，下载该 **up主** 的所有视频，
- ......
