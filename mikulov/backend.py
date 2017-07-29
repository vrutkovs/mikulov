# -*- coding: utf-8 -*-
import logging
import hashlib
import re
import aiofiles
import os
import errno
from uuid import uuid4

logger = logging.getLogger('backend')
POSTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "posts")
TITLE_PATH = "title"
MARKDOWN_PATH = "post.md"
HTML_PATH = "index.html"
TOKEN_PATH = "token"


async def post_digest(title, text):
    m = hashlib.sha256()
    m.update(bytes(title, 'utf-8'))
    m.update(bytes(text, 'utf-8'))
    return m.hexdigest()[:8]


async def save_post(title, text, digest, url_part):
    # Create a directory
    directory = os.path.join(POSTS_PATH, url_part)
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Generate a secret access token
    token = uuid4().hex

    # Write it
    token_path = os.path.join(directory, TOKEN_PATH)
    async with aiofiles.open(token_path, mode='w') as f:
        await f.write(token)

    # Save title to title
    title_path = os.path.join(directory, TITLE_PATH)
    async with aiofiles.open(title_path, mode='w') as f:
        await f.write(title)

    # Save markdown to post.md
    markdown_post_path = os.path.join(directory, MARKDOWN_PATH)
    async with aiofiles.open(markdown_post_path, mode='w') as f:
        await f.write(text)

    #TODO: Convert to HTML

    return (token, url_part)


async def make_a_post(data):
    logger.info("make_a_post")
    title = data['title']
    text = data['text']

    slug = await slugify(title)
    digest = await post_digest(title, text)
    url_part = "{0}-{1}".format(digest, slug)

    return await save_post(title, text, digest, url_part)


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
