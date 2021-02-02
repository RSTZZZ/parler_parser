import os
from urllib.parse import urlparse

import html_parser


def is_echo(soup):
    '''
    Use soup to test if this post is an echo.
    '''
    return soup.find('div', {'class': 'echo-byline--wrapper'}) is not None


def echo_has_post(soup):
    '''
    Use soup to ttest if the echoed post has any text.
    '''
    return get_container(soup, 'span.reblock.post') is not None


def article_exist(container):
    '''
    Check if the article exists inside the container.
    '''
    return container.find('span', {'class': 'mc-article--title'}) is not None


def link_exist(container):
    '''
    Check if there is a link inside the container.
    '''
    return container.find('span', {'class': 'mc-basic--link'}) is not None


def video_exist(container):
    '''
    Check if there is a linked video inside the container.
    '''
    return container.find('span', {'class': 'mc-video--title'}) is not None


def get_post_article(container):
    '''
    Use soup to get post article if any.
    '''
    if (not article_exist(container)):
        return None

    article_title = get_text(container, 'span', {'class': 'mc-article--title'})
    article_excerpt = get_text(
        container, 'span', {'class': 'mc-article--excerpt'})
    article_link = get_link(container, 'span', {'class': 'mc-article--link'})
    article_image = get_image_src(container, {'alt': "Article Image"})

    return {
        "title": article_title,
        "excerpt": article_excerpt,
        "link": article_link,
        "image": article_image
    }


def get_post_link(container):
    '''
    Use soup to get post link if any.
    '''
    if (not link_exist(container)):
        return None

    link_container = get_container(container, 'span.mc-basic--link')
    post_link = get_text(link_container, 'a', {}).strip()
    post_image = get_image_src(container, {'class': 'mc-basic--image'},
                               html_tag="div")

    return {"url": post_link, "image": post_image}


def get_post_video(container):
    '''
    Use soup to get video link if any.
    '''
    if (not video_exist(container)):
        return None

    video_title = get_text(container, 'span', {'class': 'mc-video--title'})
    video_excerpt = get_text(container, 'span', {'class': 'mc-video--excerpt'})
    video_src = get_video_src(container, {'class': 'mc-video--wrapper'})
    return {
        "title": video_title,
        "excerpt": video_excerpt,
        "src": video_src
    }


def check_parler_badge(container):
    '''
    Use soup to get the parler badge from container if exists.
    '''
    badge_map = {
        "00.svg": "Citizen",
        "01.svg": "Influencer",
        "02.svg": "Partnership",
        "03.svg": "Affliate",
        "04.svg": "Locked",
        "05.svg": "Citizen Restricted Comments",
        "06.svg": "What is this",
        "07.svg": "Employee",
        "09.svg": "Early Adopter"
    }

    badge_url = get_image_src(container, {'alt': 'Badge'})

    if badge_url == "":
        return None

    badge = urlparse(badge_url)

    try:
        badge_image = os.path.basename(badge.path)
        return badge_map[badge_image]
    except:
        return None


def get_post_info_from_container(container):
    '''
    Use container to get post information.
        -> Photo
        -> Badge
        -> Name
        -> Username
        -> Timestamp
        -> Impressions
        -> Text
        -> Article
        -> Link
        -> Video
    '''
    if (container is None):
        return None

    profile_pic = get_image_src(container, {'alt': 'Post Author Profile Pic'})
    profile_badge = check_parler_badge(container)

    name = get_text(container, 'span', {'class': 'author--name'})
    username = get_text(container, 'span', {'class': 'author--username'})

    timestamp = get_text(container, 'span', {'class': 'post--timestamp'})
    impressions = get_text(container, 'span', {'class': 'impressions--count'})

    text = get_paragraph(container, 'div',  {'class': 'card--body'})

    article = get_post_article(container)
    link = get_post_link(container)
    video = get_post_video(container)

    return {
        "profile_photo": profile_pic,
        "profile_badge": profile_badge,
        "name": name,
        "username": username,
        "timestamp": timestamp,
        "impressions": impressions,
        "text": text,
        "article": article,
        "link": link,
        "video": video,
    }


def get_echoed_info(soup):
    '''
    Use container to get post information.
        -> Photo
        -> Badge
        -> Name
        -> Username
        -> Timestamp
        -> Impressions
        -> Text
        -> Article
        -> Link
        -> Video
    '''
    container = get_container(soup, 'div.echo-byline--wrapper')

    profile_pic = get_image_src(container, {'class': 'eb--profile-pic'})

    # start at 10 since it always starts with "Echoed By "
    name = get_text(container, 'span', {'class': 'reblock'})[10:]

    # In the meta field, we can find the username..
    username = soup.find('meta', {"name": "twitter:title"}).get(
        'content', '').split()[0]
    timestamp = get_text(container, 'span', {'class': 'reblock'}, index=1)

    return {
        "profile_photo": profile_pic,
        "profile_badge": None,
        "name": name,
        "username": username,
        "timestamp": timestamp,
        "impressions": None,
        "text": None,
        "article": None,
        "link": None,
        "video": None,
    }


def get_main_post_info(soup):
    '''
    Inside soup, get the main post information.
        -> Original poster
        -> Echo poster
        -> The echo line with the rest not filled.
    '''
    if (is_echo(soup) and not echo_has_post(soup)):

        return get_echoed_info(soup)

    main_post_container = get_container(soup, 'span.reblock.post')
    return get_post_info_from_container(main_post_container)


def get_post_reactions(soup):
    comments = get_text(soup, 'span', {'class': 'pa--item--count'}, index=0)
    echoes = get_text(soup, 'span', {'class': 'pa--item--count'}, index=1)
    upvotes = get_text(soup, 'span', {'class': 'pa--item--count'}, index=2)

    return {"comments": comments,
            "echoes": echoes,
            "upvotes": upvotes
            }
