from bs4 import BeautifulSoup

DEFAULT_VALUE = None


def try_except(function):
    '''
    Specific helper function to
    '''
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except AttributeError:
            return DEFAULT_VALUE
    return inner


def get_html_doc(html_file):
    return BeautifulSoup(html_file, 'html.parser')


@try_except
def get_element_by_css(html_element, css_selector):
    '''
    Get the appropriate HTML element and its child elements specified by the css_selector
    '''
    return html_element.select_one(css_selector)


@try_except
def get_all_elements(html_element, html_tag, html_attribute):
    '''
    Get all HTML elements that match the html_tag and html_attribute
    '''
    return html_element.find_all(html_tag, html_attribute)


@try_except
def get_content(html_element,  html_tag, html_attribute):
    '''
    Get the appropriate HTML element and its child elements specified by the css_selector
    '''
    return html_element.find(html_tag, html_attribute).get('content', '')


@try_except
def get_image_src(html_element, html_attribute, html_tag="img"):
    '''
    Get the appropriate image source specified by the html_tag and html_attribute in the provided HTML element.
    html_tag is optional with default value of 'img'
    '''
    if (html_tag == "img"):
        return html_element.find(html_tag, html_attribute).get('src', '')

    return html_element.find(html_tag, html_attribute).find('img').get('src', '')


@try_except
def get_link(html_element, html_tag, html_attribute):
    '''
    Get the appropriate link (href) specified by the html_tag and html_attribute in the provided HTML element.
    '''
    return html_element.find(html_tag, html_attribute).find('a').get('href', '')


@try_except
def get_paragraph(html_element, html_tag, html_attribute):
    '''
    Get the appropriate paragraph text specified by the html_tag and html_attribute in the provided HTML element.
    '''
    return html_element.find(html_tag, html_attribute).find('p').get_text(" ")


@try_except
def get_text(html_element, html_tag, html_attribute, index=-1):
    '''
    Get the appropriate text by the html_tag and html_attribute in the provided HTML element.
    Provide index if more than one matches the critera from html_tag and html_attribute.
    '''
    if (index > 0):
        return html_element.find_all(html_tag, html_attribute)[index].get_text(" ")
    else:
        return html_element.find(html_tag, html_attribute).get_text(" ")


@try_except
def get_video_src(html_element, html_attribute, html_tag="div"):
    '''
    Get the appropriate video source specified by the html_tag and html_attribute in the provided HTML element.
    html_tag is optional with default value of 'div'
    '''
    return html_element.find(html_tag, html_attribute).find('video').find('source').get('src', '')
