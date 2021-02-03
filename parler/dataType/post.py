from .basePost import BasePost
from .media import Media
from .mentions import Mentions
from .hashtags import Hashtags
from .user import User

from .util import Util


class Post(BasePost):
    '''
    Represents a post made in Parler. Parallels to twitter tweets will be made.

    A post will be of the following:
        - An original post <==> A whole new tweet:
            Example: https://parler.com/post/f523ab0c0bad4afe8b20e210cfa8638c

        - An echoed post <==> A retweet
            Example: https://parler.com/post/ce6507b865974629bd9d76363398a884

        - An echoed post with its own reply <==> A retweet with comments:
            Example: https://parler.com/post/ce6777a798c64fc7a037db01eb8e81c9

    A post will look like the following:
    {  
       <basePost object converted to dict>
       ...
       "post_type_id" : int => [1 - 3]
       "post_type" : str => 
                     1 - "new post" 
                     2 - "echoed post"
                     3 - "echoed post with reply"
                     4 - "echoed post with root echo and no reply"
                     5 - "echoed post with root echo and reply"
       "echoed_post" : <basePost object converted to dict>
       "root_echoed_post" : <basePost object converted to dict>
    }
    '''

    UNKNOWN = -1
    ORIGINAL = 1
    ECHO_NO_REPLY = 2
    ECHO_WITH_REPLY = 3
    ECHO_WITH_ROOT_AND_NO_REPLY = 4
    ECHO_WITH_ROOT_AND_REPLY = 5

    POST_TYPE_MAP = {
        UNKNOWN: "unknown",
        ORIGINAL: "new post",
        ECHO_NO_REPLY: "echoed post",
        ECHO_WITH_REPLY: "echoed post with reply",
        ECHO_WITH_ROOT_AND_NO_REPLY: "echoed post with root echo and no reply",
        ECHO_WITH_ROOT_AND_REPLY: "echoed post with root echo and reply",
    }

    def __init__(self, main_post: BasePost,
                 post_type_id: int = UNKNOWN,
                 echoed_post: BasePost = None,
                 root_echoed_post: BasePost = None):

        super().__init__(main_post.created_at,
                         main_post.text,
                         main_post.user,
                         main_post.view_count,
                         main_post.hashtags,
                         main_post.mentions,
                         main_post.media,
                         main_post.comment_count,
                         main_post.echo_count,
                         main_post.upvote_count)

        self.post_type_id = post_type_id
        self.echoed_post = echoed_post
        self.root_echoed_post = root_echoed_post

    def convert(self):
        result = super().convert()
        result["post_type_id"] = self.post_type_id
        result["post_type"] = self.POST_TYPE_MAP[self.post_type_id]
        result["echoed_post"] = Util.convert(self.echoed_post)
        result["root_echoed_post"] = Util.convert(self.root_echoed_post)
        return result
