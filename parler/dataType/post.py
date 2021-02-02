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
       "post_type" : int => 
                     1 - "original" 
                     2 - "echo"
                     3 - "echo with reply"
       "echoed_status" : <basePost object converted to dict>
    }
    '''

    UNKNOWN = -1
    ORIGINAL = 1
    ECHO_NO_REPLY = 2
    ECHO_WITH_REPLY = 3

    def __init__(self, main_post: BasePost,
                 post_type: int = ORIGINAL,
                 echoed_status: BasePost = None):

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

        self.post_type = post_type
        self.echoed_status = echoed_status

    def convert(self):
        result = super().convert()
        result["post_type"] = self.post_type
        result["echoed_status"] = Util.convert(self.echoed_status)
        return result
