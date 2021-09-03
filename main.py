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

    if fname.split(' ')[0].__contains__("@") or fname.split(' ')[0].__contains__(".me/"):
        fname = fname.split(f"{fname.split(' ')[0]}")[+1]
    if (fname.__contains__("@") or fname.__contains__(".me/")) and ((not fname.split(' ')[0].__contains__("@")) and (not fname.split(' ')[0].__contains__(".me/"))):
        fname = fname.split(f"{fname.rsplit(' ', 1)[1]}")[0]

    if a.split(' ')[0].__contains__("@") or a.split(' ')[0].__contains__(".me/"):
        a = a.split(f"{a.split(' ')[0]}")[+1]
    if (a.__contains__("@") or a.__contains__(".me/")) and ((not a.split(' ')[0].__contains__("@")) and (not a.split(' ')[0].__contains__(".me/"))):
        a = a.split(f"{a.rsplit(' ', 1)[1]}")[0]
     
    if al.split(' ')[0].__contains__("@") or al.split(' ')[0].__contains__(".me/"):
        al = al.split(f"{al.split(' ')[0]}")[+1]
    if (al.__contains__("@") or al.__contains__(".me/")) and ((not al.split(' ')[0].__contains__("@")) and (not al.split(' ')[0].__contains__(".me/"))):
        al = al.split(f"{al.rsplit(' ', 1)[1]}")[0]

    if c.split(' ')[0].__contains__("@") or c.split(' ')[0].__contains__(".me/"):
        c = c.split(f"{c.split(' ')[0]}")[+1]
    if (c.__contains__("@") or c.__contains__(".me/")) and ((not c.split(' ')[0].__contains__("@")) and (not c.split(' ')[0].__contains__(".me/"))):
        c = c.split(f"{c.rsplit(' ', 1)[1]}")[0]

    if l.split(' ')[0].__contains__("@") or l.split(' ')[0].__contains__(".me/"):
        l = l.split(f"{l.split(' ')[0]}")[+1]
    if (l.__contains__("@") or l.__contains__(".me/")) and ((not l.split(' ')[0].__contains__("@")) and (not l.split(' ')[0].__contains__(".me/"))):
        l = l.split(f"{l.rsplit(' ', 1)[1]}")[0]

    if t.split(' ')[0].__contains__("@") or t.split(' ')[0].__contains__(".me/"):
        t = t.split(f"{t.split(' ')[0]}")[+1]
    if (t.__contains__("@") or t.__contains__(".me/")) and ((not t.split(' ')[0].__contains__("@")) and (not t.split(' ')[0].__contains__(".me/"))):
        t = t.split(f"{t.rsplit(' ', 1)[1]}")[0]

    if g.split(' ')[0].__contains__("@") or g.split(' ')[0].__contains__(".me/"):
        g = g.split(f"{g.split(' ')[0]}")[+1]
    if (g.__contains__("@") or g.__contains__(".me/")) and ((not g.split(' ')[0].__contains__("@")) and (not g.split(' ')[0].__contains__(".me/"))):
        g = g.split(f"{g.rsplit(' ', 1)[1]}")[0]

    music.remove_tag('lyrics')
    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    music['artist'] = a + custom_tag
    music['title'] = t + custom_tag
    music['album'] = al + custom_tag
    music['genre'] = g + custom_tag
    music['comment'] = c + custom_tag
    music['lyrics'] = l + custom_tag
    music.save()

    if CAPTION == "TRUE":
        caption = "✏️ Title: " + t + "\n" + "👤 Artist: " + a + "\n" + "💽 Album: " + al + "\n" + "🎼 Genre: " + g
    else:
        caption = update.message['caption']
    try:
        context.bot.sendAudio(
            chat_id = update.message.chat_id,
            filename = fname,
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
