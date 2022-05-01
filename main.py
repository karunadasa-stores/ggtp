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
    is_new_file
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
    if message.chat.id not in admin_ids:
        text = "Sorry {}, you are not an admin.🚫".format(message.chat.first_name)
        bot.send_message(message.chat.id, text)
    else:
        bot.delete_messages(message.chat.id, message.message_id)
        if message.chat.id in admin_ids:
            count = 0
            print("Working")
            msg_id = message.message_id + 1
            bot.send_message(message.chat.id, "<b>Subtitle Downloading start</b>")
            websites = ['baiscopelk', 'upasirasi', 'cineru', 'pirate']
            type = ['film', 'tv']

            for i in websites:
                for x in type:
                    n = 0
                    cond = 0
                    while True:  # website type
                        n = n + 1
                        print('\n', n, "page number")
                        subtitle = search_sub(n, i, type=x)
                        if cond < 100 and subtitle['title'] and subtitle is not None:
                            for num in range(len(subtitle['title'])):
                                try:
                                    downloaded_file = download(subtitle['link'][num], subtitle['title'][num])
                                    for f in downloaded_file:
                                        file = f.replace('\\', '/')
                                        if is_new_file(file[file.rindex('/')+1:]):
                                            siteName = i.replace(i[0], i[0].upper())
                                            caption = f'<b>File Name : </b> \n{file[file.rindex("/") + 1:]}\n\n<b' \
                                                      f'>Source link : </b><a href="{subtitle["link"][num]}">from {siteName}' \
                                                      f'</a>\n\n<b>Type : </b>{x} \n\n<b>Uploaded by <a href="' \
                                                      f'{bot_owner}">{bot_owner[bot_owner.rindex("/") + 1:]}</a></b> '
                                            for chat_id in database_channel:
                                                bot.send_document(chat_id, f, caption=caption)
                                        else:
                                            cond += 1
                                        try:
                                            os.remove(downloaded_file['name'])
                                            print(downloaded_file)
                                            bot.edit_message_text(message.chat.id, msg_id,
                                                                  "Download Count : {}\n{}".format(count, f))
                                            count = count + 1
                                            print("File deleted\n\n")
                                        except:
                                            pass
                                    else:
                                        import shutil
                                        shutil.rmtree('Extract')
                                        pass
                                except Exception as e:
                                    print(e)
                                    print('404 error not found')
                                    pass
                        else:
                            break
            else:
                bot.edit_message_text(message.chat.id, msg_id,
                                      "<b>Download Completed</b> \n{} Subtitles Downloaded".format(count))
                print('completed')
        else:
            print(message.chat.id)


print("starting user")
idle()
bot.stop()
