# Welcome Bot for Discord

A Discord bot that greets specific users when they join a voice channel with more than one human participant. The bot generates a personalized audio message and plays it in the voice channel.

---

## Features

- Greets monitored users with custom messages.
- Plays audio in the voice channel when specific conditions are met.
- Tracks only human participants in voice channels.
- Customizable user-message mappings via `.env`.

---

## Requirements

- **Node.js** (>= 16.9.0)
- **Discord Bot Token**
- A server where you can invite your bot.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Danielh002/welcome-bot.git
cd welcome-bot
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Create a .env File
Create a .env file in the root directory and configure the environment variables as shown below.

### Environment Variables
Create a .env file in the root directory and configure the environment variables as shown below.

Example .env File
```
DISCORD_TOKEN=your_discord_bot_token_here
DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED=2500
MONITORED_USERS={"XXXXXXX":"¡Hola Juan, bienvenido!","XXXXY":"¡lMAO!","YYYYYYYY":"Hello!","YYYYYYX":"Whats up?"}
```
- DISCORD_TOKEN: Your bot's token from the Discord Developer Portal.
- DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED: Time delay (in milliseconds) before the bot starts speaking after a user joins.
- MONITORED_USERS: A JSON object where keys are Discord user IDs, and values are the custom messages to be played for those users.

---

### Usage

## Run the Bot

```bash
npm run start
```

### Invite the Bot to Your Server
1. Go to the Discord Developer Portal and select your bot.
2. Under OAuth2 > URL Generator, check the following permissions:
    - Bot
    - Voice Channel Connect
3. Copy the generated URL and paste it into your browser to invite the bot to your server.

### Dependencies

## Required Libraries
- [discord.js](https://www.npmjs.com/package/@discordjs/voice) - For interacting with the Discord API.
- [@discordjs/voice](https://www.npmjs.com/package/@discordjs/voice) - For handling voice connections and playing audio.
- [dotenv](https://www.npmjs.com/package/dotenv) - For loading environment variables.
- [gtts](https://www.npmjs.com/package/gtts) - For generating audio from text.

## Install Dependencies
```bash
npm install discord.js @discordjs/voice dotenv gtts
```

## Folder Structure
```
welcome-bot/
├── helpers.js         # Utility functions (e.g., for file system checks)
├── bot.js           # Main bot logic
├── audios/            # Folder for storing generated audio files
├── .env               # Environment variables
└── package.json       # Project metadata and dependencies
```


## Notes
1. Audio Storage: Generated audio files are saved in the audios/ directory. Ensure this folder exists or is created dynamically (the bot does this automatically).
2. Monitoring Users: Update the MONITORED_USERS JSON in the .env file to add or remove users and customize their messages.

## Contributing
Feel free to open an issue or submit a pull request if you want to contribute!

## License
This project is licensed under the MIT License. See the LICENSE file for details.




