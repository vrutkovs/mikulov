# -*- coding: utf-8 -*-
import logging
import hashlib
import re

logger = logging.getLogger('backend')


async def post_digest(title, text):
    m = hashlib.sha256()
    m.update(bytes(title, 'utf-8'))
    m.update(bytes(text, 'utf-8'))
    return m.hexdigest()[:8]

async def save_post(title, text, digest, url_part):

    return True

async def make_a_post(data):
    logger.info("make_a_post")
    title = data['title']
    text = data['text']

    slug = await slugify(title)
    digest = await post_digest(title, text)
    # TODO: throw exception if the folder already exists
    url_part = "{0}-{1}".format(digest, slug)

    result = await save_post(title, text, digest, url_part)
    assert result

    return (
        "wubbadubbadubdubs",
        url_part
    )


async def slugify(s):
    """
    http://blog.dolphm.com/slugify-a-string-in-python/
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some-articles-title"
    s = s.replace(' ', '-')
    return s
