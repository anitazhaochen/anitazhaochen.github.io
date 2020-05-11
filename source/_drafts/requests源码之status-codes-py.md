---
title: requests源码之status_codes.py
date: 2019-11-08 09:58:11
tags: [Python, requests]
category: Python

---





```python

# -*- coding: utf-8 -*-

r"""
The ``codes`` object defines a mapping from common names for HTTP statuses
to their numerical codes, accessible either as attributes or as dictionary
items.

>>> requests.codes['temporary_redirect']
307
>>> requests.codes.teapot
418
>>> requests.codes['\o/']
200

Some codes have multiple names, and both upper- and lower-case versions of
the names are allowed. For example, ``codes.ok``, ``codes.OK``, and
``codes.okay`` all correspond to the HTTP status code 200.
"""

from .structures import LookupDict

_codes = {

    # Informational.
    100: ('continue',),
    101: ('switching_protocols',),
    102: ('processing',),
    103: ('checkpoint',),
    122: ('uri_too_long', 'request_uri_too_long'),
    200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
    201: ('created',),
    202: ('accepted',),
    203: ('non_authoritative_info', 'non_authoritative_information'),
    204: ('no_content',),
    205: ('reset_content', 'reset'),
    206: ('partial_content', 'partial'),
    207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
    208: ('already_reported',),
    226: ('im_used',),

    # Redirection.
    300: ('multiple_choices',),
    301: ('moved_permanently', 'moved', '\\o-'),
    302: ('found',),
    303: ('see_other', 'other'),
    304: ('not_modified',),
    305: ('use_proxy',),
    306: ('switch_proxy',),
    307: ('temporary_redirect', 'temporary_moved', 'temporary'),
    308: ('permanent_redirect',
          'resume_incomplete', 'resume',),  # These 2 to be removed in 3.0

    # Client Error.
    400: ('bad_request', 'bad'),
    401: ('unauthorized',),
    402: ('payment_required', 'payment'),
    403: ('forbidden',),
    404: ('not_found', '-o-'),
    405: ('method_not_allowed', 'not_allowed'),
    406: ('not_acceptable',),
    407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
    408: ('request_timeout', 'timeout'),
    409: ('conflict',),
    410: ('gone',),
    411: ('length_required',),
    412: ('precondition_failed', 'precondition'),
    413: ('request_entity_too_large',),
    414: ('request_uri_too_large',),
    415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
    416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
    417: ('expectation_failed',),
    418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
    421: ('misdirected_request',),
    422: ('unprocessable_entity', 'unprocessable'),
    423: ('locked',),
    424: ('failed_dependency', 'dependency'),
    425: ('unordered_collection', 'unordered'),
    426: ('upgrade_required', 'upgrade'),
    428: ('precondition_required', 'precondition'),
    429: ('too_many_requests', 'too_many'),
    431: ('header_fields_too_large', 'fields_too_large'),
    444: ('no_response', 'none'),
    449: ('retry_with', 'retry'),
    450: ('blocked_by_windows_parental_controls', 'parental_controls'),
    451: ('unavailable_for_legal_reasons', 'legal_reasons'),
    499: ('client_closed_request',),

    # Server Error.
    500: ('internal_server_error', 'server_error', '/o\\', '✗'),
    501: ('not_implemented',),
    502: ('bad_gateway',),
    503: ('service_unavailable', 'unavailable'),
    504: ('gateway_timeout',),
    505: ('http_version_not_supported', 'http_version'),
    506: ('variant_also_negotiates',),
    507: ('insufficient_storage',),
    509: ('bandwidth_limit_exceeded', 'bandwidth'),
    510: ('not_extended',),
    511: ('network_authentication_required', 'network_auth', 'network_authentication'),
}

codes = LookupDict(name='status_codes')

def _init():
    for code, titles in _codes.items():
        for title in titles:
            setattr(codes, title, code)
            if not title.startswith(('\\', '/')):
                setattr(codes, title.upper(), code)

    def doc(code):
        names = ', '.join('``%s``' % n for n in _codes[code])
        return '* %d: %s' % (code, names)

    global __doc__
    __doc__ = (__doc__ + '\n' +
               '\n'.join(doc(code) for code in sorted(_codes))
               if __doc__ is not None else None)


_init()

```

在 requests 源码中，status_codes.py 文件中，主要是完成了 http 的一些异常码处理。

在平时的工作之中，自己开发平台，提供 api 供给别人使用，当别人没有提供给 api 必要的参数导致程序运行异常的时候，就需要返回一个错误码。

在本文件中， 通过 "_" 开头的 "\_codes" 字典， 表示一个保护成员，只有类对象和子类对象自己能访问到这些变量。使用 from module import * 时不会被获取，但是使用 import module 可以获取。



“\_code” 通过 {key（数字）： value（元祖）  }  的形式来进行存储，当一个状态码可能表示多种信息时，就显得非常有用。



其中 LookupDict 源码：

```python
class LookupDict(dict):
    """Dictionary lookup object."""

    def __init__(self, name=None):
        self.name = name
        super(LookupDict, self).__init__()

    def __repr__(self):
        return '<lookup \'%s\'>' % (self.name)

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None

        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

```

这个函数我觉得主要实现的就是封装了原来的字典，如果获取一个不存在的键的时候，会默认返回 None 。

其中    def \_\_repr\_\_() 函数的作用在直接通过 print 函数打印对象的时候，会显示 此函数的返回信息。跟这个相似的还有  def \_\_str\_\_() 函数，这个函数也是在打印对象的时候打印其返回的信息。这两个函数的不同之处在于， 如果 通过 print 输出这个类的对象， Python 首先会去尝试使用 \_\_str\_\_ 方法，如果没有定义，就会去使用 \_\_repr\_\_ 方法。

在交互式环境中，区别如下：

```python
a = new A() # A 类重构了 __str__ 和 __repr__ 方法的前提下
a  # 输出 的是 __repr__ 中的返回
print(a)  # 输出的是 __str__ 中的返回

```





而这里，LookupDict 通过继承dict类，然后初始化参数可以传递一个名称，这里定义了 \_\_repr\_\_ 方法作用是比如输出这个 codes 对象，会得到如下输出:

```python
<lookup 'status_codes'>
```

我觉得这样做的好处应该可以使 codes 的 错误码，和具体的展示类来 解耦分隔开来，比如需要另一套 codes api 异常码，我们在不改动任何代码的情况下，依旧可以直接使用 LookupDict 。



\_\_getitem\_\_ 实现的是一个对象可以使用 [] 来取值，这里进行了封装，直接使用原始dict 如果值不存在，则会报错，这里不存在会返回默认的 None。

 

接下来是一个 \_\_init\_\_() 方法，主要做的工作是对 _codes 进行解析，将 \_codes 中键对应的值存储为 key， 这样就可以在需要的时候，方便的找到对应的 状态码，即通过值找键 。

如：

```python
print(codes['not_found'])  # 输出 404
```



下面是输出 \_\_doc\_\_

```python
Some codes have multiple names, and both upper- and lower-case versions of
the names are allowed. For example, ``codes.ok``, ``codes.OK``, and
``codes.okay`` all correspond to the HTTP status code 200.

* 100: ``continue``
* 101: ``switching_protocols``
* 102: ``processing``
* 103: ``checkpoint``
* 122: ``uri_too_long``, ``request_uri_too_long``
* 200: ``ok``, ``okay``, ``all_ok``, ``all_okay``, ``all_good``, ``\o/``, ``✓``
* 201: ``created``
* 202: ``accepted``
* 203: ``non_authoritative_info``, ``non_authoritative_information``
* 204: ``no_content``
* 205: ``reset_content``, ``reset``
* 206: ``partial_content``, ``partial``
```



