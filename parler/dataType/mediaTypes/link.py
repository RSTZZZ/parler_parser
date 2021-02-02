class Link:
    '''
    Class representing a linked link inside a post.

    A link will have the following fields:
    {
        "src" : str
        "image" : str
    }
    '''

    def __init__(self, src: str = None, image: str = None):
        self.src = src
        self.image = image

    def convert(self):
        if (self.src is None):
            return None

        return {
            "src": self.src,
            "image": self.image,
        }
