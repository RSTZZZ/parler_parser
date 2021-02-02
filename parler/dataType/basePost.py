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
        "created_at" : str,
        "id" : str,
        "text" : str,
        "user" : <user object converted to dict>,
        "view_count" : int,
        "hashtags" : <hashtag object converted to dict>
        "mentions" : <media object converted to dict>
        "media" : <media object converted to dict>,
    }
    '''

    def __init__(self,
                 created_at: str,
                 text: str,
                 user: User,
                 view_count: int,
                 hashtags: Hashtags = None,
                 mentions: Mentions = None,
                 media: Media = None):
        '''
        Initializer for the base post data type.
        '''
        self.created_at = created_at
        self.text = text
        self.user = user
        self.view_count = view_count
        self.hashtags = hashtags
        self.mentions = mentions
        self.media = media
        self.id = ""

    def convert(self):
        return Util.compress_dict({
            "created_at": self.created_at,
            "id": self.id,
            "text": self.text,
            "user": Util.convert(self.user),
            "view_count": self.view_count,
            "hashtags": Util.convert(self.hashtags),
            "mentions": Util.convert(self.mentions),
            "media": Util.convert(self.media),
        })
