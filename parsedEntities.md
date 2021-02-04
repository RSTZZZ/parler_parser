# Parsed Entities

The following are the different entities that are parsed from the parler posts and users.

## Post:

A post object contains the following fields:

| Field                  | Type                  | Nullable | Description                                                                                                                            |
| ---------------------- | --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                   | `str`                 | `false`  | md5Hash of something... still deciding                                                                                                 |
| `parler_post_id`       | `str`                 | `true`   | Parler's post id                                                                                                                       |
| `estimated_created_at` | `str`                 | `false`  | UTC date time of when the post was created at in the format of `YYYY-MM-DD HH:MM:SS`                                                   |
| `timestamp`            | `str`                 | `false`  | Time stamp of post in the HTML                                                                                                         |
| `text`                 | `str`                 | `true`   | The actual UTF-8 text of the post                                                                                                      |
| `user`                 | [`User`](#user)       | `false`  | The user who made the post.                                                                                                            |
| `view_count`           | `int`                 | `true`   | # of impressions / viewers who saw the post. For posts that are simply echoed, no impressions are given                                |
| `hashtags`             | [`Hashtag`](#hashtag) | `true`   | Hashtags extracted from `text`                                                                                                         |
| `mentions`             | [`Mention`](#mention) | `true`   | Mentions extracted from `text`                                                                                                         |
| `media`                | [`Media`](#media)     | `true`   | Any linked media for this post.                                                                                                        |
| `comment_count`        | `int`                 | `true`   | # of comments made to this post                                                                                                        |
| `echo_count`           | `int`                 | `true`   | # of echoes made to this post                                                                                                          |
| `upvote_count`         | `int`                 | `true`   | # of upvotes made to this post                                                                                                         |
| `post_type_id`         | `int`                 | `false`  | ID in [1- 5]. See table below for details.                                                                                             |
| `post_type`            | `int`                 | `false`  | Full name of the post type. See table below for details.                                                                               |
| `echoed_post`          | [`post`](#post)       | `true`   | The echoed `post`. Includes all the same fields except `post_type_id`, `post_type`, `echoed_post`, and `root_echoed_post`.             |
| `root_echoed_post`     | [`post`](#post)       | `true`   | The root of the echoed `post`. Includes all the same fields except `post_type_id`, `post_type`, `echoed_post`, and `root_echoed_post`. |

For examples, see [sample_output](./sample_output.json)

| Post Type ID | Post Type                                     | Description                                                                              |
| ------------ | --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1            | new `post`                                    | A whole new `post` made by the `user`.                                                   |
| 2            | echoed `post`                                 | A `post` the `user` chose to `echo`.                                                     |
| 3            | echoed `post` with `reply`                    | A `post` the `user` chose to `echo` with a `reply`                                       |
| 4            | echoed `post` with root `echo` and no `reply` | A `post` the `user` chose to `echo` which already `echoes` another `post`                |
| 5            | echoed `post` with root `echo` and `reply`    | A `post` the `user` chose to `echo` with a `reply` which already `echoes` another `post` |

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

## Mention

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
      "user_id": "ebf237470e985b2f1a0a8d489743ff96",
      "indices": [11, 18],
      "username": "@sample",
    },
    {
      "user_id": "b7ef7e9117491321ffb55bee54c8deed",
      "indices": [19, 24],
      "username": "@test",
    },
  ]
```

## Media

A medium entity contain the following field:

| Field            | Type   | Nullable | Description                                               |
| ---------------- | ------ | -------- | --------------------------------------------------------- |
| `medium_type_id` | `int`  | `false`  | ID from [1 - 7]. Check table below for detail.            |
| `medium_type`    | `str`  | `false`  | Medium type found. Check table below for possible values. |
| `title`          | `str`  | `true`   | Title that is provided                                    |
| `excerpt`        | `str`  | `true`   | Excerpt that is provided                                  |
| `image_src`      | `str`  | `true`   | Source to the image used.                                 |
| `link_src`       | `str`  | `true`   | Source to the medium                                      |
| `sensitive`      | `bool` | `false`  | Whether the medium is marked sensitive or not             |

A post can have multiple mediums.

The following table explains which field inside the medium type will be null:

| Medium Type ID | Medium Type | Title  | Excerpt | Image Src | Link Src |
| :------------: | ----------- | :----: | :-----: | :-------: | :------: |
|       1        | `article`   |        |         |           |          |
|       2        | `audio`     |        |         |  `null`   |          |
|       3        | `iframe`    |        |         |  `null`   |          |
|       4        | `image`     | `null` | `null`  |           |  `null`  |
|       5        | `link`      | `null` | `null`  |           |          |
|       6        | `video`     |        |         |  `null`   |          |
|       7        | `website`   |        |         |           |          |

Example media parsed from a post with multiple mediums:

```yaml
"media":
  [
    {
      "medium_type_id": 1,
      "medium_type": "article",
      "title": "Global defense contractor IT expert testifies in Italian court he and others switched votes in the U.S. presidential race",
      "excerpt": "Rome, Italy (January 5, 2021) – An employee of the 8th largest global defense contractor, Leonardo SpA, provided a shocking",
      "image_src": "https://images.parler.com/44JxOMm2OXIBT6OoSOgj9z9TWWQFtOuZ",
      "link_src": "https://noqreport.com/2021/01/06/global-defense-contractor-it-expert-testifies-in-italian-court-he-and-others-switched-votes-in-the-u-s-presidential-race/",
      "sensitive": false,
    },
    {
      "medium_type_id": 7,
      "medium_type": "website",
      "title": "Vocaroo | Online voice recorder",
      "excerpt": "Vocaroo is a quick and easy way to share voice messages over the interwebs.",
      "image_src": null,
      "link_src": "https://vocaroo.com/1e976QE4oDoy",
      "sensitive": false,
    },
  ]
```
