from dateutil.relativedelta import relativedelta

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

    def __init__(self, post, file_creation_date, parler_post_id=None):
        self.post = post
        self.file_creation_date = file_creation_date
        self.parler_post_id = parler_post_id

    def parse(self):
        return BasePost(
            timestamp=self.get_timestamp(),
            estimated_created_at=self.get_estimated_created_at(),
            text=self.get_text(),
            user=self.get_user(),
            view_count=self.get_view_count(),
            parler_post_id=self.parler_post_id,
            hashtags=self.get_hashtags(),
            mentions=self.get_mentions(),
            media=self.get_media(),
        )

    def get_timestamp(self):
        self.timestamp = htmlParser.get_text(
            self.post, 'span', {'class': 'post--timestamp'})
        return self.timestamp

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

    def get_estimated_created_at(self):
        if (self.timestamp is None):
            return None

        time_interval = int(self.timestamp.split()[0])

        if ("min" in self.timestamp):
            return self.file_creation_date - relativedelta(minutes=time_interval)

        if ("day" in self.timestamp):
            return self.file_creation_date - relativedelta(days=time_interval)

        if ("week" in self.timestamp):
            return self.file_creation_date - relativedelta(weeks=time_interval)

        if ("year" in self.timestamp):
            return self.file_creation_date - relativedelta(years=time_interval)
