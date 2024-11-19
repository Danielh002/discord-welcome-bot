require('dotenv').config();

const gTTS = require('gtts');
const { Client, GatewayIntentBits } = require('discord.js');
const { joinVoiceChannel, createAudioPlayer, createAudioResource, VoiceConnectionStatus } = require('@discordjs/voice');
const { ensureDirectoryExists, checkIfDirExists, resolvePath } = require('./helpers');

// Configuración del bot
const TOKEN = process.env.DISCORD_TOKEN;
const DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED = process.env.DISCORD_TOKEN || 2500

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.GuildMembers
  ],
});

const monitoredUsers = {
  '285803618169520130': '¡Hola Cano, bienvenido!',
  '132668197743624192': '¡Puto Chino!',
  '233419603185762304': 'Minecraft!',
  '230880858418970625': 'Gordo, Macdo Macdo?',
  '164940415957467136': 'Gordo, Macdo Macdo?'
};

// Evento cuando el bot se conecta
client.once('ready', () => {
  console.log(`Bot conectado como ${client.user.tag}`);
  console.log('Bot conectado. Aquí están los canales accesibles:');
  client.guilds.cache.forEach(guild => {
    console.log(`Servidor: ${guild.name}`);
    guild.channels.cache
      .filter(channel => channel.isVoiceBased()) // Solo canales de voz
      .forEach(channel => {
        console.log(`- Canal: ${channel.name} (ID: ${channel.id})`);
      });
  });
});

// Detectar cambios en el estado de voz
client.on('voiceStateUpdate', (oldState, newState) => {
  // Si el usuario se conecta a un canal de voz
  if (!oldState.channel && newState.channel) {
    const channel = newState.channel;
    const userId = newState.member.id;

    if (monitoredUsers[userId] && channel.members.size >= 1) {
      const message = monitoredUsers[userId];
      const audioPath = `./audios/audio_${userId}.mp3`;

      if (!checkIfDirExists(audioPath)) {
        ensureDirectoryExists(audioPath);
        const tts = new gTTS(message, 'es');
        tts.save(audioPath, (err) => {
          if (err) {
            console.error('Error al generar el audio:', err);
          } else {
            console.log(`Audio generado para ${newState.member.user.username}`);
          }
        });
      }

      setTimeout(() => {
        const connection = joinVoiceChannel({
          channelId: newState.channel.id,
          guildId: newState.guild.id,
          adapterCreator: newState.guild.voiceAdapterCreator,
        });

        connection.on(VoiceConnectionStatus.Ready, () => {
          const player = createAudioPlayer();
          const resource = createAudioResource(resolvePath(audioPath));

          player.play(resource);
          connection.subscribe(player);

          player.on('idle', () => {
            connection.destroy();
          });
        });
      }, DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED);
    }
  }
});

client.login(TOKEN);
