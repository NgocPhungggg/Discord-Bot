import discord

# Khai báo TOKEN của bot
TOKEN = ''  # Đảm bảo sử dụng token mới từ Discord Developer Portal

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.voice_states = True  # Bật thêm voice intents để kiểm tra kênh thoại

client = discord.Client(intents=intents)

# Sự kiện khi bot kết nối thành công
@client.event
async def on_ready():
    print(f'{client.user} đã sẵn sàng hoạt động!')

# Sự kiện khi có tin nhắn mới
@client.event
async def on_message(message):
    # Chỉ xử lý tin nhắn từ kênh "chat-nội-bang" hoặc "chat-bot"
    if message.channel.name in ['chat-nội-bang', 'chat-bot']:
        print(f"Đã nhận tin nhắn từ {message.channel.name} bởi {message.author}: {message.content}")
        # Kiểm tra nếu tin nhắn có chứa emoji hoặc sticker cần kiểm tra
        if ":emoji_61:" in message.content:
            guild = message.guild
            # Giả định rằng kênh "Nhà tù" luôn tồn tại, lấy kênh này mà không cần kiểm tra
            prison_channel = discord.utils.get(guild.voice_channels, name="Nhà tù")

            # Kiểm tra xem bot có tìm thấy kênh "Nhà tù" hay không
            if prison_channel is None:
                await message.channel.send("Không tìm thấy kênh 'Nhà tù'.")
                return

            # Kiểm tra nếu người dùng đang trong một kênh thoại khác
            if message.author.voice:
                try:
                    await message.author.move_to(prison_channel)
                    await message.channel.send(f"Người dùng {message.author.name} đã bị chuyển xuống kênh 'Nhà tù'.")
                except discord.Forbidden:
                    await message.channel.send("Bot không có quyền di chuyển người dùng.")
            else:
                await message.channel.send(f"{message.author.name} không ở trong kênh thoại nào.")

# Chạy bot với token thực tế
client.run(TOKEN)
