import requests
from pyrogram import *
from pyrogram.types import *
import wget
import os
import glob
from config import botcax_api
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx
from config import botcax_api

__MODULES__ = "Couple"

def help_string(org):
    return h_s(org, "help_couple")

@zb.ubot("couple")
async def pinterest(client, message, *args):
    jalan = await message.reply(f"🪐 <b>ᴘʀᴏᴄᴇssɪɴɢ...</b>")
    chat_id = message.chat.id
    url = f"https://api.botcahx.eu.org/api/randomgambar/couplepp?apikey={botcax_api}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        male_url = data['result']['male']
        female_url = data['result']['female']

        # Download images using wget
        male_image_filename = wget.download(male_url, out="male.jpg")
        female_image_filename = wget.download(female_url, out="female.jpg")

        # Prepare media group
        media_group = [
            InputMediaPhoto(media=male_image_filename),
            InputMediaPhoto(media=female_image_filename)
        ]

        # Send media group
        janda = await client.send_media_group(chat_id, media_group)
        if janda:
            await jalan.delete()
        # Clean up downloaded files
        os.remove(male_image_filename)
        os.remove(female_image_filename)
    else:
        await message.reply(f"Request failed with status code {response.status_code}")
