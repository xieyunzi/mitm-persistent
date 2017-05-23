from mitmproxy import http


def response(flow: http.HTTPFlow) -> None:
    print('-- request url')
    print(flow.request.url)
    print(flow.request.method)

    print('-- response')
    print(flow.response.http_version)
    print(flow.response.status_code)
    print(flow.response.headers)
    print(flow.response.get_content)
