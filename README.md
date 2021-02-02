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

1. Determine what type of post we are dealing with:

   - Original Post
   - Echoed Post with No Reply
   - Echoed Post with Reply

2. If original post:

   - Parse post info.
   - Set `echoed_status` to be null.

3. If echoed post with reply, we have to:

   - Parse the reply post as the "main" post.
   - Set `echoed_status` to be the information parsed from the echoed post.

4. If echoed post with no reply:
   - Use the "Echoed by ... " line to get the "main" post information.
   - Grab `username` from the meta information stored in the header.
   - No profile badge can be found in the post this way.
   - Set `echoed_status` to be the information parsed from the echoed post.
   - The `comment_count`, `echo_count`, `upvote_count` belongs to the echoed post.
