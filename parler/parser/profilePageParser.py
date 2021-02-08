import os
from datetime import datetime
from parler.parser.singlePostParser import SinglePostParser
from typing import List, Tuple

from parler.dataType.post import Post
from parler.dataType.user import User

import parler.parser.htmlParser as htmlParser

from parler.parser.profilePageUserParser import ProfilePageUserParser


class ProfilePageParser():
    '''
    Parses the given HTML file, assuming its the profile page, to get the user and all the posts listed on the profile page.
    '''

    def __init__(self, file_path, timestamp) -> None:

        if (os.path.exists(file_path)):
            with open(file_path, 'r', encoding="utf-8") as html_doc:
                self.profile_page = htmlParser.get_html_doc(html_doc)
                self.timestamp = datetime.strptime(
                    str(timestamp), '%Y%m%d%H%M%S')

    def parse(self) -> Tuple[User, List[Post]]:

        # Check if valid page
        print(self.profile_page is None)
        if (htmlParser.get_element_by_css(self.profile_page, "div#hero--wrapper") is None):
            return (None, None)

        user = ProfilePageUserParser(self.profile_page).parse()

        post_elements = htmlParser.get_all_elements(
            self.profile_page, "div", {"class": "post--card--wrapper"})

        posts = []

        for post_element in post_elements:
            posts.append(SinglePostParser(
                post_element, self.timestamp, user).parse())

        return (user, posts)
