import os
import discord
from logFactory import logFactory
from discord.ext import tasks, commands
from modules.commands import Commands

from dotenv import load_dotenv
load_dotenv()

class PolarisBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.message_content = True
        self.extraLifeLastRan = None
        self.logger = logFactory('Bot')
        self.reportingChannel = None
        self.yeetErrors = True

        super().__init__(command_prefix="!", intents=intents, *args, **kwargs)

    async def on_ready(self):
        self.logger.info(f"Getting Ready!")
        await self.add_cog(Commands(bot))
        self.logger.info(f"Cogs were loaded")
        self.logger.info(f"Importing reporting channel")
        self.reportingChannel = self.get_channel(int(os.environ['GENERAL_CHANNEL'])) 
        onReadyMessage = f"{self.user.name} (v{os.environ['VERSION']}) {os.environ['STATUS']}"

        if (int(os.environ['DEBUG']) == 1): 
            onReadyMessage = '[DEBUG MODE] '+onReadyMessage

        self.logger.info(onReadyMessage)
        await self.reportingChannel.send(onReadyMessage)       
     
    async def on_guild_join(self, guild):
        self.logger.info(f"Joining Guild: {guild.name} ({guild.id})")

    async def on_guild_remove(self, guild):
        self.logger.warning(f"Leaving Guild: {guild.name} ({guild.id})")

    async def setup_hook(self) -> None:
        self.logger.info('setup_hook Running')
        await self.tree.sync()
        self.loop1.start()
        self.loop2.start()
        self.logger.info('setup_hook complete')

    async def yeetError(self, message):
        self.logger.error(message)
        if self.yeetErrors:
            try:
                await self.reportingChannel.send(message)
            except Exception as Exc:
                self.logger.critical('An error occured reporting the last error ({message}) Error Reason {Exc}')
                
    @tasks.loop(seconds=10)  # task runs every 20 seconds
    async def loop1(self):
        self.logger.info("Loop1 Trigger")

    @tasks.loop(seconds=15)  # task runs every 20 seconds
    async def loop2(self):
        self.logger.info("Loop2 Trigger")

    @loop1.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    @loop2.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
    
    def run(self):
        if os.environ['BOT_TOKEN']:
            try:
                super().run(os.environ['BOT_TOKEN'])
            except:
                self.logger.fatal("[BOT_TOKEN] was not a valid token (Err - B.run.1)")
        else:
            self.logger.fatal("[BOT_TOKEN] did not contain a value (Err - B.run.2)")


if __name__ == "__main__":
    bot = PolarisBot()
    bot.run()
