import asyncio
import logging
import re
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
from post import get_yesterday_posts

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

dp = Dispatcher()


def create_media(post: dict):
    name = f'<strong><em>{post["name"]}</em></strong>'

    # получение описания без html тегов
    description = re.sub(r'\<[^>]*\>', '', post['description'])

    # получение списка категорий и вещей в этих категориях
    categories_and_clothes = []
    for category in post['clothes_category']:

        # получение и оборачивание ссылок на товары
        clothes = list(map(lambda cloth: f'<a href="{cloth["links"][0]["link"]}">   -{cloth["name"]}</a>', category['clothes']))
        clothes = '\n'.join(clothes)
        categories_and_clothes.append(f'<b><i>{category["name"]}:</i></b>\n{clothes}')

    # преобразование списка категорий с вещами в строку (текст)
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


async def send_posts(bot, channel_id):
    yesterday_posts = get_yesterday_posts()
    for post in yesterday_posts:
        await bot.send_media_group(channel_id, media=create_media(post))


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    print("bot is started...")
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.add_job(send_posts, trigger='cron', hour=20, minute=35, kwargs={'bot': bot, 'channel_id': CHANNEL_ID})
    # scheduler.start()
    # await bot.delete_webhook()
    # await dp.start_polling(bot)

    await send_posts(bot=bot, channel_id=CHANNEL_ID)
    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
