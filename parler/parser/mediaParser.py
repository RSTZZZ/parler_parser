from parler.dataType.media import Media

from parler.parser.mediaTypes.articleParser import ArticleParser
from parler.parser.mediaTypes.audioParser import AudioParser
from parler.parser.mediaTypes.imageParser import ImageParser
from parler.parser.mediaTypes.linkParser import LinkParser
from parler.parser.mediaTypes.videoParser import VideoParser


class MediaParser:
    '''
    Parse the media container inside a post
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Media(
            article=self.get_article(),
            audio=self.get_audio(),
            image=self.get_image(),
            link=self.get_link(),
            video=self.get_video()
        )

    def get_article(self):
        return ArticleParser(self.post).parse()

    def get_audio(self):
        return AudioParser(self.post).parse()

    def get_image(self):
        return ImageParser(self.post).parse()

    def get_link(self):
        return LinkParser(self.post).parse()

    def get_video(self):
        return VideoParser(self.post).parse()
