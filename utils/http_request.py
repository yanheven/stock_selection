__author__ = 'evan'
import requests

def request(url, method="GET", body=None, headers=None, **kwargs):
        """Request without authentication."""

        content_type = "text/html; charset=utf-8"
        content_type = 'application/json'
        headers = headers or {}
        headers.setdefault('Accept', content_type)

        if body:
            headers.setdefault('Content-Type', content_type)

        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36"

        resp = requests.request(
            method,
            url,
            data=body,
            headers=headers,
            **kwargs)

        return resp, resp.text