#!/usr/bin/env mitmdump -s

from mitmproxy import http
import pymongo

collection = pymongo.MongoClient('localhost', 27017).mitm.page


def response(flow: http.HTTPFlow) -> None:
    data = {
        'request:url': flow.request.url,
        'request:method': flow.request.method,
        'request:host': flow.request.host,
        'request:port': flow.request.port,
        'request:path': flow.request.path,
        'request:http_version': flow.request.http_version,
        'request:headers': flow.request.headers,
        'request:content': flow.request.get_content(),
        'request:timestamp_start': flow.request.timestamp_start,
        'request:timestamp_end': flow.request.timestamp_end,

        'response:http_version': flow.response.http_version,
        'response:status_code': flow.response.status_code,
        'response:headers': flow.response.headers,
        'response:content': flow.response.get_content(),
        'response:timestamp_start': flow.response.timestamp_start,
        'response:timestamp_end': flow.response.timestamp_end,
    }
    collection.insert_one(data)
