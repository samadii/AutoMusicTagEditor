from telegram import Update
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from music_tag import load_file


CAPTION = os.environ.get("DYNAMIC_CAPTION")
channel = os.environ.get("CHANNEL_ID")
if 'CUSTOM_TAG' in os.environ:
    custom_tag = os.environ.get("CUSTOM_TAG")
else:
    custom_tag = " "


def file_handler(update, context):
    fname = update.message['audio']['file_name']
    file_id = update.message['audio']['file_id']
    file = context.bot.get_file(file_id)
    file.download('file.mp3')
    music = load_file("file.mp3")
    t = f"{music['title']}"
    a = f"{music['artist']}"
    al = f"{music['album']}"
    g = f"{music['genre']}"

    if fname.__contains__("@") or fname.__contains__("["):
        first = fname.split(' ')[0]
        if "@" in first:
            filename = fname.split(f'{first}', -1)
        elif fname.__contains__("(@") and not "@" in first:
            filename = fname.split("(@")[-2]
        elif fname.__contains__("[@") and not "@" in first:
            filename = fname.split("[@")[-2]
        elif fname.__contains__("[") and not "@" in first:
            filename = fname.split("[")[-2]
        elif (not "@" in first) and (not fname.__contains__("(@") or fname.__contains__("[") or fname.__contains__("[@")):
            filename = fname.split("@")[-2]
    else:
        filename = fname

    if g.__contains__("@") or g.__contains__("["):
        first = g.split(' ')[0]
        if "@" in first:
            genre = g.split(f'{first}', -1)
        elif g.__contains__("(@") and not "@" in first:
            genre = g.split("(@")[-2]
        elif g.__contains__("[@") and not "@" in first:
            genre = g.split("[@")[-2]
        elif g.__contains__("[") and not "@" in first:
            genre = g.split("[")[-2]
        elif (not "@" in first) and (not g.__contains__("(@") or g.__contains__("[") or g.__contains__("[@")):
            genre = g.split("@")[-2]
    else:
        genre = g

    if t.__contains__("@") or t.__contains__("["):
        first = t.split(' ')[0]
        if "@" in first:
            title = t.split(f'{first}', -1)
        elif t.__contains__("(@") and not "@" in first:
            title = t.split("(@")[-2]
        elif t.__contains__("[@") and not "@" in first:
            title = t.split("[@")[-2]
        elif t.__contains__("[") and not "@" in first:
            title = t.split("[")[-2]
        elif (not "@" in first) and (not t.__contains__("(@") or t.__contains__("[") or t.__contains__("[@")):
            title = t.split("@")[-2]
    else:
        title = t

    if al.__contains__("@") or al.__contains__("["):
        first = al.split(' ')[0]
        if "@" in first:
            album = al.split(f'{first}', -1)
        elif al.__contains__("(@") and not "@" in first:
            album = al.split("(@")[-2]
        elif al.__contains__("[@") and not "@" in first:
            album = al.split("[@")[-2]
        elif al.__contains__("[") and not "@" in first:
            album = al.split("[")[-2]
        elif (not "@" in first) and (not al.__contains__("(@") or al.__contains__("[") or al.__contains__("[@")):
            album = al.split("@")[-2]
    else:
        album = al

   
    if a.__contains__("@") or a.__contains__("["):
        first = a.split(' ')[0]
        if "@" in first:
            artist = a.split(f'{first}', -1)
        elif a.__contains__("(@") and not "@" in first:
            artist = a.split("(@")[-2]
        elif a.__contains__("[@") and not "@" in first:
            artist = a.split("[@")[-2]
        elif a.__contains__("[") and not "@" in first:
            artist = a.split("[")[-2]
        elif (not "@" in first) and (not a.__contains__("(@") or a.__contains__("[") or a.__contains__("[@")):
            artist = a.split("@")[-2]
    else:
        artist = a

    music.remove_tag('artist')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    music['artist'] = artist + " [" + custom_tag + "]"
    music['title'] = title + " [" + custom_tag + "]"
    music['album'] = album + " [" + custom_tag + "]"
    music['genre'] = genre + " [" + custom_tag + "]"
    music.save()

    if CAPTION == "TRUE":
        caption = "✏️ Title: " + title + "\n" + "👤 Artist: " + artist + "\n" + "💽 Album: " + album + "\n" + "🎼 Genre: " + genre
    else:
        caption = update.message['caption']
    try:
        context.bot.sendAudio(
            chat_id = channel,
            filename = filename,
            caption = caption, 
            audio = open('file.mp3', 'rb')
        )
    except Exception as e:
        print(e)
        
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi, Add me to the specified channel and then send the musics here, i will post them.")


if __name__=='__main__':
    token = os.environ.get('BOT_TOKEN')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.audio, file_handler))
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
