from typing import List

from .util import Util


class Mention:
    '''
    Represents a mention.

    A mention will have the following fields:
    { 
        "user id" : md5Hash(username)
        "username: str
        "indices" : [ int, int]        
    }
    '''

    def __init__(self, username: str, indices: List[int]):
        self.username = username
        self.indices = indices
        self.user_id = Util.get_md5Hash(username)

    def convert(self):
        return {
            "user_id": self.user_id,
            "indices": self.indices,
            "username": self.username
        }
