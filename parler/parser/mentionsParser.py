import re

from parler.dataType.mentions import Mentions
from parler.dataType.mention import Mention


class MentionsParser:
    '''
    Parses all mentions from the given text.
    '''

    def __init__(self, text):
        self.text = text

    def parse(self):
        '''
        Helper function to find all mentions used inside the text.
        '''

        # https://www.nltk.org/_modules/nltk/tokenize/casual.html#TweetTokenizer
        # Use the regex based on tweet tokenizer for handles.
        mention_re = re.compile(
            r"(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)",
            re.UNICODE)

        hashtags = Mentions()

        for match in mention_re.finditer(self.text):

            username = match.group().strip()
            end_index = match.end()
            start_index = end_index - len(username)

            hashtags.add(Mention(username=username,
                                 indices=[start_index, end_index]))

        return hashtags
