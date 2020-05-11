---
title: requests源码之status_codes.py
date: 2019-09-10 09:58:11
tags: [Python, requests]
category: Python


---

## Requests 包里的文件

```python
__init__.py
__version__.py
_internal_utils.py
adapters.py
api.py
auth.py
certs.py
compat.py
cookies.py
exception.py
help.py
hooks.py
models.py
packages.py
sessions.py
status_codes.py
structures.py
utils.py

# 一共 18 个文件
```

接下来，我们可以写一条 requests 请求某个 url 来查看其中的架构：

比如写一句：

```python
requests.get('http://baidu.com')
```

进入 get 方法内，发现此时的文件为 api.py

首先观察一下 api.py 里面的方法有:

```python
def request(method, url, **kwargs):

def get(url, params=None, **kwargs):
      r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)

def options(url, **kwargs):

def head(url, **kwargs):

def post(url, data=None, json=None, **kwargs):

def put(url, data=None, **kwargs):

def patch(url, data=None, **kwargs):

def delete(url, **kwargs):

```

了解 http ，就可以看得出来这些方法都是 http 的基本方法，除了 request 方法，这个方法接收一个自定义的 method。

没错，这个文件的名称就像其文件名一样， 都是 api ，给人一种清爽的感觉。

在做一件事情的时候，各个文件中的代码，各自负责各自所擅长的领域。而不至于全部代码都写在一起。这里的 api 每个函数都使用了 \*\*kwargs 参数，并且会使用  kwargs.setdefault('allow_redirects', True) 来进行赋值，然后传递给下层函数。其他方法通过简单的封装，最后全部都是调用 def request(method, url, **kwargs): 方法来进行后来的操作。

```python
# api.py
def request(method, url, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)
      
# sessions.py
class Session(SessionRedirectMixin):
    def request(self, method, url,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        # Create the Request.
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {
            'timeout': timeout,
            'allow_redirects': allow_redirects,
        }
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        return resp
      
```

这个函数主要做的事情就是 创建会话对象，然后将参数拼装完成，然后调用 send 方法发送，然后返回 response 。

其中会 首先调用一个 Request 类，对请求的参数进行处理，这里应该还是属于处理 request 参数的层级，然后调用 self.prepare_request(req) 继续处理参数，而这里处理的级别属于 session 层，如果两者写在一起，那肯定看着就不是这么清爽了。处理完之后，就会进行接下来的一些共同的设置内容，紧接着就进行了 send 发送请求，接下来的事情暂且不说。

总结一下发送一个 get 请求的流程：

1. 对于requests 的 api 方法，其中又很多是可选参数，面对多种方法，它提供了具体的 get、post、head 等方法，方便了编程，并不是只提供一个 request(method, url, **kwargs) 方法。做了一层封装后，最后请求还是会调用 request 方法进行后续处理

2. 从 get、post 具体的方法进入 request 方法后，开始构建 session 处理，而 session 这里通过 with 语句可以避免在request 执行完后，忘记关闭资源，导致存在资源占用问题。将参数继续传递给 session 进行构建。

3. 在session的 request 方法中，它会先调用 Request 类生成 Request 对象继续完成Request 的必要初始化，然后继续调用属于 session 范畴的初始化 self.prepare_request(req) 。

4. 等 Request 范畴和 Session 范畴的工作都做完后，就进行 settings = self.merge_environment_settings() 的设置内容，然后设置发送的参数，然后所有的准备工作都做好了。

5. 通过具体的 self.send 方法进行发送请求，而具体 send 如何实现的，就属于比较底层的事情了，稍后在研究。

   

   





会话对象，向同一主机发送多个请求，底层TCP连接将会被重用，从而带来显著的性能提升。



### 请求与响应对象

任何时候进行了类似 requests.get() 的调用，你都在做两件主要的事情，其一，你在构建一个 Request 对象，该对象将被发送到某个服务器请求或查询一些资源。其二，一旦 requests 得到一个从服务器返回的响应就会产生一个 Response 对象。该响应对象包含服务器返回的所有信息，也包含你原来创建的 Request 对象。

如

response.request.headers

可以获取到 原 request 的属性



### 准备的请求

当你从 API 或者会话调用中收到一个 Response 对象时， request 属性其实是使用了 PreparedRequest。 有时在发送请求之前，你需要对 body 或者 header（或者别的什么东西）做一些额外的处理。

由于你没有对 `Request` 对象做什么特殊事情，你立即准备和修改了 `PreparedRequest` 对象，然后把它和别的参数一起发送到 `requests.*` 或者 `Session.*`。

```python
from requests import Request, Session

s = Session()
req = Request('GET', url,
    data=data,
    headers=header
)
prepped = req.prepare()

# do something with prepped.body
# do something with prepped.headers

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```

然而，上述代码会失去 Requests [`Session`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Session) 对象的一些优势， 尤其 [`Session`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Session) 级别的状态，例如 cookie 就不会被应用到你的请求上去。要获取一个带有状态的 [`PreparedRequest`](https://2.python-requests.org//zh_CN/latest/api.html#requests.PreparedRequest)， 请用 [`Session.prepare_request()`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Session.prepare_request) 取代 [`Request.prepare()`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Request.prepare) 的调用，如下所示：

```python
from requests import Request, Session

s = Session()
req = Request('GET',  url,
    data=data
    headers=headers
)

prepped = s.prepare_request(req)

# do something with prepped.body
# do something with prepped.headers

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)

print(resp.status_code)
```

区别就是将

prepped = req.prepare()

换成

prepped = s.prepare_request(req)

就拥有了Session 级别的状态，例如  cookie。



## SSL 证书验证

Request 可以为 HTTPS 请求验证 SSL 证书，就像 web 浏览器一样。SSL 验证默认是开启的，如果证书验证失败，Requests 会抛出 SSLError 。

通俗来说，就是 Requests 可以保证我们在访问 https 网站的时候，会主动对网站的 真实性就行校验，如果不通过就会抛出异常。与下面的客户端证书是不同的。



## 客户端证书

你也可以指定一个本地证书用作客户端证书，可以是单个文件（包含秘钥和证书）或一个包含两个文件路径的元祖。

比如在某些需要客户端证书的系统中，就可以通过手动指定客户端证书位置来完成请求。



## CA证书

注意： Requests 默认附带了一套它信任的根证书，来自于 [Mozilla trust store](https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt)。然而它们在每次 Requests 更新时才会更新。这意味着如果你固定使用某一版本的 Requests，你的证书有可能已经 太旧了。

从 Requests 2.4.0 版之后，如果系统中装了 [certifi](http://certifi.io/) 包，Requests 会试图使用它里边的 证书。这样用户就可以在不修改代码的情况下更新他们的可信任证书。

为了安全起见，我们建议你经常更新 certifi！



## 响应体内容流

默认情况下，当你进行网络请求后，响应体会立即被下载。你可以通过 `stream` 参数覆盖这个行为，推迟下载响应体直到访问 [`Response.content`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Response.content) 属性：

```
tarball_url = 'https://github.com/kennethreitz/requests/tarball/master'
r = requests.get(tarball_url, stream=True)
```

此时仅有响应头被下载下来了，连接保持打开状态，因此允许我们根据条件获取内容：

```
if int(r.headers['content-length']) < TOO_LONG:
  content = r.content
  ...
```

你可以进一步使用 [`Response.iter_content`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Response.iter_content) 和 [`Response.iter_lines`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Response.iter_lines) 方法来控制工作流，或者以 [`Response.raw`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Response.raw) 从底层 urllib3 的 `urllib3.HTTPResponse <urllib3.response.HTTPResponse` 读取未解码的响应体。

*如果你在请求中把 `stream` 设为 `True`，Requests 无法将连接释放回连接池，除非你 消耗了所有的数据，或者调用了 [`Response.close`](https://2.python-requests.org//zh_CN/latest/api.html#requests.Response.close)。 这样会带来连接效率低下的问题。如果你发现你在使用 `stream=True` 的同时还在部分读取请求的 body（或者完全没有读取 body），那么你就应该考虑使用 with 语句发送请求，这样可以保证请求一定会被关闭：*

```python
with requests.get('http://httpbin.org/get', stream=True) as r:
    # 在此处理响应。
```

## 保持活动状态（持久连接）

好消息——归功于 urllib3，同一会话内的持久连接是完全自动处理的！同一会话内你发出的任何请求都会自动复用恰当的连接！

注意：只有所有的响应体数据被读取完毕连接才会被释放为连接池；所以确保将 `stream` 设置为 `False` 或读取 `Response` 对象的 `content` 属性。



## 流式上传

Requests支持流式上传，这允许你发送大的数据流或文件而无需先把它们读入内存。要使用流式上传，仅需为你的请求体提供一个类文件对象即可：

```
with open('massive-body') as f:
    requests.post('http://some.url/streamed', data=f)
```

警告

警告

我们强烈建议你用二进制模式（[binary mode](https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files)）打开文件。这是因为 requests 可能会为你提供 header 中的 `Content-Length`，在这种情况下该值会被设为文件的**字节数**。如果你用**文本模式**打开文件，就可能碰到错误。

## 事件挂钩

Requests有一个钩子系统，你可以用来操控部分请求过程，或信号事件处理。

可用的钩子:

- `response`:

  从一个请求产生的响应

你可以通过传递一个 `{hook_name: callback_function}` 字典给 `hooks` 请求参数为每个请求分配一个钩子函数：

```
hooks=dict(response=print_url)
```

`callback_function` 会接受一个数据块作为它的第一个参数。

```
def print_url(r, *args, **kwargs):
    print(r.url)
```

若执行你的回调函数期间发生错误，系统会给出一个警告。

若回调函数返回一个值，默认以该值替换传进来的数据。若函数未返回任何东西，也没有什么其他的影响。

我们来在运行期间打印一些请求方法的参数：

```python
>>> requests.get('http://httpbin.org', hooks=dict(response=print_url))
http://httpbin.org
<Response [200]>
```