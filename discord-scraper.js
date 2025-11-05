const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');

// Configuration - UPDATE THESE VALUES
const CONFIG = {
  BOT_TOKEN: process.env.DISCORD_BOT_TOKEN || 'YOUR_BOT_TOKEN_HERE',
  SERVER_ID: process.env.DISCORD_SERVER_ID || 'YOUR_SERVER_ID_HERE',
  OUTPUT_FILE: 'discord_members.json'
};

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildPresences // Optional: for online status
  ]
});

client.once('ready', async () => {
  console.log(`[SUCCESS] Bot logged in as ${client.user.tag}`);

  try {
    const guild = client.guilds.cache.get(CONFIG.SERVER_ID);

    if (!guild) {
      console.error(`[ERROR] Server not found. Bot is in ${client.guilds.cache.size} servers:`);
      client.guilds.cache.forEach(g => console.log(`  - ${g.name} (ID: ${g.id})`));
      client.destroy();
      process.exit(1);
    }

    console.log(`[INFO] Fetching members from: ${guild.name}`);
    console.log(`       Member count: ~${guild.memberCount}`);

    // Fetch all members (handles rate limiting automatically)
    const members = await guild.members.fetch({ limit: 1000 });

    const memberList = members.map(member => ({
      username: member.user.username,
      display_name: member.displayName,
      id: member.user.id,
      discriminator: member.user.discriminator,
      bot: member.user.bot,
      joined_at: member.joinedAt?.toISOString(),
      roles: member.roles.cache.map(role => role.name).filter(name => name !== '@everyone'),
      nickname: member.nickname,
      avatar_url: member.user.displayAvatarURL()
    }));

    // Save to JSON
    fs.writeFileSync(CONFIG.OUTPUT_FILE, JSON.stringify(memberList, null, 2));
    console.log(`[SUCCESS] Saved ${memberList.length} members to ${CONFIG.OUTPUT_FILE}`);

    // Also save as CSV for easier analysis
    const csvData = memberList.map(m =>
      `"${m.username}","${m.display_name}","${m.id}","${m.bot}","${m.joined_at}","${m.roles.join(';')}"`
    ).join('\n');

    fs.writeFileSync('discord_members.csv',
      'username,display_name,id,bot,joined_at,roles\n' + csvData
    );
    console.log(`[SUCCESS] Saved CSV to discord_members.csv`);

  } catch (error) {
    console.error('[ERROR] Error:', error.message);
  } finally {
    client.destroy();
    process.exit();
  }
});

client.on('error', error => {
  console.error('[ERROR] Client error:', error);
});

// Login
console.log('[INFO] Logging in to Discord...');
client.login(CONFIG.BOT_TOKEN).catch(err => {
  console.error('[ERROR] Login failed:', err.message);
  console.log('\nSetup Instructions:');
  console.log('1. Go to https://discord.com/developers/applications');
  console.log('2. Create a New Application');
  console.log('3. Go to Bot section -> Add Bot');
  console.log('4. Enable "Server Members Intent" under Privileged Gateway Intents');
  console.log('5. Copy the bot token and set DISCORD_BOT_TOKEN environment variable');
  console.log('6. Invite bot to your server using OAuth2 URL with "bot" scope and "Read Messages/View Channels" permission');
  process.exit(1);
});