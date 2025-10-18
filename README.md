# FISH 2025
A QQ Bot called fish.
## 📕简介
Fish是一个借助NapCat+Onebot框架，以Python语言写就的QQ Bot.

网络通信方面，采用Websocket协议；程序实现方面，通过asyncio实现并发执行。

![](https://cdn.nlark.com/yuque/__mermaid_v3/07e90d081b16d973503548509d75f1bc.svg)

### 不同的需求
如果只需要使用fish现有的功能，可以直接通过私聊或群聊与fish交互。

如果想要将fish部署到本地、开发新功能，或是利用fish的代码简便地实现QQ通信，可以在[https://github.com/549w/fish](https://github.com/549w/fish)获取fish的全部代码，并参考这篇文档进行操作。

> 在交互、部署或开发时遇到任何问题，欢迎与笔者交流。
>

![](https://cdn.nlark.com/yuque/__mermaid_v3/03d829cf7e556badd96f17215897bd33.svg)

## 🐟Fish的代码构成
### `main.py`
这是fish的主程序。

协程`deal_msg()`负责监听消息，并将消息传递给不同的功能函数；

协程`main()`负责初始化，并将`deal_msg()`和不涉及消息接受的功能函数并发执行。

### `settings.json`
fish运行所需的配置信息。

### `.//tools`
这里存放了包含常用函数的程序，比如发送QQ消息、使用语雀API等。

#### `api.py`
这里是与napcat接口通信的各种函数。为了避免不必要的麻烦，函数名均与请求字符串一致，函数的形参也与响应数据中的参数名一致。

### `.//plugins`
这里存放了包含功能函数的程序。

### `.//data`
 这里是各种运行数据，均以json文件的形式存储。它们有些会在运行过程中生成，有些则需要自行建立。

| 文件名 | 相关程序 | 内容 |
| --- | --- | --- |
| `all_tu.json` | `.//plugins//tu.py` | 以列表的形式存放若干图片URL |
| `criteria.json` | `.//plugins//yuque.py` | 以键值对的形式存放用户qq号和所需要文档的描述 |
| `doc_updateTime.json` | `.//plugins//yuque.py` | 以键值对的形式存放语雀`doc_id`和最后一次更新时间 |
| `group_functions.json` | `main.py` | 以键值对的形式存放QQ群号和安静模式的开启与否 |
| `group_list.json` | `main.py` | 以列表的形式存放所有群的详细信息 |
| `record.json` | 各种功能 | 以列表的形式存放每次功能响应的日志 |


## 🔨如何进行本地部署or仅实现QQ通信
1. 参考[https://napneko.github.io/](https://napneko.github.io/)安装NapCat；
2. 在NapCat中配置一个WebSocket服务端，并记下端口号；
3. 在`settings.json`中编辑端口号等信息，如`"port": 3000`；
4. 运行`main.py`or使用`.//tools//api.py`中的函数实现QQ通信。

> ⚠注意：
>
> 笔者尝试将fish部署到云端服务器时，发现NapCat的部分响应数据的结构与本地并不相同。这会导致消息的部分信息无法被正常解析。怀疑是由于不同版本API之间的差异。
>
> 因此，建议在部署时`print`一下msg的具体内容并据此改变解析方式，或避免解析结构相异的数据。
>

## 🔧如何开发功能
以需要接受消息的功能为例。

1. 在`.//plugins`下创建`function.py`；
2. 在`function.py`中定义协程函数，即`async def function(msg):`；
3. 在`function()`中编写功能；

> 关于msg中数据的解析，请参考`.//plugins`中已有代码的写法，诸如`raw_message = msg['raw_message']`；
>

4. 在`main.py`-`deal_msg()`-`while True:`-`相应的if语句`中加入`asyncio.create_task(function(msg))`
5. 运行`main.py`。如果写得自洽，功能就可以使用了。

## 注意事项（开发心得）
