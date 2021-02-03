import re

from parler.dataType.media import Media
from parler.dataType.medium import Medium

import parler.parser.htmlParser as htmlParser


class MediaParser:
    '''
    Parse the post for all mediums / media
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        '''
        Helper function to find all medium inside the post
        '''

        # There is always only one media container which can
        #  1. contain a sensitive content wrapper.
        #  2. contain one or more medium.

        medium_list = htmlParser.get_all_elements(
            self.post, 'div', re.compile('mc-.*--container'))

        sensitive_element = htmlParser.get_element_by_css(
            self.post, "div.sensitive--content--wrapper")

        sensitive = (sensitive_element is not None)

        media = Media()

        if (medium_list is None):
            return media

        for medium in medium_list:
            media.add(self.parse_medium(medium, sensitive))

        return media

    def parse_medium(self, medium, sensitive):
        '''
        Helper function to parse a medium
        '''

        medium_class_type = medium.get('class', '')[0]
        medium_type = medium_class_type[3: medium_class_type.index("--")]

        if (medium_type == "image"):
            return Medium(
                image_src=htmlParser.get_image_src(
                    medium, {'class': "mc-image--wrapper"}, html_tag="div"),
                medium_type=medium_type,
                sensitive=sensitive
            )

        image_src = htmlParser.get_image_src(
            medium, {'class': f"mc-{medium_type}--image"}, html_tag="div")

        title = htmlParser.get_text(
            medium, 'span', {'class': f"mc-{medium_type}--title"})

        excerpt = htmlParser.get_text(
            medium, 'span', {'class': f"mc-{medium_type}--excerpt"})

        link_element = htmlParser.get_element_by_css(
            medium, f'span.mc-{medium_type}--link')

        link_src = None if link_element is None else htmlParser.get_text(
            link_element, 'a', {}).strip()

        return Medium(image_src=image_src,
                      title=title,
                      excerpt=excerpt,
                      link_src=link_src,
                      medium_type=medium_type,
                      sensitive=sensitive)
