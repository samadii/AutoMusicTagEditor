from telegram import Update
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from music_tag import load_file

CAPTION = os.environ.get("DYNAMIC_CAPTION")
if 'CUSTOM_TAG' in os.environ:
    custom_tag = " [" + os.environ.get("CUSTOM_TAG") + "]"
else:
    custom_tag = " "


def tag(update, context):
    fname = update.message['audio']['file_name']
    file_id = update.message['audio']['file_id']
    file = context.bot.get_file(file_id)
    file.download('file.mp3')
    music = load_file("file.mp3")
    t = f"{music['title']}"
    a = f"{music['artist']}"
    al = f"{music['album']}"
    g = f"{music['genre']}"
    c = f"{music['comment']}"
    l = f"{music['lyrics']}"

    if fname.__contains__("@") or fname.__contains__("["):
        first = fname.split(' ')[0]
        if "@" in first:
            filename = fname.split(f'{first}')[+1]
        elif fname.__contains__("(@") and not "@" in first:
            filename = fname.split("(@")[-2]
        elif fname.__contains__("[@") and not "@" in first:
            filename = fname.split("[@")[-2]
        elif fname.__contains__("{@") and not "@" in first:
            filename = fname.split("{@")[-2]
        elif fname.__contains__("[") and (not fname.__contains__("[@")) and (not "@" in first):
            filename = fname.split("[")[-2]
        elif (not "@" in first) and (not fname.__contains__("(@") or fname.__contains__("[") or fname.__contains__("{@") or fname.__contains__("[@")):
            filename = fname.split("@")[-2]
    else:
        filename = fname

    if g.__contains__("@") or g.__contains__("["):
        first = g.split(' ')[0]
        if "@" in first:
            genre = g.split(f'{first}')[+1]
        elif g.__contains__("(@") and not "@" in first:
            genre = g.split("(@")[-2]
        elif g.__contains__("{@") and not "@" in first:
            genre = g.split("{@")[-2]
        elif g.__contains__("[@") and not "@" in first:
            genre = g.split("[@")[-2]
        elif g.__contains__("[") and (not g.__contains__("[@")) and (not "@" in first):
            genre = g.split("[")[-2]
        elif (not "@" in first) and (not g.__contains__("(@") or g.__contains__("{@") or g.__contains__("[") or g.__contains__("[@")):
            genre = g.split("@")[-2]
    else:
        genre = g
    
    if l.__contains__("@") or l.__contains__("["):
        first = l.split(' ')[0]
        if "@" in first:
            lyrics = l.split(f'{first}')[+1]
        elif l.__contains__("(@") and not "@" in first:
            lyrics = l.split("(@")[-2]
        elif l.__contains__("{@") and not "@" in first:
            lyrics = l.split("{@")[-2]
        elif l.__contains__("[@") and not "@" in first:
            lyrics = l.split("[@")[-2]
        elif l.__contains__("[") and (not l.__contains__("[@")) and (not "@" in first):
            lyrics = l.split("[")[-2]
        elif (not "@" in first) and (not l.__contains__("(@") or l.__contains__("{@") or l.__contains__("[") or l.__contains__("[@")):
            lyrics = l.split("@")[-2]
    else:
        lyrics = l

    if c.__contains__("@") or c.__contains__("["):
        first = c.split(' ')[0]
        if "@" in first:
            comment = c.split(f'{first}')[+1]
        elif c.__contains__("(@") and not "@" in first:
            comment = c.split("(@")[-2]
        elif c.__contains__("{@") and not "@" in first:
            comment = c.split("{@")[-2]
        elif c.__contains__("[@") and not "@" in first:
            comment = c.split("[@")[-2]
        elif c.__contains__("[") and (not c.__contains__("[@")) and (not "@" in first):
            comment = c.split("[")[-2]
        elif (not "@" in first) and (not c.__contains__("(@") or c.__contains__("{@") or c.__contains__("[") or c.__contains__("[@")):
            comment = c.split("@")[-2]
    else:
        comment = c

    if t.__contains__("@") or t.__contains__("["):
        first = t.split(' ')[0]
        if "@" in first:
            title = t.split(f'{first}')[+1]
        elif t.__contains__("{@") and not "@" in first:
            title = t.split("{@")[-2]
        elif t.__contains__("(@") and not "@" in first:
            title = t.split("(@")[-2]
        elif t.__contains__("[@") and not "@" in first:
            title = t.split("[@")[-2]
        elif t.__contains__("[") and (not t.__contains__("[@")) and (not "@" in first):
            title = t.split("[")[-2]
        elif (not "@" in first) and (not t.__contains__("(@") or t.__contains__("{@") or t.__contains__("[") or t.__contains__("[@")):
            title = t.split("@")[-2]
    else:
        title = t

    if al.__contains__("@") or al.__contains__("["):
        first = al.split(' ')[0]
        if "@" in first:
            album = al.split(f'{first}')[+1]
        elif al.__contains__("(@") and not "@" in first:
            album = al.split("(@")[-2]
        elif al.__contains__("{@") and not "@" in first:
            album = al.split("{@")[-2]
        elif al.__contains__("[@") and not "@" in first:
            album = al.split("[@")[-2]
        elif al.__contains__("[") and (not al.__contains__("[@")) and (not "@" in first):
            album = al.split("[")[-2]
        elif (not "@" in first) and (not al.__contains__("(@") or al.__contains__("{@") or al.__contains__("[") or al.__contains__("[@")):
            album = al.split("@")[-2]
    else:
        album = al

    if a.__contains__("@") or a.__contains__("[") or a.__contains__("("):
        first = a.split(' ')[0]
        if "@" in first:
            artist = a.split(f'{first}')[+1]
        elif a.__contains__("(@") and not "@" in first:
            artist = a.split("(@")[-2]
        elif a.__contains__("[@") and not "@" in first:
            artist = a.split("[@")[-2]
        elif a.__contains__("{@") and not "@" in first:
            artist = a.split("{@")[-2]
        elif a.__contains__("[") and (not a.__contains__("[@")) and (not "@" in first):
            artist = a.split("[")[-2]
        elif a.__contains__("(") and (not a.__contains__("(@")) and (not "@" in first):
            artist = a.split("(")[-2]
        elif (not "@" in first) and (not a.__contains__("(@") or a.__contains__("{@") or a.__contains__("[") or a.__contains__("[@") or a.__contains__("(")):
            artist = a.split("@")[-2]
    else:
        artist = a

    music.remove_tag('lyrics')
    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    music['artist'] = artist + custom_tag
    music['title'] = title + custom_tag
    music['album'] = album + custom_tag
    music['genre'] = genre + custom_tag
    music['comment'] = comment + custom_tag
    music['lyrics'] = lyrics + custom_tag
    music.save()

    if CAPTION == "TRUE":
        caption = "✏️ Title: " + title + "\n" + "👤 Artist: " + artist + "\n" + "💽 Album: " + album + "\n" + "🎼 Genre: " + genre
    else:
        caption = update.message['caption']
    try:
        context.bot.sendAudio(
            chat_id = update.message.chat_id,
            filename = filename,
            caption = caption, 
            audio = open('file.mp3', 'rb')
        )
    except Exception as e:
        print(e)
        
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi, I am Music Tag Editor Bot.\n\nSend me some musics, I will remove almost all usernames in the music tags.")


if __name__=='__main__':
    token = os.environ.get('BOT_TOKEN')
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.audio, tag))
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
