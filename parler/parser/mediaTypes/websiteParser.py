from parler.dataType.mediaTypes.website import Website

import parler.parser.htmlParser as htmlParser


class WebsiteParser:
    '''
    Parse the website inside media container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Website(
            title=self.get_title(),
            excerpt=self.get_excerpt(),
            src=self.get_src(),
            image=self.get_image(),
        )

    def get_title(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-website--title'})

    def get_excerpt(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-website--excerpt'})

    def get_src(self):
        src_element = htmlParser.get_element_by_css(
            self.post, 'span.mc-website--link')

        if src_element is None:
            return None

        return htmlParser.get_text(src_element, 'a', {}).strip()

    def get_image(self):
        return htmlParser.get_image_src(self.post, 'span', {'alt': "Website Image"})
