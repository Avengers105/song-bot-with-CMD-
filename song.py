import os
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

# logging
bot = Client(
   "Music-Bot",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)
## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@bot.on_message(filters.command("start") & ~filters.edited)
async def start(_, message):
   if message.chat.type == 'private':
       await message.reply("👋 𝗛𝗲𝗹𝗹𝗼 {}\n\n𝗜 𝗔𝗺 🎸𝐒𝐨𝐧𝐠 𝐏𝐥𝐚𝐲 𝐁𝐨𝐭[🎶](https://telegra.ph/file/c3c4ebdc70fa7a5510968.jpg)\n\n𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗡𝗮𝗺𝗲 𝗢𝗳 𝗧𝗵𝗲 𝗦𝗼𝗻𝗴 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁... 😍🥰🤗\n\n𝗧𝘆𝗽𝗲 /s 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲\n\n𝐄𝐠. /s Faded",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Developer', url='https://t.me/Peterparker6'),
                    InlineKeyboardButton('Deploy', url='https://t.me/SongPlayRoBot?startgroup=true')
                ]
            ]
        )
    )

@bot.on_message(filters.command("s") & ~filters.edited)
async def s(_, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 😕')
            return
    except Exception as e:
        m.edit(
            "✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐤 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲.\n\nEg./s Faded"
        )
        print(str(e))
        return
    m.edit("🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐀 𝐒𝐨𝐧𝐠 🎶 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 ⏳️ 𝐅𝐨𝐫 𝐅𝐞𝐰 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 [🚀](https://telegra.ph/file/534b7a64c646706df8bec.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 𝐓𝐢𝐭𝐥𝐞 : [{title[:35]}]({link})\n⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{duration}`\n👁‍🗨 𝐕𝐢𝐞𝐰𝐬 : `{views}`\n\n💌 𝐁𝐲 : @MusicDownloadv2bot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ 𝐄𝐫𝐫𝐨𝐫\n\n Report This Erorr To Fix @Peterparker6 🔥')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
