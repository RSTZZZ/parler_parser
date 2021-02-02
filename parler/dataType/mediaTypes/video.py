from .baseMediaType import BaseMediaType


class Video(BaseMediaType):
    '''
    Class representing a linked video inside a post.

    A video will have the following fields:
    {
        "title" : str
        "excerpt" : str
        "src" : str
    }
    '''
