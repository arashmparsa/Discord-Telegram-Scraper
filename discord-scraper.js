const { Client, GatewayIntentBits } = require('discord.js');
const fs = require('fs');
const path = require('path');

class DiscordMemberScraper {
  constructor(token) {
    this.client = new Client({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildPresences
      ]
    });
    this.token = token;
    this.memberData = [];
  }

  async initialize() {
    return new Promise((resolve, reject) => {
      this.client.once('ready', resolve);
      this.client.once('error', reject);
      this.client.login(this.token);
    });
  }

  async scrapeGuild(guildId, options = {}) {
    const {
      includeBots = false,
      saveToFile = true,
      filename = `members_${guildId}_${Date.now()}.json`
    } = options;

    const guild = this.client.guilds.cache.get(guildId);
    
    if (!guild) {
      throw new Error(`Guild ${guildId} not found or bot not in server`);
    }

    console.log(`🔄 Fetching members from: ${guild.name}`);
    
    const members = await guild.members.fetch();
    const filteredMembers = includeBots ? members : members.filter(m => !m.user.bot);
    
    const memberData = filteredMembers.map(member => this.extractMemberData(member));
    
    if (saveToFile) {
      this.saveToFile(memberData, filename);
    }
    
    return {
      guild: guild.name,
      totalMembers: members.size,
      filteredMembers: filteredMembers.size,
      members: memberData
    };
  }

  extractMemberData(member) {
    return {
      id: member.user.id,
      username: member.user.username,
      globalName: member.user.globalName,
      discriminator: member.user.discriminator,
      avatar: member.user.avatarURL({ format: 'png', size: 256 }),
      displayName: member.displayName,
      bot: member.user.bot,
      joinedAt: member.joinedAt?.toISOString() || null,
      accountCreated: member.user.createdAt.toISOString(),
      roles: member.roles.cache.map(role => ({
        id: role.id,
        name: role.name,
        color: role.hexColor,
        position: role.position
      })),
      status: member.presence?.status || 'offline',
      activities: member.presence?.activities?.map(activity => activity.name) || [],
      premiumSince: member.premiumSince?.toISOString() || null,
      permissions: member.permissions.toArray()
    };
  }

  saveToFile(data, filename) {
    const filePath = path.join(process.cwd(), filename);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    console.log(`💾 Data saved to: ${filePath}`);
  }

  async destroy() {
    this.client.destroy();
  }
}

// Usage Example
async function main() {
  const scraper = new DiscordMemberScraper('YOUR_BOT_TOKEN_HERE');
  
  try {
    await scraper.initialize();
    console.log('✅ Bot ready!');
    
    // Scrape single server
    const result = await scraper.scrapeGuild('YOUR_SERVER_ID_HERE', {
      includeBots: false,
      filename: 'server_members.json'
    });
    
    console.log(`✅ Scraped ${result.filteredMembers} members from ${result.guild}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await scraper.destroy();
  }
}

// Run if this file is executed directly
if (require.main === module) {
  main();
}

module.exports = DiscordMemberScraper;