from parler.dataType.mediaTypes.article import Article

import parler.parser.htmlParser as htmlParser


class ArticleParser:
    '''
    Parse the article inside media container in the post.
    '''

    def __init__(self, post):
        self.post = post

    def parse(self):
        return Article(
            title=self.get_title(),
            excerpt=self.get_excerpt(),
            src=self.get_src(),
            image=self.get_image(),
        )

    def get_title(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-article--title'})

    def get_excerpt(self):
        return htmlParser.get_text(self.post, 'span', {'class': 'mc-article--excerpt'})

    def get_src(self):
        return htmlParser.get_link(self.post, 'span', {'class': 'mc-article--link'})

    def get_image(self):
        return htmlParser.get_image_src(self.post, 'span', {'alt': "Article Image"})
