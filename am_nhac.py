import discord
from discord.ext import commands
import yt_dlp
import asyncio
import sys
print("Bot đang dùng Python tại:", sys.executable)


# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Cấu hình yt-dlp để lấy link stream trực tiếp
ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True, # Thêm dòng này để tắt cảnh báo
    'nocheckcertificate': True, # Thêm dòng này để bỏ qua kiểm tra chứng chỉ
}
ytdl = yt_dlp.YoutubeDL(ytdl_opts)

@bot.event
async def on_ready():
    print(f'Bot đã sẵn sàng với tên: {bot.user}')

@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("Bố phải vào kênh voice trước đã!")
        return
    
    channel = ctx.author.voice.channel
    
    # Kết nối vào voice channel
    if ctx.voice_client is None:
        await channel.connect()
    
    async with ctx.typing():
        try:
            # Lấy thông tin từ YouTube
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            audio_url = data['url']
            
            # Cấu hình FFmpeg (Bố nhớ cài FFmpeg vào máy trước nhé)
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            source = discord.FFmpegPCMAudio(
                audio_url, executable="ffmpeg",
                **ffmpeg_options)

            
            # Phát nhạc
            ctx.voice_client.play(source)
            await ctx.send(f"Đang quẩy nhạc cho bố: **{data['title']}**")
        except Exception as e:
            await ctx.send(f"Con gặp lỗi rồi bố ơi: {str(e)}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Đã dừng nhạc theo ý bố.")

import os
TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
