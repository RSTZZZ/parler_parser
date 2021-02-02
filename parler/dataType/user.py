from __future__ import annotations

from .hashtags import Hashtags
from .util import Util


class User:
    '''
    Represents a user inside Parler.

    A user will have the following attributes:
        * Photo
        * Name
        * Username <==> screen name in Twitter User Object
        * Badge 
        * Description          | Optional
        * Description Hashtags | Optional
    '''

    def __init__(self, photo: str, name: str, username: str, badge: str = None, description: str = None, description_hashtags: Hashtags = None):
        self.photo = photo
        self.name = name
        self.username = username
        self.badge = badge

        self.user_id = Util.get_md5Hash(
            username) if username is not None else ""

        self.description = description
        self.description_hashtags = description_hashtags

    def merge(self, new_user: User):
        '''
        Merge two user objects, with itself as priority. Only check the following:
            -> Badge : If new user has a badge, then replace
            -> Description : If new user has a description, then replace
            -> Description Hashtags : If new user has a description, then also replace description hashtags
        '''
        if (self.badge is None and new_user.badge is not None):
            self.badge = new_user.badge

        if (self.description is None and new_user.description is not None):
            self.description = new_user.description
            self.description_hashtags = new_user.description_hashtags

    def convert(self):
        return Util.compress_dict({
            "user_id": self.user_id,
            "photo": self.photo,
            "badge": self.badge,
            "name": self.name,
            "username": self.username,
            "description": self.description,
            "description_hashtags": Util.convert(self.description_hashtags)
        })
