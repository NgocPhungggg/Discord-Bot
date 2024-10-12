import discord
from discord.ext import tasks, commands
from datetime import datetime
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Khởi tạo bot với intents phù hợp
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!phung-', intents=intents)

# Biến toàn cục lưu tên phòng và giờ phút ngắt kết nối
disconnect_settings = {}

# Task chạy mỗi phút để kiểm tra thời gian và ngắt kết nối
@tasks.loop(minutes=1)
async def check_time_and_disconnect():
    now = datetime.now()
    
    for guild_id, settings in disconnect_settings.items():
        if now.hour == settings['hour'] and now.minute == settings['minute']:
            guild = bot.get_guild(guild_id)
            voice_channel = discord.utils.get(guild.voice_channels, name=settings['room'])
            
            if voice_channel:
                for member in voice_channel.members:
                    if not member.bot:  # Không ngắt kết nối bot
                        await member.move_to(None)
                        print(f'Đã ngắt kết nối {member.name} khỏi kênh {voice_channel.name}')
                # Sau khi ngắt kết nối, xóa cài đặt để không ngắt lần nữa
                del disconnect_settings[guild_id]
                print(f'Ngắt kết nối hoàn tất, xóa cài đặt cho {voice_channel.name}')

# Lệnh cho phép người dùng nhập giờ, phút và tên phòng
@bot.command(name='disconnect_at')
async def set_disconnect_time(ctx, hour: int, minute: int, *, room: str):
    guild_id = ctx.guild.id
    disconnect_settings[guild_id] = {
        'hour': hour,
        'minute': minute,
        'room': room
    }
    await ctx.send(f'Đã đặt lịch ngắt kết nối cho phòng **{room}** vào lúc **{hour:02d}:{minute:02d}**')

# Khi bot khởi động
@bot.event
async def on_ready():
    print(f'{bot.user} đã sẵn sàng!')
    check_time_and_disconnect.start()

# Chạy bot
bot.run(TOKEN)
