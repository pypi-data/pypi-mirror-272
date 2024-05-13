import typing
from datetime import datetime

from io import BytesIO
from pathlib import Path

try:
    from PIL import Image

    def is_pil_image(item):
        return isinstance(item, Image.Image)
except ImportError:
    def is_pil_image(item):
        return False

TimeStampType = typing.Union[datetime, int]
DateTimeGMT = typing.Union[datetime, str]


class TumblrRestClientMixin:
    @classmethod
    def define_params(cls, params):
        return {k.strip("_"): v for k, v in params.items() if v is not None}

    @staticmethod
    def to_ts(dt: typing.Optional[TimeStampType]):
        if isinstance(dt, datetime):
            return int(dt.timestamp())
        return dt

    @staticmethod
    def define_data_item(item):
        if isinstance(item, str):
            with open(item, 'rb') as f:
                return f.read()
        elif isinstance(item, Path):
            with item.open('rb') as f:
                return f.read()
        elif isinstance(item, BytesIO):
            return item
        elif is_pil_image(item):
            return item.tobytes()

    @classmethod
    def define_data_list(cls, data):
        files = dict()
        if isinstance(data, (list, tuple)):
            for idx, item in enumerate(data):
                files[f'data[{idx}]'] = cls.define_data_item(item)
        elif isinstance(data, dict):
            for k, item in data.items():
                files[k] = cls.define_data_item(item)
        item = cls.define_data_item(data)
        if item:
            files['data'] = item
        return files if files else None
