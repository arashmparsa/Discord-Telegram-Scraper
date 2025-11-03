const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers]
});

client.once('ready', async () => {
  console.log('Bot is ready');
  
  const guild = client.guilds.cache.get('YOUR_SERVER_ID_HERE');
  
  if (guild) {
    console.log(`Found server: ${guild.name}`);
    const members = await guild.members.fetch();
    
    const memberList = members.map(member => ({
      username: member.user.username,
      id: member.user.id,
      bot: member.user.bot,
      joinedAt: member.joinedAt
    }));
    
    fs.writeFileSync('members.json', JSON.stringify(memberList, null, 2));
    console.log(`Saved ${memberList.length} members to members.json`);
    
  } else {
    console.log('Server not found');
  }
  
  client.destroy();
  process.exit();
});

client.login('YOUR_BOT_TOKEN_HERE');