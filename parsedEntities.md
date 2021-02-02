# Parsed Entities

The following are the different entities that are parsed from the parler posts and users.

## Post:

A post object contains the following fields:

| Field           | Type                  | Nullable | Description                                                                                             |
| --------------- | --------------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `created_at`    | `str`                 | `false`  | Time stamp of post in the HTML                                                                          |
| `id`            | `str`                 | `false`  | md5Hash of something... still deciding                                                                  |
| `text`          | `str`                 | `true`   | The actual UTF-8 text of the post                                                                       |
| `user`          | [`User`](#user)       | `false`  | The user who made the post.                                                                             |
| `view_count`    | `int`                 | `true`   | # of impressions / viewers who saw the post. For posts that are simply echoed, no impressions are given |
| `hashtags`      | [`Hashtag`](#hashtag) | `true`   | Hashtags extracted from `text`                                                                          |
| `mentions`      | [`Mention`](#mention) | `true`   | Mentions extracted from `text`                                                                          |
| `media`         | [`Media`](#media)     | `true`   | Any linked media for this post.                                                                         |
| `comment_count` | `int`                 | `true`   | # of comments made to this post                                                                         |
| `echo_count`    | `int`                 | `true`   | # of echoes made to this post                                                                           |
| `upvote_count`  | `int`                 | `true`   | # of upvotes made to this post                                                                          |
| `post_type`     | `int`                 | `true`   | `1` - original post, `2` - post that echoes without a reply, `3` - post that echoes without a reply     |
| `echoed_status` | [`post`](#post)       | `true`   | The echoed `post`. Includes all the same fields except `post_type` and `echoed_status`                  |

For examples, see [sample_output](./sample_output.json)

## User:

A user object contains the following fields:

| Field                  | Type                  | Nullable | Description                                                                                                                                             |
| ---------------------- | --------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_id`              | `str`                 | `false`  | md5 hash of the `username`                                                                                                                              |
| `photo`                | `str`                 | `false`  | url source for the image                                                                                                                                |
| `badge`                | `str`                 | `true`   | Can be one of ["Citizen", "Influencer", "Partnership", "Affiliate","Locked", "Citizen Restricted Comments","What is this","Employee", "Early Adopter" ] |
| `name`                 | `str`                 | `false`  | user defined name (has spaces)                                                                                                                          |
| `username`             | `str`                 | `false`  | unique name                                                                                                                                             |
| `description`          | `str`                 | `true`   | user bio                                                                                                                                                |
| `description_hashtags` | [`Hashtag`](#hashtag) | `true`   | Hashtags extracted from the description.                                                                                                                |

Example User converted to json:

```yaml
"user":
  {
    "user_id": "b7f0a482553a2cc8102d34703f190f25",
    "photo": "https://images.parler.com/fcf0b8932bd540e4a6a7a2a8ff9523e3_256",
    "badge": null,
    "name": "Ppapin83",
    "username": "@Ppapin83",
    "description": null,
    "description_hashtags": null,
  }
```

## Hashtag:

A hashtag entity contain the following fields:

| Field        | Type         | Nullable | Description                                    |
| ------------ | ------------ | -------- | ---------------------------------------------- |
| `hashtag_id` | `str`        | `false`  | md5 hash of the `text`                         |
| `indices`    | `[int, int]` | `false`  | [`start`, `end`] of where the hashtag is found |
| `text`       | `str`        | `false`  | the hashtag without `#`                        |

Example hashtags given sentence: `"This is my #sample #test!"`

```yaml
"description_hashtags":
  [
    {
      "hashtag_id": "5e8ff9bf55ba3508199d22e984129be6",
      "indices": [11, 18],
      "text": "sample",
    },
    {
      "hashtag_id": "098f6bcd4621d373cade4e832627b4f6",
      "indices": [19, 24],
      "text": "test",
    },
  ]
```

## Mention Entity

A mention entity contain the following fields:

| Field      | Type         | Nullable | Description                                    |
| ---------- | ------------ | -------- | ---------------------------------------------- |
| `user_id`  | `str`        | `false`  | md5 hash of the `username`                     |
| `indices`  | `[int, int]` | `false`  | [`start`, `end`] of where the mention is found |
| `username` | `str`        | `false`  | the username that is mentioned                 |

Example mentions given sentence: `"This is my @sample @test!"`

```yaml
"mentions":
  [
    {
      "hashtag_id": "ebf237470e985b2f1a0a8d489743ff96",
      "indices": [11, 18],
      "text": "@sample",
    },
    {
      "hashtag_id": "b7ef7e9117491321ffb55bee54c8deed",
      "indices": [19, 24],
      "text": "@test",
    },
  ]
```

## Media

A media entity contain the following field:

- Usually only one is filled...

| Field     | Type    | Nullable | Description                                                                                                                                                               |
| --------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `article` | `str`   | `true`   | A linked article in the post: `{ "title" : "example title", "excerpt" : "example excerpt", "src" : "url source to the article", "image" "image source for the website" }` |
| `audio`   | `Audio` | `true`   | A linked audio in the post: `{"title": "example title", "excerpt": "example excerpt", "src": "url source to the audio",}`                                                 |
| `image`   | `str`   | `true`   | The url source to the linked image                                                                                                                                        |
| `link`    | `str`   | `true`   | A linked link:`{ "src" : "url source to the link", "image" "image source for the link"}`                                                                                  |
| `video`   | `Video` | `true`   | A linked video in the post: `{ "title": "example title", "excerpt": "example excerpt", "src": "url source to the video",}`                                                |
