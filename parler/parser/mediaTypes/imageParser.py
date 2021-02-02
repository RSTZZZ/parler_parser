from parler.dataType.mediaTypes.image import Image

import parler.parser.htmlParser as htmlParser


class ImageParser:
    '''
    Parse the image inside media basic container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Image(
            src=self.get_src(),
        )

    def get_src(self):
        return htmlParser.get_image_src(self.post, {'class': "mc-image--wrapper"}, html_tag="div")
