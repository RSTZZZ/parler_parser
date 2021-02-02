from .mediaTypes.article import Article
from .mediaTypes.audio import Audio
from .mediaTypes.image import Image
from .mediaTypes.link import Link
from .mediaTypes.video import Video

from .util import Util


class Media:
    '''
    Represents the different media that a post can contain.

    A media will have the following fields:
    {
        "article":  <article class>
        "audio" : <audio class>
        "image" : <image class>
        "link" :  <link class>
        "video" : <video class>
        "slider" : <slider class>
        "iframe" : <iframe class>
    }
    '''

    def __init__(self,
                 article: Article = None,
                 audio: Audio = None,
                 image: Image = None,
                 link: Link = None,
                 video: Video = None,
                 ):
        self.article = article
        self.audio = audio
        self.image = image
        self.link = link
        self.video = video

    def convert(self):
        return Util.compress_dict({
            "article": Util.convert(self.article),
            "audio": Util.convert(self.audio),
            "image": Util.convert(self.image),
            "link": Util.convert(self.link),
            "video": Util.convert(self.video),
        })
