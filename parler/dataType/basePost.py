from datetime import datetime
from .user import User
from .hashtags import Hashtags
from .mentions import Mentions
from .media import Media

from .util import Util


class BasePost:
    '''
    Represents a base post made in Parler. 

    The base post will always have the following fields filled out:
    {  
        "id" : str,
        "post_id" : str,
        "estimated_created_at" : str,
        "timestamp" : str
        "text" : str,
        "user" : <user object converted to dict>,
        "view_count" : int,
        "hashtags" : <hashtag object converted to dict>
        "mentions" : <media object converted to dict>
        "media" : <media object converted to dict>,
        "comment_count" : int
        "echo_count" : int
        "upvote_count" : int
    }
    '''

    def __init__(self,
                 estimated_created_at: datetime,
                 timestamp: str,
                 text: str,
                 user: User,
                 view_count: int,
                 parler_post_id: str = None,
                 hashtags: Hashtags = None,
                 mentions: Mentions = None,
                 media: Media = None,
                 comment_count: int = None,
                 echo_count: int = None,
                 upvote_count: int = None,
                 ):
        '''
        Initializer for the base post data type.
        '''
        self.estimated_created_at = estimated_created_at
        self.timestamp = timestamp
        self.text = text
        self.user = user
        self.view_count = view_count

        self.parler_post_id = parler_post_id
        self.hashtags = hashtags
        self.mentions = mentions
        self.media = media
        self.comment_count = comment_count
        self.echo_count = echo_count
        self.upvote_count = upvote_count

    def convert(self):
        return Util.compress_dict({
            "post_hash": self.get_hash_id(),
            "parler_post_id": self.parler_post_id,
            "estimated_created_at": self.estimated_created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": self.timestamp,
            "text": self.text,
            "user": Util.convert(self.user),
            "view_count": Util.to_int(self.view_count),
            "hashtags": Util.convert(self.hashtags),
            "mentions": Util.convert(self.mentions),
            "media": Util.convert(self.media),
            "comment_count": Util.to_int(self.comment_count),
            "echo_count": Util.to_int(self.echo_count),
            "upvote_count": Util.to_int(self.upvote_count),
        })

    def get_hash_id(self):
        # This function will be used to help compare different posts.
        # We can identify a post by its text, user, hashtags, mentions, and media.
        hash_id = Util.get_md5Hash(self.text or "")
        hash_id += self.user.user_id
        hash_id += self.hashtags.get_id()
        hash_id += self.mentions.get_id()

        return hash_id
