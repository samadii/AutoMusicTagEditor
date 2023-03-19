import os
import io
import re
from PIL import Image
from music_tag import load_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
CAPTION = os.environ.get("DYNAMIC_CAPTION")
if 'CUSTOM_TAG' in os.environ:
    custom_tag = " [" + os.environ.get("CUSTOM_TAG") + "]"
else:
    custom_tag = " "

Bot = Client(
    "Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)


START_TXT = """
Hi {}, I am Auto Music Tagger Bot.
I will remove all usernames in the music tags automatically, and append your own username to music if you defined it already.

Send a music to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/samadii/AutoMusicTagEditor'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

   
@Bot.on_message(filters.private & filters.audio)
async def tag(bot, m):
    fname = m.audio.file_name
    await m.download("temp/file.mp3")
    music = load_file("temp/file.mp3")
    t = f"{music['title']}"
    a = f"{music['artist']}"
    al = f"{music['album']}"
    g = f"{music['genre']}"
    c = f"{music['comment']}"
    l = f"{music['lyrics']}"
    try:
        artwork = music['artwork']
        image_data = artwork.value.data
        img = Image.open(io.BytesIO(image_data))
        img.save("artwork.jpg")
    except ValueError:
        artwork = None
  
    fname = get_cleaned_tags(fname)
    title = get_cleaned_tags(f"{music['title']}")
    artist = get_cleaned_tags(f"{music['artist']}")
    album = get_cleaned_tags(f"{music['album']}")
    genre = get_cleaned_tags(f"{music['genre']}")
    comment = get_cleaned_tags(f"{music['comment']}")
    lyrics = get_cleaned_tags(f"{music['lyrics']}")
    
    # remove old tags
    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('lyrics')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    
    # apply new tags
    music['artist'] = artist + custom_tag
    music['title'] = title + custom_tag
    music['album'] = album + custom_tag
    music['genre'] = genre + custom_tag
    music['comment'] = comment + custom_tag
    music['lyrics'] = lyrics + custom_tag
    music.save()

    if CAPTION == "TRUE":
        caption = "✏️ Title: " + t + "\n" + "👤 Artist: " + a + "\n" + "💽 Album: " + al + "\n" + "🎼 Genre: " + g
    else:
        caption = m.caption if m.caption else " "

    try:
        if artwork is not None:
            await bot.send_audio(
                chat_id=m.chat.id,
                file_name=fname,
                performer=a,
                title=t,
                duration=m.audio.duration,
                caption=caption,
                thumb=open('artwork.jpg', 'rb'),
                audio='temp/file.mp3'
            )
        elif artwork is None:
            await bot.send_audio(
                chat_id=m.chat.id,
                file_name=fname,
                performer=a,
                title=t,
                duration=m.audio.duration,
                caption=caption,
                audio='temp/file.mp3'
            )
    except Exception as e:
        print(e)


Bot.run()
