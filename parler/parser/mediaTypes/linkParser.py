from parler.dataType.mediaTypes.link import Link

import parler.parser.htmlParser as htmlParser


class LinkParser:
    '''
    Parse the article inside media container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Link(
            src=self.get_src(),
            image=self.get_image(),
        )

    def get_src(self):
        src_element = htmlParser.get_element_by_css(
            self.post, 'span.mc-basic--link')

        if src_element is None:
            return None

        return htmlParser.get_text(src_element, 'a', {}).strip()

    def get_image(self):
        return htmlParser.get_image_src(self.post, {'class': 'mc-basic--image'}, html_tag="div")
