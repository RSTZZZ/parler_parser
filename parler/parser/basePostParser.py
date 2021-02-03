from parler.dataType.basePost import BasePost

import parler.parser.htmlParser as htmlParser

from parler.parser.basePostUserParser import BasePostUserParser
from parler.parser.hashtagsParser import HashtagsParser
from parler.parser.mentionsParser import MentionsParser
from parler.parser.mediaParser import MediaParser


class BasePostParser:
    '''
    Parse the profile from a post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return BasePost(
            created_at=self.get_created_at(),
            text=self.get_text(),
            user=self.get_user(),
            view_count=self.get_view_count(),
            hashtags=self.get_hashtags(),
            mentions=self.get_mentions(),
            media=self.get_media(),
        )

    def get_created_at(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'post--timestamp'})

    def get_text(self):
        self.text = htmlParser.get_paragraph(
            self.post, 'div',  {'class': 'card--body'})
        return self.text

    def get_user(self):
        return BasePostUserParser(self.post).parse()

    def get_view_count(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'impressions--count'})

    def get_hashtags(self):
        return HashtagsParser(self.text).parse()

    def get_mentions(self):
        return MentionsParser(self.text).parse()

    def get_media(self):
        return MediaParser(self.post).parse()
