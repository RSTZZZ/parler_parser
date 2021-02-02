# Parler Parser

The parler parser is used to parse parler posts from base HTML files.

# Example Run:

```python
import glob

from tqdm import tqdm
from bs4 import BeautifulSoup

from parler.parser.postParser import PostParser
from parler.dataType.post import Post

files = glob.glob('posts/*')

data = []
for idx, file in enumerate(tqdm(files)):
  doc_data = {}

  post = PostParser(file).parse()
  if (post is not None):
    data.append(post.convert())

data
```

You should get the same results as shown in [sample_output](./sample_output.json) or:

```yaml
[
  {
    "created_at": null,
    "id": "",
    "text": null,
    "user":
      {
        "user_id": "b7f0a482553a2cc8102d34703f190f25",
        "photo": "https://images.parler.com/fcf0b8932bd540e4a6a7a2a8ff9523e3_256",
        "badge": null,
        "name": "Ppapin83",
        "username": "@Ppapin83",
        "description": null,
        "description_hashtags": null,
      },
    "view_count": null,
    "hashtags": [],
    "mentions": [],
    "media": null,
    "comment_count": "418",
    "echo_count": "2130",
    "upvote_count": "4815",
    "post_type": 2,
    "echoed_status": null,
  },
  {
    "created_at": null,
    "id": "",
    "text": null,
    "user":
      {
        "user_id": "0aa3b9f9d557b78ff671b4604f88378b",
        "photo": "https://images.parler.com/cdd1853c6c6342828b46ad22390120e5_256",
        "badge": null,
        "name": "Grace Cochran",
        "username": "@eagleandcrow",
        "description": null,
        "description_hashtags": null,
      },
    "view_count": null,
    "hashtags": [],
    "mentions": [],
    "media": null,
    "comment_count": "1067",
    "echo_count": "7329",
    "upvote_count": "16871",
    "post_type": 2,
    "echoed_status": null,
  },
  {
    "created_at": "4 days ago",
    "id": "",
    "text": "Who authorizes these stoppages??? Whoever it is is part of the steal....",
    "user":
      {
        "user_id": "b153129f372ab4b5f339d09128b7f4f2",
        "photo": "https://images.parler.com/56d4eb4dc50f49ba94ad0059f9e1d56f_256",
        "badge": "Citizen",
        "name": "Glcalahan",
        "username": "@Glcalahan",
        "description": null,
        "description_hashtags": null,
      },
    "view_count": "315",
    "hashtags": [],
    "mentions": [],
    "media": null,
    "comment_count": "5589",
    "echo_count": "7356",
    "upvote_count": "26306",
    "post_type": 3,
    "echoed_status":
      {
        "created_at": "4 days ago",
        "id": "",
        "text": "Who authorizes these stoppages??? Whoever it is is part of the steal....",
        "user":
          {
            "user_id": "b153129f372ab4b5f339d09128b7f4f2",
            "photo": "https://images.parler.com/56d4eb4dc50f49ba94ad0059f9e1d56f_256",
            "badge": "Citizen",
            "name": "Glcalahan",
            "username": "@Glcalahan",
            "description": null,
            "description_hashtags": null,
          },
        "view_count": "315",
        "hashtags": [],
        "mentions": [],
        "media": null,
      },
  },
  {
    "created_at": "4 days ago",
    "id": "",
    "text": "President DJT 11AM",
    "user":
      {
        "user_id": "c258dcf092a40f5466022ea949bdb107",
        "photo": "https://images.parler.com/b5aacbd1ae4c4253a1b2b40318064def_256",
        "badge": null,
        "name": "jjdrrmfr",
        "username": "@jjdrrmfre",
        "description": null,
        "description_hashtags": null,
      },
    "view_count": "17",
    "hashtags": [],
    "mentions": [],
    "media":
      {
        "article": null,
        "audio": null,
        "image": null,
        "link":
          {
            "src": "https://twitter.com/realdonaldtrump/status/1346588064026685443?s=12",
            "image": "/512ae92f/images/icons/link.svg",
          },
        "video": null,
      },
    "comment_count": "0",
    "echo_count": "1",
    "upvote_count": "1",
    "post_type": 1,
    "echoed_status": null,
  },
]
```
