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

    def convert(self):
        result = []
        for medium in self.medium_collection:
            result.append(Util.convert(medium))
        return result
