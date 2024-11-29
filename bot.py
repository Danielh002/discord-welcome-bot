import os
import json
import time
import discord
from dotenv import load_dotenv
from gtts import gTTS
import asyncio
from discord.ext import commands
from discord import Intents, VoiceChannel
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DELAY_IN_MILI_SECONDS_AFTER_USER_CONNECTED = int(os.getenv("DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED", 2500)) / 1000
AUDIO_COOLDOWN_IN_SECONDS = int(os.getenv("AUDIO_COOLDOWN", 600000)) / 1000
MONITORED_USERS = json.loads(os.getenv("MONITORED_USERS", "{}"))

# Variables globales
recent_audio_users = {}
intents = Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

def count_human_members(channel: VoiceChannel):
    return sum(1 for member in channel.members if not member.bot)

def ensure_directory_exists(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    for guild in bot.guilds:
        print(f"Servidor: {guild.name}")
        for channel in guild.channels:
            if isinstance(channel, VoiceChannel):
                print(f"- Canal: {channel.name} (ID: {channel.id})")

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)

    if not before.channel and after.channel:
        channel = after.channel

        if count_human_members(channel) > 1:
            now = time.time()

            if user_id in recent_audio_users and now - recent_audio_users[user_id] < AUDIO_COOLDOWN_IN_SECONDS:
                print(f"Audio no reproducido para {member.display_name}, está en cooldown.")
                return

            recent_audio_users[user_id] = now
            message = MONITORED_USERS.get(user_id)

            if message:
                audio_path = f"./audios/audio_{user_id}.mp3"

                if not os.path.exists(audio_path):
                    ensure_directory_exists(audio_path)
                    tts = gTTS(message, lang="es")
                    tts.save(audio_path)
                    print(f"Audio generado para {member.display_name}")

                await play_audio(channel, audio_path)

async def play_audio(channel, audio_path):
    vc = await channel.connect()

    await asyncio.sleep(DELAY_IN_MILI_SECONDS_AFTER_USER_CONNECTED)

    if vc.is_connected():
        vc.play(discord.FFmpegPCMAudio(audio_path), after=lambda e: print(f"Audio reproducido: {audio_path}"))
        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

bot.run(TOKEN)
