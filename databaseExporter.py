from pymongo import MongoClient
from loguru import logger

from parler.dataType.post import Post


class DatabaseExporter:
    '''
    Used to help export information to the respective databases.
    '''

    def __init__(self, username, pwd, hostname, port, db_name):
        mongo_db_uri = self.create_mongo_db_uri(username, pwd, hostname, port)

        self.client = MongoClient(mongo_db_uri)
        self.db = self.client[db_name]
        self.postDB = self.db.posts
        self.userDB = self.db.users
        self.hashtagDB = self.db.hashtag_relations
        self.mentionDB = self.db.mention_relations
        self.quoteDB = self.db.quote_relations
        self.retweetDB = self.db.retweet_relations

    def create_mongo_db_uri(self, username, pwd, hostname, port):
        '''
        Creates mongodb URI connection string
        '''
        return f"mongodb://{username}:{pwd}@{hostname}:{port}"

    def insert_user(self, user):
        '''
        Insert user if it doesn't exist.
        '''
        user_query = {'user_id': user['user_id']}
        existing_user = self.userDB.find_one(user_query)

        if (existing_user is None):
            self.userDB.insert_one(user)
        else:
            if (existing_user["badge"] is None and user["badge"] is not None):
                self.userDB.update_one(
                    user_query, {"$set": {"badge": user["badge"]}})

    def insert_hashtags_relation(self, hashtags, user_id, username, post_id, post_estimated_created_at):
        '''
        Insert hashtag_relation if it doesn't exist.
        '''
        for hashtag in hashtags:

            existing_hashtag_relation = self.hashtagDB.find_one(
                {
                    "post_id": post_id,
                    "hashtag_text": hashtag['text']
                }
            )

            if (existing_hashtag_relation is None):

                hashtag_relation = {
                    "user_id": user_id,
                    "username": username,
                    "hashtag_id": hashtag['hashtag_id'],
                    "hashtag_text": hashtag['text'],
                    "hashtag_indices": hashtag["indices"],
                    "post_id": post_id,
                    "post_estimated_created_at": post_estimated_created_at
                }

                self.hashtagDB.insert_one(hashtag_relation)

    def insert_mentions_relation(self, mentions, user_id, username, post_id, post_estimated_created_at):
        '''
        Insert mention_relations if it doesn't exist.
        '''
        for mention in mentions:

            existing_mention_relation = self.mentionDB.find_one(
                {
                    "post_id": post_id,
                    "mentioned_username": mention["username"]
                }
            )

            if (existing_mention_relation is None):

                mention_relation = {
                    "user_id": user_id,
                    "username": username,
                    "mentioned_user_id": mention["user_id"],
                    "mentioned_username": mention["username"],
                    "post_id": post_id,
                    "post_estimated_created_at": post_estimated_created_at
                }

                self.mentionDB.insert_one(mention_relation)

    def insert_quote_relation(self, quoted_user_id, quoted_username, quoted_post_id, user_id, username, post_id, post_estimated_created_at):
        '''
        Insert quote relation if it doesn't exist.
        '''
        existing_quote_relation = self.quoteDB.find_one(
            {
                "quoted_post_id": quoted_post_id,
                "post_id": post_id
            }
        )

        if (existing_quote_relation is not None):
            return

        quote_relation = {
            "user_id": user_id,
            "username": username,
            "quoted_user_id": quoted_user_id,
            "quoted_username": quoted_username,
            "quoted_post_id": quoted_post_id,
            "post_id": post_id,
            "post_estimated_created_at": post_estimated_created_at
        }

        self.quoteDB.insert_one(quote_relation)

    def insert_retweet_relation(self, retweeted_user_id, retweeted_username, retweeted_post_id, user_id, username, post_id, post_estimated_created_at):
        '''
        Insert retweet relation if it doesn't exist.
        '''

        existing_retweet_relation = self.retweetDB.find_one(
            {
                "retweeted_post_id": retweeted_post_id,
                "post_id": post_id
            }
        )

        if (existing_retweet_relation is not None):
            return

        retweet_relation = {
            "user_id": user_id,
            "username": username,
            "retweeted_user_id": retweeted_user_id,
            "retweeted_username": retweeted_username,
            "retweeted_post_id": retweeted_post_id,
            "post_id": post_id,
            "post_estimated_created_at": post_estimated_created_at
        }

        self.retweetDB.insert_one(retweet_relation)

    def get_max_count(self, old_count, new_count):

        if (new_count is None):
            return old_count

        if (old_count is None):
            return new_count

        if (new_count > old_count):
            return new_count
        else:
            return old_count

    def insert_base_post_into_db(self, post):
        '''
        Insert post into the db and return its object id
        '''

        post_query = {'post_hash': post['post_hash']}
        existing_post = self.postDB.find_one(post_query)

        # Return post if it already exists.
        # Update comment_count, echo_count, and upvote_count if greater.
        if (existing_post is not None):

            self.postDB.update_one(post_query,
                                   {"$set": {"comment_count": self.get_max_count(existing_post["comment_count"], post["comment_count"]),
                                             "echo_count": self.get_max_count(existing_post["echo_count"], post["echo_count"]),
                                             "upvote_count": self.get_max_count(existing_post["upvote_count"], post["upvote_count"]),
                                             }
                                    }
                                   )

            return existing_post['_id']

        # 1. Insert User
        post_user = post["user"]
        self.insert_user(post_user)

        # 2. Insert Post
        new_post = self.postDB.insert_one(post)

        # 3. Insert the hashtags
        self.insert_hashtags_relation(post["hashtags"],
                                      post_user["user_id"],
                                      post_user["username"],
                                      new_post.inserted_id,
                                      post["estimated_created_at"])

        # 4. Insert the mentions
        self.insert_mentions_relation(post["mentions"],
                                      post_user["user_id"],
                                      post_user["username"],
                                      new_post.inserted_id,
                                      post["estimated_created_at"]
                                      )

        return new_post.inserted_id

    def insert_echoed_post_into_db(self, echoed_post):
        '''
        Insert the echoed post into the database.
        '''
        # Add fields for the echoed_post
        echoed_post["post_type_id"] = Post.ORIGINAL
        echoed_post["post_type"] = "new post"
        echoed_post["echoed_post"] = None
        echoed_post["root_echoed_post"] = None

        return self.insert_base_post_into_db(echoed_post)

    def insert_root_echoed_post_into_db(self, root_echoed_post, echoed_post):
        '''
        Inserts the root echoed post and the echoed post into the db.
        '''

        # Update echoed_post
        echoed_post["post_type_id"] = Post.ECHO_WITH_REPLY
        echoed_post["post_type"] = "echoed post with reply"
        echoed_post["echoed_post"] = root_echoed_post
        echoed_post["root_echoed_post"] = None
        echoed_post_id = self.insert_base_post_into_db(echoed_post)

        # Add fields for the root_echoed_post
        root_echoed_post["post_type_id"] = Post.ORIGINAL
        root_echoed_post["post_type"] = "new post"
        root_echoed_post["echoed_post"] = None
        root_echoed_post["root_echoed_post"] = None
        root_echoed_post_id = self.insert_base_post_into_db(root_echoed_post)

        return echoed_post_id, root_echoed_post_id

    def insert_original_post(self, post):
        self.insert_base_post_into_db(post)

    def insert_echoed_no_reply_post(self, post):
        # Insert echoed post first and replace it with the id.
        echoed_post = post["echoed_post"]
        echoed_post_id = self.insert_echoed_post_into_db(echoed_post)
        post["echoed_post"] = echoed_post_id

        # Insert outside post
        post_id = self.insert_base_post_into_db(post)

        # Add retweet_relation
        self.insert_retweet_relation(retweeted_user_id=echoed_post["user"]["user_id"],
                                     retweeted_username=echoed_post["user"]["username"],
                                     retweeted_post_id=echoed_post_id,
                                     user_id=post["user"]["user_id"],
                                     username=post["user"]["username"],
                                     post_id=post_id,
                                     post_estimated_created_at=post["estimated_created_at"])

    def insert_echoed_with_reply_post(self, post):
        # Insert echoed post first and replace it with the id.
        echoed_post = post["echoed_post"]
        echoed_post_id = self.insert_echoed_post_into_db(echoed_post)
        post["echoed_post"] = echoed_post_id

        # Insert outside post
        post_id = self.insert_base_post_into_db(post)

        # Add quoted relation
        self.insert_quote_relation(quoted_user_id=echoed_post["user"]["user_id"],
                                   quoted_username=echoed_post["user"]["username"],
                                   quoted_post_id=echoed_post_id,
                                   user_id=post["user"]["user_id"],
                                   username=post["user"]["username"],
                                   post_id=post_id,
                                   post_estimated_created_at=post["estimated_created_at"])

    def insert_root_echoed_no_reply(self, post):
        # Insert echoed and root echoed post and replace with ID.
        echoed_post = post["echoed_post"]
        root_echoed_post = post["root_echoed_post"]
        echoed_post_id, root_echoed_post_id = self.insert_root_echoed_post_into_db(
            root_echoed_post, echoed_post)

        post["echoed_post"] = echoed_post_id
        post["root_echoed_post"] = root_echoed_post_id

        # Insert outside post
        post_id = self.insert_base_post_into_db(post)

        # Insert quoted relation -> echo is quoting root
        self.insert_quote_relation(quoted_user_id=root_echoed_post["user"]["user_id"],
                                   quoted_username=root_echoed_post["user"]["username"],
                                   quoted_post_id=root_echoed_post_id,
                                   user_id=echoed_post["user"]["user_id"],
                                   username=echoed_post["user"]["username"],
                                   post_id=echoed_post_id,
                                   post_estimated_created_at=echoed_post["estimated_created_at"])

        # Insert retweeted relation -> main post is retweeting echo
        self.insert_retweet_relation(retweeted_user_id=echoed_post["user"]["user_id"],
                                     retweeted_username=echoed_post["user"]["username"],
                                     retweeted_post_id=echoed_post_id,
                                     user_id=post["user"]["user_id"],
                                     username=post["user"]["username"],
                                     post_id=post_id,
                                     post_estimated_created_at=post["estimated_created_at"])

    def insert_root_echoed_with_reply(self, post):
        # Insert echoed and root echoed post and replace with ID.
        echoed_post = post["echoed_post"]
        root_echoed_post = post["root_echoed_post"]
        echoed_post_id, root_echoed_post_id = self.insert_root_echoed_post_into_db(
            root_echoed_post, echoed_post)

        post["echoed_post"] = echoed_post_id
        post["root_echoed_post"] = root_echoed_post_id

        # Insert outside post
        post_id = self.insert_base_post_into_db(post)

        # Insert quoted relation -> echo is quoting root
        self.insert_quote_relation(quoted_user_id=root_echoed_post["user"]["user_id"],
                                   quoted_username=root_echoed_post["user"]["username"],
                                   quoted_post_id=root_echoed_post_id,
                                   user_id=echoed_post["user"]["user_id"],
                                   username=echoed_post["user"]["username"],
                                   post_id=echoed_post_id,
                                   post_estimated_created_at=echoed_post["estimated_created_at"])

        # Insert quoted relation -> main post is retweeting echo
        self.insert_quote_relation(quoted_user_id=echoed_post["user"]["user_id"],
                                   quoted_username=echoed_post["user"]["username"],
                                   quoted_post_id=echoed_post_id,
                                   user_id=post["user"]["user_id"],
                                   username=post["user"]["username"],
                                   post_id=post_id,
                                   post_estimated_created_at=post["estimated_created_at"])

    @logger.catch
    def insert_post(self, post):
        # Determine the type of post this is
        post_type = post['post_type_id']

        if (post_type == Post.ORIGINAL):
            self.insert_original_post(post)

        if (post_type == Post.ECHO_NO_REPLY):
            self.insert_echoed_no_reply_post(post)

        if (post_type == Post.ECHO_WITH_REPLY):
            self.insert_echoed_with_reply_post(post)

        if (post_type == Post.ECHO_WITH_ROOT_AND_NO_REPLY):
            self.insert_root_echoed_no_reply(post)

        if (post_type == Post.ECHO_WITH_ROOT_AND_REPLY):
            self.insert_root_echoed_with_reply(post)
