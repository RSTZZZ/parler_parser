# Parler Parser

The parler parser is used to parse parler HTML posts and user profiles.

## Parsed Entities:

Refer to [here](./parsedEntities.md)

## Example Run:

```python
import glob
from tqdm import tqdm

from parler.parser.postParser import PostParser
from parler.dataType.post import Post

files = glob.glob('posts/*')

data = []
for idx, file in enumerate(tqdm(files)):
  doc_data = {}

  post = PostParser(file).parse()
  if (post is not None):
    data.append(post.convert())

print(data)
```

## Sample Output

You should get the same results as shown in [sample_output](./sample_output.json).
