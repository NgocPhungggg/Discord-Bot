import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio
from googletrans import Translator  # Dùng để dịch văn bản

# Đặt token bot Discord của bạn ở đây
TOKEN = ''  # Thay thế bằng token của bạn

# Khởi tạo bot với quyền cần thiết
intents = discord.Intents.default()
intents.messages = True  # Để nhận tin nhắn từ kênh chat
intents.message_content = True  # Đảm bảo quyền đọc nội dung tin nhắn được bật
intents.guilds = True
intents.voice_states = True  # Cho phép bot sử dụng voice

bot = commands.Bot(command_prefix='!p', intents=intents)

# Hàm dịch văn bản
def translate_text(text, source_lang='vi', target_lang='en'):
    translator = Translator()
    translated = translator.translate(text, src=source_lang, dest=target_lang)
    return translated.text

# Lệnh bot vào voice channel khi gõ "!p-join"
@bot.command(name='-join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            try:
                await channel.connect()
                await ctx.send(f"Bot đã vào voice channel: {channel.name}")
            except Exception as e:
                await ctx.send(f"Không thể kết nối vào voice channel: {e}")
                print(f"Lỗi kết nối vào voice channel: {e}")  # In lỗi vào console
        else:
            await ctx.send("Bot đã có mặt trong voice channel.")
    else:
        await ctx.send("Bạn cần phải ở trong voice channel để tôi vào.")

# Lệnh xử lý phát âm thanh khi có lệnh "!p-t"
@bot.command(name='t')
async def google(ctx, *, message: str):
    # Kiểm tra bot đã vào voice channel chưa
    if ctx.voice_client is None:
        await ctx.send("Bot cần phải vào voice channel trước. Hãy dùng lệnh !p-join.")
        return

    # Dịch văn bản tiếng Việt sang tiếng Anh
    translated_text = translate_text(message, source_lang='vi', target_lang='en')
    
    # Chuyển văn bản thành giọng nói tiếng Việt
    tts_vi = gTTS(text=message, lang='vi')
    tts_en = gTTS(text=translated_text, lang='en')

    # Tạo file âm thanh tạm thời
    tts_vi.save("message_vi.mp3")
    tts_en.save("message_en.mp3")

    # Lấy kênh voice của người dùng
    voice_client = ctx.voice_client
    
    # Phát giọng nói tiếng Việt
    voice_client.play(discord.FFmpegPCMAudio("message_vi.mp3"), after=lambda e: print('Done playing Vietnamese', e))
    while voice_client.is_playing():
        await asyncio.sleep(1)
    
    # Phát giọng nói tiếng Anh
    voice_client.play(discord.FFmpegPCMAudio("message_en.mp3"), after=lambda e: print('Done playing English', e))
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Xóa file âm thanh sau khi phát
    os.remove("message_vi.mp3")
    os.remove("message_en.mp3")

# Khi bot khởi động
@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng!')
    print(f"Bot đang hoạt động với {len(bot.guilds)} server.")

# Khởi chạy bot
bot.run(TOKEN)
