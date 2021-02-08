from datetime import datetime
from dateutil.relativedelta import relativedelta


from parler.dataType.basePost import BasePost
from parler.dataType.post import Post
from parler.dataType.user import User

import parler.parser.htmlParser as htmlParser

from parler.parser.basePostParser import BasePostParser
from parler.parser.echoNoReplyUserParser import EchoNoReplyUserParser


class SinglePostParser():
    '''
    Parses a given HTML element for a parler post.
    '''

    def __init__(self, post_element, file_creation_date: datetime, user: User, file_name=None):
        self.post_element = post_element
        self.post_type = Post.UNKNOWN
        self.file_creation_date = file_creation_date
        self.file_name = file_name
        self.user = user

    def parse(self) -> Post:

        self.get_needed_html_sections()
        self.set_post_type_id()

        # Early exit if we cannot determine the post type
        if (self.post_type_id == Post.UNKNOWN):
            return None

        # Get the main post -> Original post | Echo reply Post
        post = Post(self.get_main_post_info())
        post.post_type_id = self.post_type_id

        # Fill out echoed post if it exists:
        if (self.post_type_id != Post.ORIGINAL):
            post.echoed_post = self.get_echoed_post_info()

        if (self.post_type_id == Post.ECHO_NO_REPLY or self.post_type_id == Post.ECHO_WITH_ROOT_AND_NO_REPLY):
            #   1. Our main post will not get a proper user.
            #   2. Our main post will not have a proper created_at time | use the one provided
            post.user = self.user
            post.timestamp = self.get_created_at_from_echo_no_reply()
            post.estimated_created_at = self.get_estimated_created_at(
                post.timestamp)

            # The comment, echo and upvote found belongs to the echoed post
            post.echoed_post.comment_count = self.get_comment_count()
            post.echoed_post.echo_count = self.get_echo_count()
            post.echoed_post.upvote_count = self.get_upvote_count()
        else:
            # The comment, echo and upvote found belongs to the main post
            post.comment_count = self.get_comment_count()
            post.echo_count = self.get_echo_count()
            post.upvote_count = self.get_upvote_count()

        if (self.post_type_id == Post.ECHO_WITH_ROOT_AND_NO_REPLY or self.post_type_id == Post.ECHO_WITH_ROOT_AND_REPLY):
            # Get the root echoed post
            post.root_echoed_post = self.get_root_echoed_post_info()

        return post

    def get_needed_html_sections(self):
        self.echo_byline = htmlParser.get_element_by_css(
            self.post_element, "div.echo-byline--wrapper")

        self.root_echoed_post = htmlParser.get_element_by_css(
            self.post_element, 'span.reblock.echo--root'
        )

        self.echoed_post = htmlParser.get_element_by_css(
            self.post_element, 'span.reblock.echo--parent'
        )

        self.echo_reply_post = htmlParser.get_element_by_css(
            self.post_element, "span.reblock.show-under-echo")

        self.new_post = htmlParser.get_element_by_css(
            self.post_element, 'span.reblock.post'
        )

    def set_post_type_id(self):
        if self.new_post is None and self.echo_byline is None:
            self.post_type_id = Post.UNKNOWN
            return

        if self.echo_byline is None:
            self.post_type_id = Post.ORIGINAL
        else:
            if self.root_echoed_post is None:
                if self.echo_reply_post is None:
                    self.post_type_id = Post.ECHO_NO_REPLY
                else:
                    self.post_type_id = Post.ECHO_WITH_REPLY
            else:
                if self.echo_reply_post is None:
                    self.post_type_id = Post.ECHO_WITH_ROOT_AND_NO_REPLY
                else:
                    self.post_type_id = Post.ECHO_WITH_ROOT_AND_REPLY

    def get_main_post_info(self) -> BasePost:
        if (self.post_type_id == Post.ORIGINAL):
            return BasePostParser(self.new_post, self.file_creation_date, parler_post_id=self.file_name).parse()
        else:
            return BasePostParser(self.echo_reply_post, self.file_creation_date, parler_post_id=self.file_name).parse()

    def get_echoed_post_info(self) -> BasePost:
        return BasePostParser(self.echoed_post, self.file_creation_date).parse()

    def get_root_echoed_post_info(self) -> BasePost:
        return BasePostParser(self.root_echoed_post, self.file_creation_date).parse()

    def get_created_at_from_echo_no_reply(self):
        timestamp = htmlParser.get_element_by_css(
            self.post_element, 'div.eb--timestamp')
        return htmlParser.get_text(timestamp, 'span', {})

    def get_comment_count(self):
        return htmlParser.get_text(self.post_element, 'span', {'class': 'pa--item--count'}, index=0)

    def get_echo_count(self):
        return htmlParser.get_text(self.post_element, 'span', {'class': 'pa--item--count'}, index=1)

    def get_upvote_count(self):
        return htmlParser.get_text(self.post_element, 'span', {'class': 'pa--item--count'}, index=2)

    def get_estimated_created_at(self, timestamp):
        time_interval = int(timestamp.split()[0])

        if ("min" in timestamp):
            return self.file_creation_date - relativedelta(minutes=time_interval)

        if ("hour" in timestamp):
            return self.file_creation_date - relativedelta(hours=time_interval)

        if ("day" in timestamp):
            return self.file_creation_date - relativedelta(days=time_interval)

        if ("week" in timestamp):
            return self.file_creation_date - relativedelta(weeks=time_interval)

        if ("month" in timestamp):
            return self.file_creation_date - relativedelta(months=time_interval)

        if ("year" in timestamp):
            return self.file_creation_date - relativedelta(years=time_interval)
