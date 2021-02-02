from parler.dataType.mediaTypes.video import Video

import parler.parser.htmlParser as htmlParser


class VideoParser:
    '''
    Parse the video inside media container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Video(
            title=self.get_title(),
            excerpt=self.get_excerpt(),
            src=self.get_src(),
        )

    def get_title(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-video--title'})

    def get_excerpt(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-video--excerpt'})

    def get_src(self):
        return htmlParser.get_link(self.post, 'span', {'class': 'mc-video--link'})
