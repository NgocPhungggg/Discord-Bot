import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio

# Đặt token bot Discord của bạn ở đây
TOKEN = ''  # Thay thế bằng token của bạn

ffmpeg_path = r'W:\FFmpeg\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe'

# Khởi tạo bot với quyền cần thiết
intents = discord.Intents.default()
intents.messages = True  # Để nhận tin nhắn từ kênh chat
intents.message_content = True  # Đảm bảo quyền đọc nội dung tin nhắn được bật
intents.guilds = True
intents.voice_states = True  # Cho phép bot sử dụng voice

bot = commands.Bot(command_prefix='!p', intents=intents)

# Lệnh cho bot vào voice channel khi gõ "phung-join"
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

# Lệnh xử lý phát âm thanh khi có lệnh phung-google
@bot.command(name='t')
async def google(ctx, *, message: str):
    # Kiểm tra bot đã vào voice channel chưa
    if ctx.voice_client is None:
        await ctx.send("Bot cần phải vào voice channel trước. Hãy dùng lệnh phung-join.")
        return

    # Tạo file âm thanh từ tin nhắn
    tts = gTTS(text=message, lang='vi')
    tts.save("message.mp3")

    # Phát file âm thanh trong voice channel
    voice_client = ctx.voice_client
    #voice_client.play(discord.FFmpegPCMAudio('message.mp3'))
    voice_client.play(discord.FFmpegPCMAudio('message.mp3', executable=ffmpeg_path))


    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Xóa file âm thanh sau khi phát
    os.remove("message.mp3")

# Khi bot khởi động
@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng!')
    print(f"Bot đang hoạt động với {len(bot.guilds)} server.")

# Khởi chạy bot
bot.run(TOKEN)
