"""
This module implements the XmlResponse class which adds encoding
discovering through XML encoding declarations to the TextResponse class.

See documentation in docs/topics/request-response.rst
"""
from scrapy.http.response.text import TextResponse
from scrapy.utils.py26 import json


class JsonRpcError(Exception):

    def __init__(self, code, message, data=None):
        super(JsonRpcError, self).__init__()
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return "JSON-RPC error (code %d): %s" % (self.code, self.message)


class JsonResponse(TextResponse):

    __slots__ = ()

    @property
    def result(self):
        res = json.loads(self.body)
        if 'result' in res:
            return res['result']
        elif 'error' in res:
            er = res['error']
            raise JsonRpcError(er['code'], er['message'], er['data'])
        else:
            msg = "JSON-RPC response must contain 'result' or 'error': %s" % res
            raise ValueError(msg)

    def __str__(self):
        return "<%d JSON self.url: %s>" % (self.status, self.url, self.result)