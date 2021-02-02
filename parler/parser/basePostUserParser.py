from parler.dataType.user import User

import parler.parser.userParserHelper as userParserHelper
import parler.parser.htmlParser as htmlParser


class BasePostUserParser:
    '''
    Parses the user profile from a base post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return User(
            name=self.get_name(),
            username=self.get_username(),
            photo=self.get_photo(),
            badge=self.get_badge())

    def get_name(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'author--name'})

    def get_username(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'author--username'})

    def get_photo(self):
        return htmlParser.get_image_src(self.post, {'alt': 'Post Author Profile Pic'})

    def get_badge(self):
        return userParserHelper.parse_parler_badge(self.post)
