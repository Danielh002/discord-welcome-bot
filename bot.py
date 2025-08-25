import os
import json
import time
import discord
from discord.ext import commands
from discord import Intents, VoiceChannel, FFmpegPCMAudio
from pathlib import Path
from gtts import gTTS
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DELAY_AFTER_CONNECT = int(os.getenv("DELAY_IN_MILLISECOND_AFTER_USER_CONNECTED", 2500)) / 1000
AUDIO_COOLDOWN = int(os.getenv("AUDIO_COOLDOWN", 600000)) / 1000
USERS_JSON = "users.json"

recent_audio_users = {}
intents = Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def load_users():
    if os.path.exists(USERS_JSON):
        with open(USERS_JSON, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_JSON, "w") as f:
        json.dump(users, f, indent=2)

def count_human_members(channel: VoiceChannel):
    return sum(1 for member in channel.members if not member.bot)

def ensure_directory_exists(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def generate_tts(text, file_path):
    ensure_directory_exists(file_path)
    tts = gTTS(text, lang="es")
    tts.save(file_path)
    print(f"Audio TTS Generated: {file_path}")

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    for guild in bot.guilds:
        print(f"Server: {guild.name}")
        for channel in guild.channels:
            if isinstance(channel, VoiceChannel):
                print(f"- Canal: {channel.name} (ID: {channel.id})")

@bot.event
async def on_message(message):
    print(f"Message received: {message.content} from {message.author} in {message.channel}")
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)
    if not before.channel and after.channel:
        channel = after.channel
        if count_human_members(channel) <= 1:
            print(f"Not enough human members in {channel.name}")
            return

        now = time.time()
        if user_id in recent_audio_users and now - recent_audio_users[user_id] < AUDIO_COOLDOWN:
            print(f"Audio in cooldown for {member.display_name}")
            return

        recent_audio_users[user_id] = now
        users = load_users()
        user_config = users.get(user_id)

        if not user_config:
            print(f"No configuration found for user {member.display_name} (ID: {user_id})")
            return

        audio_path = f"./audios/{user_id}.opus"
        if user_config["type"] == "text":
            if not os.path.exists(audio_path):
                print(f"Generating TTS for {member.display_name}: {user_config['value']}")
                generate_tts(user_config["value"], audio_path)
        elif user_config["type"] == "audio":
            audio_path = user_config["value"]
            if not os.path.exists(audio_path):
                print(f"File not found: {audio_path}")
                return

        print(f"Playing audio for {member.display_name}: {audio_path}")
        await play_audio(channel, audio_path)

async def play_audio(channel, audio_path):
    try:
        vc = await channel.connect()
        await asyncio.sleep(DELAY_AFTER_CONNECT)
        if vc.is_connected():
            vc.play(FFmpegPCMAudio(audio_path, options="-b:a 64k"), after=lambda e: bot.loop.create_task(vc.disconnect()))
    except discord.errors.ClientException:
        print(f"The bot could not connect to {channel.name}")
    except Exception as e:
        print(f"ERROR: Could not reproduce: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_audio(ctx, user: discord.Member, type_: str, *, value: str):
    if type_ not in ["text", "audio"]:
        await ctx.send("The type should be 'text' or 'audio'.")
        return

    users = load_users()
    if type_ == "text":
        audio_path = f"./audios/{user.id}.opus"
        if not os.path.exists(audio_path):
            print(f"Generating TTS for {user.display_name}: {value}")
            generate_tts(value, audio_path)
        users[str(user.id)] = {"type": type_, "value": value}
    elif type_ == "audio":
        audio_path = f"./audios/{value}"
        if not os.path.exists(audio_path):
            await ctx.send(f"Audio file not found: {audio_path}")
            return
        users[str(user.id)] = {"type": type_, "value": audio_path}

    save_users(users)
    await ctx.send(f"Configuration applied to {user.display_name}: {type_} = {value}")

@bot.command()
@commands.has_permissions(administrator=True)
async def list_audio(ctx):
    """List all users and their configured audios/texts"""
    users = load_users()
    if not users:
        await ctx.send("⚠️ No users have audio configured yet.")
        return

    lines = []
    for user_id, config in users.items():
        user = ctx.guild.get_member(int(user_id))
        username = user.display_name if user else f"Unknown ({user_id})"
        if config["type"] == "text":
            lines.append(f"👤 {username} → TTS: \"{config['value']}\"")
        elif config["type"] == "audio":
            lines.append(f"👤 {username} → Audio file: {config['value']}")

    message = "\n".join(lines)
    if len(message) > 1900:
        chunks = [message[i:i+1900] for i in range(0, len(message), 1900)]
        for chunk in chunks:
            await ctx.send(f"```{chunk}```")
    else:
        await ctx.send(f"```{message}```")

@bot.command()
@commands.has_permissions(administrator=True)
async def delete_audio(ctx, user: discord.Member):
    users = load_users()
    user_id = str(user.id)

    if user_id not in users:
        await ctx.send(f"No audio configuration found for {user.display_name}.")
        return

    del users[user_id]
    save_users(users)
    await ctx.send(f"Deleted audio configuration for {user.display_name}.")

bot.run(TOKEN)