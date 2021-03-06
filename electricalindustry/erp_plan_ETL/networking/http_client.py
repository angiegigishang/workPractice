from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import util
import json


async_http_client = AsyncHTTPClient()


def get_http_request(url, method='GET', body=None):
    return HTTPRequest(url, method=method, body=body)


def get_http_request_data(request_data):
    json_request_data = json.dumps(request_data, ensure_ascii=False, default=util.alchemy_encoder)
    return json_request_data.encode('utf-8')
