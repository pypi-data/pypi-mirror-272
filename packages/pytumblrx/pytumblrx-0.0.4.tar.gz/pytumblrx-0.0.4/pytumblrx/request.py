import httpx
from ._about import __version__
from ._defaults import PYTUMBLRX_FULL_COMPATIBILITY, PYTUMBLRX_REQUEST_JSON_ERROR
from .exceptions import PyTumblrXRequestJSONError
from typing import Optional, Union, Iterable, Literal
from authlib.integrations.httpx_client import OAuth1Client, AsyncOAuth1Client
from json import JSONDecodeError


__all__ = ['TumblrRequest', 'TumblrAIORequest']


class BasicTumblrRequest:
    """
    Basic request class to query Tumblr API
    """

    def __init__(self, consumer_key, host="https://api.tumblr.com"):
        self.host = host
        self.consumer_key = consumer_key

        self.headers = {
            "User-Agent": "pytumblrx/" + __version__
        }

    def request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], url: Union[httpx.URL, str], *,
                params: Optional[dict] = None, files: Optional[dict] = None, response_raw=False,
                needs_api_key: bool = False, **kwargs):
        raise NotImplementedError

    def get(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False, **kwargs):
        raise NotImplementedError

    def post(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None,
             files: Optional[Iterable] = None, needs_api_key: bool = False, **kwargs):
        raise NotImplementedError

    def post_multipart(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None,
                       files: Optional[Iterable] = None, needs_api_key: bool = False, **kwargs):
        return self.post(url, params=params, files=files, **kwargs)

    def delete(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, **kwargs):
        raise NotImplementedError

    def put(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False, **kwargs):
        raise NotImplementedError


class TumblrRequest(BasicTumblrRequest):
    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", *,
                 host="https://api.tumblr.com", client_kwargs=None):  # TODO: Support host change
        super().__init__(consumer_key, host=host)
        if client_kwargs is None:
            client_kwargs = dict()
        self.client = OAuth1Client(consumer_key, consumer_secret, oauth_token, oauth_secret,
                                   headers=self.headers, base_url=self.host, **client_kwargs)

    def request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], url: Union[httpx.URL, str], *,
                params: Optional[dict] = None, files: Optional[dict] = None, response_raw=False,
                needs_api_key: bool = False, **kwargs):
        if files is not None and method != "POST":
            raise ValueError("File upload only in POST methods")
        if params and kwargs:
            params.update(kwargs)
        params = dict(method=method, url=url,
                      json=params if method in ("POST", "PUT", "PATCH") else None,
                      files=files,
                      params=params if method not in ("POST", "PUT", "PATCH") else None,
                      follow_redirects=False)
        if needs_api_key:
            params['params']['api_key'] = self.consumer_key
        resp = self.client.request(**params)
        if response_raw:
            return resp
        try:
            data = resp.json()
        except JSONDecodeError as e:
            if PYTUMBLRX_REQUEST_JSON_ERROR:
                data = {'meta': {'status': 500, 'msg': 'Server Error'},
                        'response': {"error": "Malformed JSON or HTML was returned."}}
            else:
                raise PyTumblrXRequestJSONError(method, url, response=resp,
                                                params=params, files=files)
        if 200 <= data['meta']['status'] <= 399:  # return 'response' only if succeed
            return data['response']
        else:
            return data

    def get(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False, **kwargs):
        return self.request("GET", url, params=params, needs_api_key=needs_api_key, **kwargs)

    def post(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, files: Optional[Iterable] = None,
             needs_api_key: bool = False, **kwargs):
        return self.request("POST", url, params=params, files=files, needs_api_key=needs_api_key, **kwargs)

    def delete(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False, **kwargs):
        return self.request("DELETE", url, params=params, needs_api_key=needs_api_key, **kwargs)

    def put(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False, **kwargs):
        return self.request("PUT", url, params=params, needs_api_key=needs_api_key, **kwargs)


class TumblrAIORequest(BasicTumblrRequest):
    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", *,
                 host="https://api.tumblr.com", client_kwargs=None):
        super(TumblrAIORequest, self).__init__(consumer_key, host=host)
        if client_kwargs is None:
            client_kwargs = dict()

        self.client_kwargs = dict(client_id=consumer_key, client_secret=consumer_secret,
                                  token=oauth_token, token_secret=oauth_secret, headers=self.headers,
                                  base_url=self.host, **client_kwargs)

    async def request(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], url: Union[httpx.URL, str], *,
                      params: Optional[dict] = None, files: Optional[dict] = None, response_raw=False,
                      needs_api_key: bool = False, **kwargs):
        if files is not None and method != "POST":
            raise ValueError("File upload only in POST methods")
        if params and kwargs:
            params.update(kwargs)
        params = dict(method=method, url=url,
                      json=params if method in ("POST", "PUT", "PATCH") else None,
                      files=files,
                      params=params if method not in ("POST", "PUT", "PATCH") else None,
                      follow_redirects=False)
        if needs_api_key:
            params['params']['api_key'] = self.consumer_key
        async with AsyncOAuth1Client(**self.client_kwargs) as client:
            resp = await client.request(**params)
            if response_raw:
                return resp
            try:
                data = await resp.json()
            except JSONDecodeError:
                if PYTUMBLRX_REQUEST_JSON_ERROR:
                    data = {'meta': {'status': 500, 'msg': 'Server Error'},
                            'response': {"error": "Malformed JSON or HTML was returned."}}
                else:
                    raise PyTumblrXRequestJSONError(method, url, response=resp,
                                                    params=params, files=files)
            if 200 <= data['meta']['status'] <= 399:  # return 'response' only if succeed
                return data['response']
            else:
                return data

    async def get(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False,
                  **kwargs):
        return await self.request("GET", url, params=params, needs_api_key=needs_api_key, **kwargs)

    async def post(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, files: Optional[Iterable] = None,
                   needs_api_key: bool = False, **kwargs):
        return await self.request("POST", url, params=params, files=files, needs_api_key=needs_api_key, **kwargs)

    async def delete(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False,
                     **kwargs):
        return await self.request("DELETE", url, params=params, needs_api_key=needs_api_key, **kwargs)

    async def put(self, url: Union[httpx.URL, str], *, params: Optional[dict] = None, needs_api_key: bool = False,
                  **kwargs):
        return await self.request("PUT", url, params=params, needs_api_key=needs_api_key, **kwargs)
