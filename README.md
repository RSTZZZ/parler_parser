# Parler Parser

The parler parser is used to parse parler HTML posts and user profiles. Parler post dumps can be found from [here](https://ddosecrets.com/wiki/Parler).

## Parsed Entities:

Refer to [here](./parsedEntities.md)

## Example Run:

```python
import glob

from parler.parser.postParser import PostParser
from parler.dataType.post import Post

files = glob.glob('posts/*')

data = []
for file in files:
  post = PostParser(file).parse()
  if (post is not None):
    data.append(post.convert())

print(data)
```

## Sample Output

You should get the same results as shown in [sample_output](./sample_output.json).

## Parsing Logic

1.  Determine what type of post we are dealing with:

    - New Post
    - Echoed Post
    - Echoed Post with Reply
    - Echoed Post with Root Echo and No Reply
    - Echoed Post with Root Echo and Reply

2.  If `new post`, parse the only post as `main post` else parse the `reply` post as `main post`.

3.  If not `new post`, parse the `echoed post`.

4.  If `echoed post` or `echoed post with root echo and no reply`:

    - Use the "Echoed by ... " line to fill out `main` post info with the `user` and `created_at`
    - Grab `username` from the meta information stored in the header.
    - No profile badge can be found in the post this way.
    - The `comment_count`, `echo_count`, `upvote_count` belongs to the echoed post.

5.  Else:

    - The `comment_count`, `echo_count`, `upvote_count` belongs to the `main` post.

6.  If `Echoed Post with Root Echo and No Reply` or `Echoed Post with Root Echo and Reply`:

    - Parse the `first` post for the `root echo`.
