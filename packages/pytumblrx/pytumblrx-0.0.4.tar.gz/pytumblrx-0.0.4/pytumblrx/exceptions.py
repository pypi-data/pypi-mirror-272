class PyTumblrXError(BaseException):
    pass


class PyTumblrXRequestError(PyTumblrXError):
    def __init__(self, method, url, *, response=None, **kwargs):
        self.method, self.url = method, url
        self.kwargs = dict(method=self.method, url=self.url, **kwargs)
        self.response = response

    @property
    def status_code(self) -> int:
        try:
            return self.response.status_code
        except AttributeError:
            return -1


class PyTumblrXRequestJSONError(PyTumblrXRequestError):
    pass


class PyTumblrXRequestAPIError(PyTumblrXRequestError):
    def __init__(self, *args, data, **kwargs):
        super(PyTumblrXRequestAPIError, self).__init__(*args, **kwargs)
        self.data = data
