
from typing import Dict

import hashlib


class Util:

    @staticmethod
    def convert(data):
        '''
        Helper Function to call convert on the object. Return None if object is None.
        '''

        if (data is None):
            return None
        else:
            return data.convert()

    @staticmethod
    def to_int(data):
        '''
        Helper function to convert object to int. Return None if object is none.
        '''
        if (data is None):
            return None
        else:
            return int(data)

    @staticmethod
    def compress_dict(dictionary: Dict):
        for _, v in dictionary.items():
            if v is not None:
                return dictionary
        return None

    @staticmethod
    def return_none_on_error(function):
        '''
        Helper Function to return None if error
        '''

        def inner(self):
            try:
                return function(self)
            except Exception:
                return None
        return inner

    @staticmethod
    def get_md5Hash(text) -> str:
        '''
        Generates the md5Hash in the format of hex digest given the text to hash.
        '''
        md5Hash = hashlib.md5(text.encode())
        return md5Hash.hexdigest()
