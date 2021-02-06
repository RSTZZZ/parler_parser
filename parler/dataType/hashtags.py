from typing import List

from parler.dataType.hashtag import Hashtag
from .util import Util


class Hashtags:
    '''
    Represents a collection of hashtags that are found inside Parler.
    A hashtag collection will be a list of Hashtag
    '''

    def __init__(self):
        self.hashtag_collection = []

    def get_id(self):
        if (len(self.hashtag_collection) > 0):
            return self.hashtag_collection[0].hashtag_id
        return ""

    def add(self, hashtag: Hashtag):
        self.hashtag_collection.append(hashtag)

    def convert(self):
        result = []
        for hashtag in self.hashtag_collection:
            result.append(Util.convert(hashtag))

        return result
