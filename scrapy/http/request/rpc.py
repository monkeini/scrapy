"""
This module implements the XmlRpcRequest class which is a more convenient class
(that Request) to generate xml-rpc requests.

See documentation in docs/topics/request-response.rst
"""
import xmlrpclib

from scrapy.http.request import Request
from scrapy.utils.python import get_func_args
from scrapy.utils.py26 import json

DUMPS_ARGS = get_func_args(xmlrpclib.dumps)


class XmlRpcRequest(Request):

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        encoding = kwargs.get('encoding', None)
        if 'body' not in kwargs and 'params' in kwargs:
            kw = dict((k, kwargs.pop(k)) for k in DUMPS_ARGS if k in kwargs)
            kwargs['body'] = xmlrpclib.dumps(**kw)

        # spec defines that requests must use POST method
        kwargs.setdefault('method', 'POST')

        # xmlrpc query multiples times over the same url
        kwargs.setdefault('dont_filter', True)

        # restore encoding
        if encoding is not None:
            kwargs['encoding'] = encoding

        super(XmlRpcRequest, self).__init__(*args, **kwargs)
        self.headers.setdefault('Content-Type', 'text/xml')


class JsonRpcRequest(Request):

    __slots__ = ('rpc_method',)

    def __init__(self, *args, **kwargs):
        req_params = None
        self.rpc_method = ""
        if 'body' not in kwargs and 'rpc_params' in kwargs:
            self.rpc_method = kwargs.pop('rpc_method')
            req_params = {'jsonrpc': '2.0',
                          'method': self.rpc_method,
                          'params': kwargs.pop("rpc_params"),
                          'id': 1}
            
        
        # spec defines that requests must use POST method
        kwargs.setdefault('method', 'POST')

        # rpc query multiples times over the same url
        kwargs.setdefault('dont_filter', True)

        super(JsonRpcRequest, self).__init__(*args, **kwargs)
        if req_params:
            self.body = json.dumps(req_params)

    def __str__(self):
        return "<JSON call to %s: %s>" % (self.url, self.rpc_method)
