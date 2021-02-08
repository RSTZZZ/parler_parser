import os
from parler.parser.singlePostParser import SinglePostParser
import platform
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

        if (os.path.exists(file_path)):
            with open(file_path, 'r', encoding="utf-8") as html_doc:
                self.post_page = htmlParser.get_html_doc(html_doc)
                self.file_creation_date = self.get_file_creation_date(
                    file_path)
                self.file_name = os.path.basename(file_path)
                self.user = self.get_user_from_echo_no_reply()

    def get_file_creation_date(self, file_path):
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            file_creation_timestamp = os.path.getctime(file_path)
        else:
            stat = os.stat(file_path)
            try:
                file_creation_timestamp = stat.st_birthtime
            except AttributeError:
                file_creation_timestamp = stat.st_mtime

        return datetime.fromtimestamp(file_creation_timestamp)

    def get_user_from_echo_no_reply(self) -> User:
        try:
            return EchoNoReplyUserParser(self.post_page).parse()
        except Exception:
            return None

    def parse(self) -> Post:
        if (self.post_page is None):
            return None

        return SinglePostParser(self.post_page, self.file_creation_date, self.user, self.file_name).parse()
