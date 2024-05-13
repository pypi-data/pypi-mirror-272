import typing

from .request import TumblrAIORequest
from .endpoints import TumblrEndpoints, BlogEndpoints
from .enums import PostTypeTyping, PostFilterTyping, PostStateTyping, PostFormatTyping
from ._client_mixin import TumblrRestClientMixin, TimeStampType, DateTimeGMT


class TumblrAIORestClient(TumblrRestClientMixin):
    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="",
                 host="https://api.tumblr.com"):
        self.request = TumblrAIORequest(consumer_key, consumer_secret, oauth_token, oauth_secret, host=host)

    async def info(self):
        return await self.request.get(TumblrEndpoints.USER_INFO)

    async def avatar(self, blogname: str, size=64):
        return await self.request.get(BlogEndpoints(blogname).get_blog_avatar_size(size))

    async def likes(self, *, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None,
                    before: typing.Optional[TimeStampType] = None,
                    after: typing.Optional[TimeStampType] = None):
        return await self.request.get(TumblrEndpoints.USER_LIKES, params=self.define_params(dict(
            limit=limit, before=self.to_ts(before), offset=offset, after=self.to_ts(after)
        )))

    async def following(self, *, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None):
        return await self.request.get(TumblrEndpoints.USER_FOLLOWING, params=dict(limit=limit, offset=offset))

    async def dashboard(self, *, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None,
                        type_: typing.Optional[typing.Union[str, PostTypeTyping]] = None,
                        since_id: typing.Optional[int] = None,
                        reblog_info: typing.Optional[bool] = None, notes_info: typing.Optional[bool] = None):
        return await self.request.get(TumblrEndpoints.USER_DASHBOARD, params=self.define_params(dict(
            limit=limit, offset=offset, type_=type_, since_id=since_id, reblog_info=reblog_info, notes_info=notes_info
        )))

    async def tagged(self, tag: str, *, before: typing.Optional[TimeStampType] = None,
                     limit: typing.Optional[int] = None,
                     filter_: typing.Optional[PostFilterTyping] = None):
        return await self.request.get(TumblrEndpoints.TAGGED, params=self.define_params(
            dict(before=self.to_ts(before), limit=limit, filter_=filter_, tag=tag)
        ))

    async def posts(self, blogname: str, *, type_: typing.Optional[PostTypeTyping] = None,
                    id_: typing.Optional[int] = None,
                    tag: typing.Optional[typing.Union[str, tuple, list]] = None,
                    limit: typing.Optional[int] = None, offset: typing.Optional[int] = None,
                    reblog_info: typing.Optional[bool] = None, notes_info: typing.Optional[bool] = None,
                    filter_: typing.Optional[PostFilterTyping] = None,
                    before: typing.Optional[TimeStampType] = None, npf: bool = False):
        return await self.request.get(BlogEndpoints(blogname).BLOG_POSTS, needs_api_key=True, params=self.define_params(
            dict(type_=type_, id_=id_, tag=tag, limit=limit, reblog_info=reblog_info, offset=offset,
                 notes_info=notes_info, filter_=filter_, before=self.to_ts(before), npf=npf)
        ))

    async def blog_info(self, blogname: str):
        return await self.request.get(BlogEndpoints(blogname).BLOG_INFO, needs_api_key=True)

    async def blog_following(self, blogname: str, *, limit: typing.Optional[int] = None,
                             offset: typing.Optional[int] = None):
        return await self.request.get(BlogEndpoints(blogname).BLOG_FOLLOWING,
                                      params=self.define_params(dict(limit=limit, offset=offset)))

    async def followers(self, blogname, *, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None):
        return await self.request.get(BlogEndpoints(blogname).BLOG_FOLLOWERS,
                                      params=self.define_params(dict(limit=limit, offset=offset)))

    async def blog_likes(self, blogname, *, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None,
                         before: typing.Optional[TimeStampType] = None, npf: bool = False,
                         after: typing.Optional[TimeStampType] = None):
        return await self.request.get(BlogEndpoints(blogname).BLOG_LIKES, needs_api_key=True, params=self.define_params(
            dict(limit=limit, offset=offset, npf=npf, before=self.to_ts(before), after=self.to_ts(after))
        ))

    async def queue(self, blogname, limit: typing.Optional[int] = None, offset: typing.Optional[int] = None,
                    filter_: typing.Optional[PostFilterTyping] = None, npf: bool = False):
        return await self.request.get(BlogEndpoints(blogname).BLOG_QUEUE,
                                      params=dict(imit=limit, offset=offset, filter_=filter_, npf=npf))

    async def drafts(self, blogname, *, filter_: typing.Optional[PostFilterTyping] = None,
                     npf: bool = False):
        return await self.request.get(BlogEndpoints(blogname).BLOG_POSTS_DRAFT,
                                      params=self.define_params(dict(filter_=filter_, npf=npf)))

    async def submission(self, blogname, *, npf: bool = False,
                         limit: typing.Optional[int] = None, offset: typing.Optional[int] = None):
        return await self.request.get(BlogEndpoints(blogname).BLOG_QUEUE,
                                      params=dict(limit=limit, offset=offset, npf=npf))

    async def follow(self, blogname: str):
        return await self.request.post(TumblrEndpoints.USER_FOLLOW, params=dict(url=blogname))

    async def unfollow(self, blogname: str):
        return await self.request.post(TumblrEndpoints.USER_UNFOLLOW, params=dict(url=blogname))

    async def like(self, id_: int, reblog_key: typing.Optional[str] = None):
        return await self.request.post(TumblrEndpoints.USER_LIKE,
                                       params=self.define_params(dict(id_=id_, reblog_key=reblog_key)))

    async def unlike(self, id_: int, reblog_key: typing.Optional[str] = None):
        return await self.request.post(TumblrEndpoints.USER_UNLIKE,
                                       params=self.define_params(dict(id_=id_, reblog_key=reblog_key)))

    async def reblog(self, blogname, *, id_: int, reblog_key: typing.Optional[str] = None,
                     comment: typing.Optional[str] = None, native_inline_images: typing.Optional[bool] = None):
        return await self.request.post(BlogEndpoints(blogname).BLOG_POST_REBLOG, params=self.define_params(dict(
            id_=id_, reblog_key=reblog_key, comment=comment, native_inline_images=native_inline_images
        )))

    async def delete_post(self, blogname: str, id_: int):
        return await self.request.post(BlogEndpoints(blogname).BLOG_POST_DELETE, params={"id": id_})

    async def edit_post(self, blogname: str, *, id_: int):
        raise NotImplementedError

    async def notes(self, blogname: str, id_, *,
                    mode: typing.Optional[typing.Literal['all', 'likes', 'conversations',
                                                         'rollup', 'reblogs_with_tags']] = None,
                    before_timestamp: typing.Optional[TimeStampType]):
        return await self.request.get(BlogEndpoints(blogname).BLOG_POST_NOTES, params=self.define_params(
            dict(id_=id_, mode=mode, before_timestamp=self.to_ts(before_timestamp))
        ))

    async def create_photo(self, blogname: str, *, state: typing.Optional[PostStateTyping] = None,
                           tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                           tweet: typing.Optional[str] = None,
                           format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                           native_inline_images: typing.Optional[bool] = None,
                           caption: typing.Optional[str] = None, link: typing.Optional[str] = None,
                           source: typing.Optional[str] = None,
                           data: typing.Optional[typing.Union[str, list, tuple, dict]]):
        raise NotImplementedError

    async def create_text(self, blogname: str, *, body: str, state: typing.Optional[PostStateTyping] = None,
                          tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                          tweet: typing.Optional[str] = None,
                          format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                          title: typing.Optional[str] = None, native_inline_images: typing.Optional[bool] = None):
        raise NotImplementedError

    async def create_quote(self, blogname: str, *, quote: str, state: typing.Optional[PostStateTyping] = None,
                           tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                           tweet: typing.Optional[str] = None,
                           native_inline_images: typing.Optional[bool] = None,
                           format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                           source: typing.Optional[str] = None):
        raise NotImplementedError

    async def create_link(self, blogname: str, *, url: str, state: typing.Optional[PostStateTyping] = None,
                          tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                          tweet: typing.Optional[str] = None,
                          format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                          title: typing.Optional[str] = None, description: typing.Optional[str] = None,
                          thumbnail: typing.Optional[str] = None, excerpt: typing.Optional[str] = None,
                          author: typing.Optional[str] = None, native_inline_images: typing.Optional[bool] = None):
        raise NotImplementedError

    async def create_chat(self, blogname: str, *, conversation: str, state: typing.Optional[PostStateTyping] = None,
                          tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                          tweet: typing.Optional[str] = None,
                          format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                          title: typing.Optional[str] = None, native_inline_images: typing.Optional[bool] = None):
        raise NotImplementedError

    async def create_audio(self, blogname: str, *, state: typing.Optional[PostStateTyping] = None,
                           tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                           tweet: typing.Optional[str] = None,
                           format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                           caption: typing.Optional[str] = None, external_url: typing.Optional[str] = None,
                           data: typing.Optional[typing.Union[str, list, tuple, dict]],
                           native_inline_images: typing.Optional[bool] = None):
        raise NotImplementedError

    async def create_video(self, blogname: str, *, state: typing.Optional[PostStateTyping] = None,
                           tags: typing.Optional[typing.Union[str, tuple, list]] = None,
                           tweet: typing.Optional[str] = None,
                           format_: typing.Optional[PostFormatTyping] = None, slug: typing.Optional[str] = None,
                           caption: typing.Optional[str] = None, embed: typing.Optional[str] = None,
                           data: typing.Optional[typing.Union[str, list, tuple, dict]],
                           native_inline_images: typing.Optional[bool] = None):
        raise NotImplementedError

    async def create_post(self, post_type: PostTypeTyping, blogname: str, kwargs):
        raise NotImplementedError
