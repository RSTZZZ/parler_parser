class Image:
    '''
    Class representing a linked image inside a post.

    An image will have the following fields:
    {
        "src" : str
    }
    '''

    def __init__(self, src: str = None):
        self.src = src

    def convert(self):
        return self.src
