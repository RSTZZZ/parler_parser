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

You should get the same results as shown in [sample_output](./sample_output.json)
