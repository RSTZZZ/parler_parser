from .baseMediaType import BaseMediaType


class Audio(BaseMediaType):
    '''
    Class representing a linked audio inside a post.

    An audio will have the following fields:
    {
        "title" : str
        "excerpt" : str
        "src" : str
    }
    '''
