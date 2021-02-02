import os
from urllib.parse import urlparse

import parler.parser.htmlParser as htmlParser

badge_map = {
    "00.svg": "Citizen",
    "01.svg": "Influencer",
    "02.svg": "Partnership",
    "03.svg": "Affiliate",
    "04.svg": "Locked",
    "05.svg": "Citizen Restricted Comments",
    "06.svg": "What is this",
    "07.svg": "Employee",
    "09.svg": "Early Adopter"
}


def parse_parler_badge(html_element):
    '''
    Gets the parler profile badge located inside the html_element.
    '''
    badge_url = htmlParser.get_image_src(html_element, {'alt': 'Badge'})

    if badge_url == "" or badge_url is None:
        return None

    badge = urlparse(badge_url)

    try:
        badge_image = os.path.basename(badge.path)
        return badge_map[badge_image]
    except:
        return None
