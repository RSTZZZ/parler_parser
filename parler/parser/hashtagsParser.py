import re

from parler.dataType.hashtags import Hashtags
from parler.dataType.hashtag import Hashtag


class HashtagsParser:
    '''
    Parses all hashtags from the given text.
    '''

    def __init__(self, text):
        self.text = text

    def parse(self):
        '''
        Helper function to find all hashtags used inside the text.
        '''

        # https://www.nltk.org/_modules/nltk/tokenize/casual.html#TweetTokenizer
        # Use the regex based on tweet tokenizer for handles and replace the starting @ with #
        hashtag_re = re.compile(
            r"(?<![A-Za-z0-9_!@#\$%&*])#(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])#(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)", re.UNICODE)

        hashtags = Hashtags()

        for match in hashtag_re.finditer(self.text):

            text = match.group().strip()
            end_index = match.end()
            start_index = end_index - len(text)

            hashtags.add(Hashtag(text=text[1:], indices=[
                         start_index, end_index]))

        return hashtags
