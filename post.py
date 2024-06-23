import os
import re

import requests
import datetime

from aiogram.types import InputMediaPhoto

BACKEND_URL = os.getenv("BACKEND_URL")


def get_yesterday_posts():
    url = "https://aidarv.pythonanywhere.com/looks"
    response = requests.get(url)
    posts = response.json()['results']
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_posts = list(filter(lambda x: x['created_at'] == yesterday, posts))
    return yesterday_posts


print(get_yesterday_posts())
