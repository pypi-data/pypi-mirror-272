from httpx import URL

__all__ = ["TumblrEndpoints", "BlogEndpoints", "PostEndpoints"]


class TumblrEndpoints:
    OAUTH1_REQ = URL("https://tumblr.com/oauth/request_token/")
    OAUTH1_TOKEN = URL("https://tumblr.com/oauth/access_token/")

    DEFAULT_HOST = URL("https://api.tumblr.com/")

    V2 = DEFAULT_HOST.join("v2/")

    OAUTH2_AUTH = V2.join("oauth2/authorize/")
    OAUTH2_TOKEN = V2.join("oauth2/token/")
    OAUTH2_EXCHANGE = V2.join("oauth2/exchange/")

    USER = V2.join("user/")
    USER_INFO = USER.join("info/")
    USER_LIMITS = USER.join("limits/")
    USER_DASHBOARD = USER.join("dashboard/")
    USER_LIKES = USER.join("likes/")
    USER_FOLLOWING = USER.join("following/")
    USER_FOLLOW = USER.join("follow/")
    USER_UNFOLLOW = USER.join("unfollow/")
    USER_LIKE = USER.join("like/")
    USER_UNLIKE = USER.join("unlike/")
    USER_FILTERED_TAGS = USER.join("filtered_tags/")
    USER_FILTERED_CONTENT = USER.join("filtered_content/")

    TAGGED = V2.join("tagged/")


class BlogEndpoints(TumblrEndpoints):
    def __init__(self, blog: str):
        self.blog = blog

        self.BLOG_ENDPOINT = self.V2.join("blog/").join(self.blog + "/")

        self.BLOG_INFO = self.BLOG_ENDPOINT.join("info/")
        self.BLOG_AVATAR = self.BLOG_ENDPOINT.join("avatar/")
        self.BLOG_BLOCKS = self.BLOG_ENDPOINT.join("blocks/")
        self.BLOG_BLOCKS_BULK = self.BLOG_BLOCKS.join("bulk/")
        self.BLOG_LIKES = self.BLOG_ENDPOINT.join("likes/")
        self.BLOG_FOLLOWING = self.BLOG_ENDPOINT.join("following/")
        self.BLOG_FOLLOWERS = self.BLOG_ENDPOINT.join("followers/")
        self.BLOG_FOLLOWED_BY = self.BLOG_ENDPOINT.join("followed_by/")
        self.BLOG_POSTS = self.BLOG_ENDPOINT.join("posts/")
        self.BLOG_QUEUE = self.BLOG_POSTS.join("queue/")
        self.BLOG_QUEUE_REORDER = self.BLOG_QUEUE.join("reorder/")
        self.BLOG_QUEUE_SHUFFLE = self.BLOG_QUEUE.join("shuffle/")
        self.BLOG_POSTS_DRAFT = self.BLOG_POSTS.join("draft/")
        self.BLOG_POSTS_SUBMISSION = self.BLOG_POSTS.join("submission/")
        self.BLOG_NOTIFICATIONS = self.BLOG_ENDPOINT.join("notifications/")
        self.BLOG_POST = self.BLOG_ENDPOINT.join("post/")
        self.BLOG_POST_EDIT = self.BLOG_POST.join("edit/")
        self.BLOG_POST_REBLOG = self.BLOG_POST.join("reblog/")
        self.BLOG_POST_DELETE = self.BLOG_POST.join("delete/")
        self.BLOG_POST_NOTES = self.BLOG_ENDPOINT.join("notes/")

    def get_blog_avatar_size(self, size):
        return self.BLOG_AVATAR.join(str(size) + "/")

    def get_posts_and_type(self, type_):
        return self.BLOG_POST.join(type_ + "/")


class PostEndpoints(TumblrEndpoints):
    # Neue post format only
    def __init__(self, blog, post):
        self.blog, self.post = blog, post

        self.POST = self.V2.join("blog/{blog}/posts/{post}".format(blog=self.blog, post=self.post))
