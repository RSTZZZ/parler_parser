from typing import List

from parler.dataType.medium import Medium
from .util import Util


class Media:
    '''
    Represents a collection of medium (media) that are found inside Parler.
    A medium collection will be a list of mediums
    '''

    def __init__(self):
        self.medium_collection = []

    def add(self, medium: Medium):
        self.medium_collection.append(medium)

    def get_id(self):
        try:
            if (len(self.medium_collection) > 0):
                return Util.get_md5Hash(Util.convert(self.medium_collection[0]))
            return Util.get_md5Hash("")
        except Exception:
            return Util.get_md5Hash("")

    def convert(self):
        result = []
        for medium in self.medium_collection:
            result.append(Util.convert(medium))
        return result
