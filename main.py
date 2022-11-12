import discord

discordBotToken = "" # Insert discord token

backupGuildID = -1 # Insert backup guild ID
roleToGiveID = -1 # Insert role to add to the user
welcomeChannelID = -1 # Insert channel ID to send message in
mainGuildID = -1 # Insert guild ID for the main server
backupLink = "https://discord.gg/BackUpCode" # Insert backup link

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Verify",style=discord.ButtonStyle.green)
    async def verify_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        otherGuild = client.get_guild(backupGuildID)
        if otherGuild:
            inServer = False
            async for user in otherGuild.fetch_members(limit=150):
                if user.id == button.user.id:
                    role = button.guild.get_role(roleToGiveID)
                    await button.user.add_roles(role)
                    inServer = True
                    await button.response.send_message(content=f"Verification complete!", ephemeral = True)
            if not inServer:
                await button.response.send_message(content=backupLink, ephemeral = True)
        else:
            await button.response.send_message(content="An error occured, contact an admin.", ephemeral=True)
    @discord.ui.button(label="Join Server",style=discord.ButtonStyle.blurple)
    async def join_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await button.response.send_message(content=backupLink, ephemeral = True)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
    welcomeChannel = client.get_guild(mainGuildID).get_channel(welcomeChannelID)
    
    newEmbed = discord.Embed()
    newEmbed.title = "Backup Server Verification"
    newEmbed.color = 2480896
    newEmbed.description = "If you are already in the backup server, click the button below to verify. Otherwise, you can join the server by pressing the Join Server button or the link above."
    newEmbed.set_footer(text = "You MUST join the server to be verified.")
    
    await welcomeChannel.send(embed=newEmbed, view = Buttons())
    



client.run(discordBotToken)