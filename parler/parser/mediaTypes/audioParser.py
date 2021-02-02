from parler.dataType.mediaTypes.audio import Audio

import parler.parser.htmlParser as htmlParser


class AudioParser:
    '''
    Parse the audio inside media container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Audio(
            title=self.get_title(),
            excerpt=self.get_excerpt(),
            src=self.get_src(),
        )

    def get_title(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-audio--title'})

    def get_excerpt(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-audio--excerpt'})

    def get_src(self):
        return htmlParser.get_link(self.post, 'span', {'class': 'mc-audio--link'})
