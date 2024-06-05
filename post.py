import os
import re

import requests
import datetime

from aiogram.types import InputMediaPhoto

BACKEND_URL = os.getenv("BACKEND_URL")


def get_yesterday_posts():
    url = "https://aidarv.pythonanywhere.com/looks"
    response = requests.get(url)
    posts = response.json()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_posts = list(filter(lambda x: x['created_at'] == yesterday, posts))
    return yesterday_posts


def create_media(post: dict):
    name = f'<strong><em>{post["name"]}</em></strong>'

    # получение описания без html тегов
    description = re.sub(r'\<[^>]*\>', '', post['description'])

    categories_and_clothes = []

    for category in post['clothes_category']:

        # получение и оборачивание ссылок на товары
        clothes = list(map(lambda cloth: f'<a href="{cloth["links"][0]["link"]}">   -{cloth["name"]}</a>', category['clothes']))
        clothes = '\n'.join(clothes)
        categories_and_clothes.append(f'<b><i>{category["name"]}:</i></b>\n{clothes}')

    clothes = '\n\n'.join(categories_and_clothes)
    # сборка полного текста поста
    text = f'{name}\n\n{clothes}\n\n{description}'

    # получение изображений поста
    images = post['images']

    # создание медиагруппы
    inputMediaPhoto_array = list(map(lambda item: InputMediaPhoto(media=item['image']), images))

    # установка форматирования
    inputMediaPhoto_array[0].parse_mode = 'HTML'
    # добавление текста к первому элементу медиа
    inputMediaPhoto_array[0].caption = text

    return inputMediaPhoto_array

