require('dotenv').config();

const gTTS = require('gtts');
const { Client, GatewayIntentBits } = require('discord.js');
const { joinVoiceChannel, createAudioPlayer, createAudioResource, VoiceConnectionStatus } = require('@discordjs/voice');
const { ensureDirectoryExists, checkIfDirExists, resolvePath, countHumanMembers } = require('./helpers');

// Configuración del bot
const TOKEN = process.env.DISCORD_TOKEN;
const DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED = process.env.DELAY_IN_MILI_SECOND_AFTER_USER_CONNECTED || 2500;
const AUDIO_COOLDOWN = process.env.AUDIO_COOLDOWN || 600000;

const recentAudioUsers = {};

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.GuildMembers
  ],
});

let monitoredUsers = {};
try {
  monitoredUsers = JSON.parse(process.env.MONITORED_USERS);
} catch (error) {
  console.error('Error al parsear MONITORED_USERS desde el archivo .env:', error);
}

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
  const userId = newState.member.id;

  // Si el usuario se conecta a un canal de voz
  if (newState.channel) {
    const channel = newState.channel;

    // Verificar que el canal tenga más de un miembro humano
    if (countHumanMembers(channel) > 1) {
      const now = Date.now();

      if (recentAudioUsers[userId] && now - recentAudioUsers[userId] < AUDIO_COOLDOWN) {
        console.log(`Audio no reproducido para ${newState.member.user.username}, está en cooldown.`);
        return;
      }

      recentAudioUsers[userId] = now;
    
      const message = monitoredUsers[userId];
      const audioPath = `./audios/audio_${userId}.mp3`;

      if (message) {
        // Generar el audio si no existe
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

        // Reproducir el audio después de un pequeño retraso
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
  }
});

client.login(TOKEN);
