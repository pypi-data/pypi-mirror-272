# libreppc 

A simple profile page creator. You can see themes examples [here](docs/themes.md).

## Installation

```sh
$ pip install libreppc
$ python -m libreppc --serve
```

## Getting started

You need to create `config.json`:

**config.json** structure
```json
{
    "theme" : "CSS_FILE_NAME_WITHOUT_.css",
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
            "title" : "projectname",
            "description" : "projectdescription",
            "filename" : "page"
        }
    ]
}
```

You also can generate config via:

```sh
$ python -m libreppc --init
```

Then you need to build site with:

```sh
$ python -m libreppc --build
```

## Contacts

| Contact                                               | Description       |
| :---:                                                 | :---              |
| [`Matrix`](https://matrix.to/#/#librehub:matrix.org)  | Matrix server     |

## Support

You can support us [here](https://warlock.codeberg.page).


