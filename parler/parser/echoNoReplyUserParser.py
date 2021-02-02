from parler.dataType.user import User

import parler.parser.htmlParser as htmlParser


class EchoNoReplyUserParser:
    '''
    Parses the user profile from the provided HTML document.

    * This document should be the full HTML document to be able to have
        1) echoed-by line
        2) username at the meta-data level
    '''

    def __init__(self, html_doc):
        self.html_doc = html_doc
        self.echo_by = htmlParser.get_element_by_css(
            self.html_doc, 'div.echo-byline--wrapper')

    def parse(self):
        return User(
            name=self.get_name(),
            username=self.get_username(),
            photo=self.get_photo()
        )

    def get_name(self):
        return htmlParser.get_text(self.echo_by, 'span', {'class': 'reblock'})[10:]

    def get_username(self):
        return htmlParser.get_content(self.html_doc, 'meta', {"name": "twitter:title"}).split()[0]

    def get_photo(self):
        return htmlParser.get_image_src(self.html_doc, {'alt': 'Post Author Profile Pic'})
