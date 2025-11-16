import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio

TOKEN = "Gan_token_o_day"  

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True  # Cho phép bot dùng voice

# gán lệnh gọi bot khi chat trong discord
bot = commands.Bot(command_prefix='!p', intents=intents)

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
                print(f"Lỗi kết nối vào voice channel: {e}")
        else:
            await ctx.send("Bot đã có mặt trong voice channel.")
    else:
        await ctx.send("Bạn cần phải ở trong voice channel để tôi vào.")

# Lệnh xử lý phát âm thanh khi có lệnh "!pt ..."
@bot.command(name='t')
async def google_tts(ctx, *, message: str):
    
    # Kiểm tra bot đã vào voice channel chưa
    if ctx.voice_client is None:
        await ctx.send("Bot cần phải vào voice channel trước. Hãy dùng lệnh !p-join.")
        return
    
    tts = gTTS(text=message, lang='vi') # Chọn giọng tiếng Việt
    file_name = "message_vi.mp3" # chuyển văn bản thành file mp3
    tts.save(file_name) #lưu file tạm

    voice_client = ctx.voice_client

    # có 2 cách để phát âm thanh
    # 1. tải ffmpeg.exe về và gán link (cách này tốn dung lượng nhưng độ trễ thấp)
    # 2. dùng thẳng ffmpeg của thư viện discord
    # --> dùng cách 2 Phát file âm thanh (dùng ffmpeg trong PATH, không cần chỉ đường dẫn)
    audio_source = discord.FFmpegPCMAudio(file_name)
    voice_client.play(audio_source)

    # Đợi phát xong
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Xóa file sau tạm sau khi phát
    if os.path.exists(file_name):
        os.remove(file_name)

# Khi bot khởi động
@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng!')
    print(f"Bot đang hoạt động với {len(bot.guilds)} server.")

# Khởi chạy bot
bot.run(TOKEN)
