# -*- coding: utf-8 -*-
import logging
import hashlib
import re
import aiofiles
import os
import errno
import shutil
import markdown2
from uuid import uuid4

logger = logging.getLogger('backend')
POSTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "posts")
TITLE_PATH = "title"
MARKDOWN_PATH = "post.md"
HTML_PATH = "index.html"
TOKEN_PATH = "token"
EXTRAS = [
    "break-on-newline", "fenced-code-blocks", "header-ids", "smarty-pants", "target-blank-links",
    "toc"
]


class PostAlreadyExists(Exception):
    pass


async def post_digest(title, text):
    m = hashlib.sha256()
    m.update(bytes(title, 'utf-8'))
    m.update(bytes(text, 'utf-8'))
    return m.hexdigest()[:8]


async def save_post(title, text, digest, url_part):
    # Create a directory
    directory = os.path.join(POSTS_PATH, url_part)
    if os.path.exists(directory):
        raise PostAlreadyExists()
    os.makedirs(directory)

    # Generate a secret access token
    token = uuid4().hex

    # Write it
    token_path = os.path.join(directory, TOKEN_PATH)
    async with aiofiles.open(token_path, mode='w') as f:
        await f.write(token)

    # Save title to title file
    title_path = os.path.join(directory, TITLE_PATH)
    async with aiofiles.open(title_path, mode='w') as f:
        await f.write(title)

    # Save markdown to post.md
    markdown_post_path = os.path.join(directory, MARKDOWN_PATH)
    async with aiofiles.open(markdown_post_path, mode='w') as f:
        await f.write(text)

    # Convert markdown to HTML and save it
    html_post_path = os.path.join(directory, HTML_PATH)
    await convert_markdown(text, html_post_path)

    return (token, url_part)


async def get_post(digest, slug):
    logger.info("get_post")

    directory = await get_post_directory(digest, slug)

    title_post_path = os.path.join(directory, TITLE_PATH)
    async with aiofiles.open(title_post_path, mode='r') as f:
        title = await f.read()

    html_post_path = os.path.join(directory, HTML_PATH)
    async with aiofiles.open(html_post_path, mode='r') as f:
        contents = await f.read()

    return (title, contents)


async def make_a_post(data):
    logger.info("make_a_post")
    title = data['title']
    text = data['text']

    slug = await slugify(title)
    digest = await post_digest(title, text)
    url_part = "{0}-{1}".format(digest, slug)

    return await save_post(title, text, digest, url_part)


async def get_post_directory(digest, slug):
    url_part = "{0}-{1}".format(digest, slug)
    directory = os.path.join(POSTS_PATH, url_part)
    if not os.path.exists(directory):
        raise RuntimeError("No such post")
    return directory


async def is_valid_token(digest, slug, token):
    logger.info("is_valid_token %s %s %s", digest, slug, token)
    try:
        directory = await get_post_directory(digest, slug)
    except RuntimeError:
        return False

    token_path = os.path.join(directory, TOKEN_PATH)
    logger.info("token_path %s" % token_path)
    async with aiofiles.open(token_path, mode='r') as f:
        expected_token = await f.read()

    result = token.strip() == expected_token.strip()
    logger.info("result %s" % result)
    return result


async def delete_post(digest, slug):
    directory = await get_post_directory(digest, slug)
    title, contents = await get_post(digest, slug)
    shutil.rmtree(directory)
    return (title, contents)


async def convert_markdown(text, html_post_path):
    html = markdown2.markdown(text, extras=EXTRAS)
    async with aiofiles.open(html_post_path, mode='w') as f:
        await f.write(html)


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
    return s[:60]
