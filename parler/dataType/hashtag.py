from typing import List

from .util import Util


class Hashtag:
    '''
    Represents a hashtag.

    A hashtag will have the following fields:
    { 
        "hashtag ID" : md5Hash(text)
        "indices" : [ int, int]
        "text" : str
    }
    '''

    def __init__(self, text: str, indices: List[int]):
        self.text = text
        self.indices = indices
        self.hashtag_id = Util.get_md5Hash(text)

    def convert(self):
        return {
            "hashtag_id": self.hashtag_id,
            "indices": self.indices,
            "text": self.text
        }
