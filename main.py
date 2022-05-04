from pyrogram import filters, idle, Client
import os
from urllib.parse import unquote
from datetime import datetime
import pytz

from info import (
    main_channel,
    bot_url,
    bot_owner,
    database_channel,
    admin_ids,
)
from plugins import (
    create_client,
    search_sub,
    download,
    is_new_title,
    save_file,
    get_last_title
)

local_time = datetime.now(pytz.timezone('Asia/Colombo'))
bot = Client('bot',
             api_id=7769505,
             api_hash='33f551652408cce07cf7e7621560021a',
             bot_token='2019524542:AAGUqBMCtPnf_ZHR2_oxXyDKpMX64-DkivQ'
             )
bot.start()


@bot.on_message(filters.private & filters.command(['start']))
def welcome(_, message):  # Done
    last = get_last_title()
    is_true = False
    if message.chat.id not in admin_ids:
        text = "Sorry {}, you are not an admin.🚫".format(message.chat.first_name)
        bot.send_message(message.chat.id, text)
    else:
        def send(text, message):
            bot.send_message(message.chat.id, text)

        if message.chat.id in admin_ids:
            print("Working")
            bot.send_message(message.chat.id, "<b>Subtitle Downloading start</b>")
            websites = ['baiscopelk', 'upasirasi', 'cineru', 'pirate']
            type = ['film', 'tv']

            for i in websites:
                for x in type:
                    n = 0
                    while True:  # website type
                        n = n + 1
                        print('\n', n, "page number")
                        subtitle = search_sub(n, i, type=x)
                        if last in subtitle['title']:
                            is_true = True
                            print(f'page {n} start')
                            bot.send_message(message.chat.id, f'page {n} start')
                        elif not subtitle['title']:
                            break
                        else:
                            print(f'page {n} skip')
                            bot.send_message(message.chat.id, f'page {n} skiped')
                        if is_true and subtitle is not None:  # cond < 100
                            for num in range(len(subtitle['title'])):
                                try:
                                    if is_new_title(subtitle['title'][num]):
                                        downloaded_file = download(subtitle['link'][num], subtitle['title'][num])
                                        for f in downloaded_file:
                                            file = f.replace('\\', '/')
                                            save_file(file[file.rindex("/") + 1:])
                                            siteName = i.replace(i[0], i[0].upper())
                                            caption = f'<b>File Name : </b> \n{file[file.rindex("/") + 1:]}\n\n<b' \
                                                      f'>Source link : </b><a href="{subtitle["link"][num]}">from {siteName}' \
                                                      f'</a>\n\n<b>Type : </b>{x} \n\n<b>Uploaded by <a href="' \
                                                      f'{bot_owner}">{bot_owner[bot_owner.rindex("/") + 1:]}</a></b> '
                                            for chat_id in database_channel:
                                                bot.send_document(chat_id, f, caption=caption)
                                            try:
                                                os.remove(downloaded_file['name'])
                                                print(downloaded_file)
                                                print("File deleted\n\n")
                                            except:
                                                pass
                                        else:
                                            import shutil
                                            shutil.rmtree('Extract')
                                            pass
                                    else:
                                        send(f"Skipped : {subtitle['title'][num]}", message)
                                except Exception as e:
                                    print(e)
                                    print('404 error not found')
                                    pass
                        elif not is_true:
                            pass
                        else:
                            break
            else:
                bot.send_message(message.chat.id, 'Compleated')
                print('completed')
        else:
            print(message.chat.id)


print("starting user")
idle()
bot.stop()
