class BaseMediaType:
    '''
    Class representing the base "complex" media type.

    An audio will have the following fields:
    {
        "title" : str
        "excerpt" : str
        "src" : str
    }
    '''

    def __init__(self, title: str = None,
                 excerpt: str = None,
                 src: str = None):
        self.title = title
        self.excerpt = excerpt
        self.src = src

    def convert(self):

        if (self.title is None):
            return None

        return {
            "title": self.title,
            "excerpt": self.excerpt,
            "src": self.src,
        }
