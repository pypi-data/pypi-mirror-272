
DEFAULT_CONFIG = {
    "theme" : "mastodon",
    "avatar" : "https://avatar-url.com",
    "username" : "yourusername",
    "description" : "yourdescription",
    "base_url" : "yourpageurl",
    "static_dir" : "static",
    "blog" : {
        "dir" : "blog",
        "title" : "Blog"
    },
    "icons" : [
        {
            "title" : "linktitle",
            "icon" : "iconurl",
            "url" : "linkurl"
        },
    ],
    "fields" : [
        {
            "title" : "Monero/XMR",
            "type" : "text",
            "target" : "yourcryptoaddress"
        },
        {
            "title" : "Patreon",
            "type" : "url",
            "target" : "https://patreon.com/"
        },
    ],
    "pages" : [
        {
            "title" : "pagename",
            "description" : "pagedescription",
            "filename" : "page"
        }
    ]
}

DEFAULT_BLOG_POST = """| title             | description                   | date              | author            |
| :---              | :---                          | :---              | :---              |
| Introduction      | First post on my blog page    | Today (changeme)  | You (changeme)    |

This is my introduction to libreppc!
"""

DEFAULT_PAGE = """
Hey! This is my cool project! Are you enjoyed?
"""

