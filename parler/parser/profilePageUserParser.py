from parler.dataType.user import User

import parler.parser.htmlParser as htmlParser
import parler.parser.userParserHelper as userParserHelper

from parler.parser.hashtagsParser import HashtagsParser


class ProfilePageUserParser:
    '''
    Represents the steps to parse a user from the profile page.
    '''

    def __init__(self, profile_page) -> None:
        self.profile_page = profile_page

    def parse(self) -> User:
        return User(
            name=self.get_name(),
            username=self.get_username(),
            photo=self.get_photo(),
            badge=self.get_badge(),
            description=self.get_description(),
            description_hashtags=self.get_description_hashtags(),
        )

    def get_name(self):
        return htmlParser.get_text(self.profile_page, 'span', {'class': 'profile--name'})

    def get_username(self):
        username = htmlParser.get_text(self.profile_page, 'span', {
                                       'class': 'profile--username'})

        if (username is not None and not username.startswith("@")):
            username = "@" + username

        return username

    def get_photo(self):
        return htmlParser.get_image_src(self.profile_page, {'class': 'profile-photo-image'}, html_tag='div')

    def get_badge(self):
        badge_html_element = htmlParser.get_element_by_css(
            self.profile_page, "div.ch--avatar--badge--wrapper")
        return userParserHelper.parse_parler_badge(badge_html_element)

    def get_description(self):
        '''
        Parses the profile page to get the "profile--bio" to get the user profile description as well as any hashtags inside.
        Returns (str, Hashtags)
        '''
        return htmlParser.get_text(self.profile_page, 'span', {'class': 'profile--bio'})

    def get_description_hashtags(self):
        '''
        Parses the profile page to get the "profile--bio" to get the user profile description as well as any hashtags inside.
        Returns (str, Hashtags)
        '''
        description = htmlParser.get_text(
            self.profile_page, 'span', {'class': 'profile--bio'})
        return HashtagsParser(description).parse()
