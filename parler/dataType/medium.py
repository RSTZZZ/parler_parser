class Medium:
    '''
    Class representing the medium inside the post.

    A medium will always have the following: {
        image_src   :  str
        title       :  str
        excerpt     :  str
        link_src    :  str
        media_type_id : int => [1 - 7]
        media_type:  => 
            1 - "article"
            2 - "audio"
            3 - "iframe"
            4 - "image"
            5 - "link"
            6 - "video"
            7 - "website"
        sensitive : bool
    }

    '''

    UNKNOWN = -1
    ARTICLE = 1
    AUDIO = 2
    IFRAME_EMBED = 3
    IMAGE = 4
    BASIC = 5
    VIDEO = 6
    WEBSITE = 7

    MEDIA_TYPE_MAP = {
        "unknown": UNKNOWN,
        "article": ARTICLE,
        "audio": AUDIO,
        "iframe-embed": IFRAME_EMBED,
        "image": IMAGE,
        "basic": BASIC,
        "video": VIDEO,
        "website": WEBSITE,
    }

    def __init__(self, image_src: str = None,
                 title: str = None,
                 excerpt: str = None,
                 link_src: str = None,
                 medium_type: str = None,
                 sensitive: bool = None,
                 ):

        self.image_src = image_src
        self.title = title
        self.excerpt = excerpt
        self.link_src = link_src
        self.medium_type = medium_type
        self.sensitive = sensitive

    def convert(self):
        return {
            "medium_type_id": self.MEDIA_TYPE_MAP[self.medium_type],
            "medium_type": self.medium_type,
            "title": self.title,
            "excerpt": self.excerpt,
            "image_src": self.image_src,
            "link_src": self.link_src,
            "sensitive": self.sensitive,
        }
