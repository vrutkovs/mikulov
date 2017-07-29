# -*- coding: utf-8 -*-
import logging
import sys
import hashlib
import re


logger = logging.getLogger(__name__)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(name)-15s: %(filename)s:%(lineno)-3d: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger('backend')


async def post_digest(title, text):
    m = hashlib.sha256()
    m.update(title)
    m.update(text)
    return m.hexdigest()[:8]


async def make_a_post(data):
    logger.info("make_a_post")
    title = data['title']
    text = data['text']

    slug = await slugify(title)
    digest = await post_digest(title, text)
    # TODO: throw exception if the folder already exists
    url_part = "{0}-{1}".format(digest, slug)

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
