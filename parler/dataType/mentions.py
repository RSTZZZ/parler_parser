from typing import List

from .mention import Mention
from .util import Util


class Mentions:
    '''
    Represents a collection of mentions that are found inside Parler.
    A mention collection will be a list of Mention (s)
    '''

    def __init__(self):
        self.mention_collection = []

    def get_id(self):
        if (len(self.mention_collection) > 0):
            return self.mention_collection[0].user_id
        return ""

    def add(self, mention: Mention):
        self.mention_collection.append(mention)

    def convert(self):
        result = []
        for mention in self.mention_collection:
            result.append(Util.convert(mention))

        return result
