from .baseMediaType import BaseMediaType
from ..util import Util


class Article(BaseMediaType):
    '''
    Class representing a linked article inside a post.

    An article will have the following fields:
    {
        "title" : str
        "excerpt" : str
        "src" : str
        "image" : str
    }
    '''

    def __init__(self, title: str = None,
                 excerpt: str = None,
                 src: str = None,
                 image: str = None):

        super().__init__(title, excerpt, src)
        self.image = image

    @Util.return_none_on_error
    def convert(self):
        result = super().convert()
        result["image"] = self.image
        return result
