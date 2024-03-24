from discord.ext import commands
from logFactory import logFactory 

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.errContact = ' Please contact justNorthofAverage'
        self.logger = logFactory('Commands')
        self.yeetErrors = True

    async def yeetError(self, message):
        self.logger.error(message)
        if self.bot.yeetErrors:
            try:
                await self.bot.reportingChannel.send(message)
            except Exception as Exc:
                self.logger.critical('An error occured reporting the last error ({message}) Error Reason {Exc}')

    #Exists to merely check if a bot is vibing on a server properly
    @commands.command()
    async def ISayHi(self, ctx):
        errLocCode = 'ISH'
        responseMessage = 'Hi!'
        try:
            await ctx.send(responseMessage)
        except Exception as Exc:
            await self.yeetError(f'An error occured reporting {responseMessage} to Guild "{ctx.guild.name}" '
                                 +f'in Channel {ctx.channel.name}(#{ctx.channel.id}) (Err - (Err - {errLocCode}.1)')
           

if __name__ == "__main__":
    print("hello")
