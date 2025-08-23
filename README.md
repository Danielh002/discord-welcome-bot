# Discord Audio Greeting Bot

This is a Discord bot that plays a custom audio or text-to-speech (TTS) greeting
when a user joins a voice channel.

## Features

- Assign a **custom audio file** or **TTS message** to each user.
- Plays the greeting only when another human is present in the channel.
- Cooldown system to avoid spam.
- Admin commands:
  - `!set_audio @user text <message>` → assign a TTS message.
  - `!set_audio @user audio <filename>` → assign a pre-recorded audio file.
  - `!delete_audio @user` → remove a user’s greeting.
- Configurations stored in `users.json`.

---

## Requirements

- Python 3.9+
- FFmpeg (required for audio playback)
- A Discord bot token

---

## Installation

1. Clone the repository:

    ```bash
   git clone https://github.com/your-username/discord-audio-greeting-bot.git
   cd discord-audio-greeting-bot
   ```

2. Create a virtual environment and install dependencies:

    ```
    ./start.sh setup
    ```
3. Create a .env file with your bot token and configs:

    ```
    DISCORD_TOKEN=your_discord_token_here
    DELAY_IN_MILLISECOND_AFTER_USER_CONNECTED=2500
    AUDIO_COOLDOWN=600000
    ```

## Usage

* Start the bot:

    ```
    ./start.sh run
    ```

* Add audio/tts greetings:

    ```
    !set_audio @user text Bienvenido a la llamada!
    !set_audio @user audio sample.opus
    ```

* Delete audio/tts greeting:

    ```
    !delete_audio @user
    ```

## File Structure
```
.
├── audios/          # Folder for audio files
├── users.json       # User configuration file
├── bot.py           # Main bot script
├── start.sh         # Helper script
├── requirements.txt # Dependencies
└── .env             # Environment variables
```