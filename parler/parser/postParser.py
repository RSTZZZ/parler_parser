import os

from parler.dataType.basePost import BasePost
from parler.dataType.post import Post
from parler.dataType.user import User

import parler.parser.htmlParser as htmlParser

from parler.parser.basePostParser import BasePostParser
from parler.parser.echoNoReplyUserParser import EchoNoReplyUserParser


class PostParser():
    '''
    Parses a given HTML file for a parler post.
    '''

    def __init__(self, file_path: str):
        self.post_page = None
        self.post_type = Post.UNKNOWN

        if (os.path.exists(file_path)):
            with open(file_path, 'r', encoding="utf-8") as html_doc:
                self.post_page = htmlParser.get_html_doc(html_doc)

    def parse(self) -> Post:

        echo_byline = htmlParser.get_element_by_css(
            self.post_page, "div.echo-byline--wrapper")

        echo_reply_post = htmlParser.get_element_by_css(
            self.post_page, "span.reblock.show-under-echo")

        main_post = htmlParser.get_element_by_css(
            self.post_page, 'span.reblock.post'
        )

        self.post_type = self.get_post_type(
            echo_byline, echo_reply_post, main_post)

        if (self.post_type == Post.UNKNOWN):
            return None

        post = Post(self.get_main_post_info(main_post))
        post.post_type = self.post_type

        # If the echo has no reply,our main post will not get a proper user.
        if (self.post_type == Post.ECHO_NO_REPLY):
            post.user = self.get_user_from_echo_no_reply()

        # Only if our post has an echo, do we try to retrive.
        if (self.post_type == Post.ECHO_WITH_REPLY):
            post.echoed_status = self.get_echoed_post_info(echo_reply_post)
        else:
            post.echoed_status = None

        post.comment_count = self.get_comment_count()
        post.echo_count = self.get_echo_count()
        post.upvote_count = self.get_upvote_count()

        return post

    def get_post_type(self, echo_byline, echo_reply_post, main_post):

        if echo_byline is None:
            return Post.ORIGINAL
        else:
            if echo_reply_post is None:
                return Post.ECHO_NO_REPLY
            else:
                return Post.ECHO_WITH_REPLY

    def get_main_post_info(self, main_post) -> BasePost:
        return BasePostParser(main_post).parse()

    def get_echoed_post_info(self, echoed_post) -> BasePost:
        return BasePostParser(echoed_post).parse()

    def get_user_from_echo_no_reply(self) -> User:
        return EchoNoReplyUserParser(self.post_page).parse()

    def get_comment_count(self):
        return htmlParser.get_text(self.post_page, 'span', {'class': 'pa--item--count'}, index=0)

    def get_echo_count(self):
        return htmlParser.get_text(self.post_page, 'span', {'class': 'pa--item--count'}, index=1)

    def get_upvote_count(self):
        return htmlParser.get_text(self.post_page, 'span', {'class': 'pa--item--count'}, index=2)
