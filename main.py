import discord
from discord.ext import commands

TOKEN = "MTM2MjM5NDM3MDk5Mjc3MTM1NA.GINDEZ.-FrIdfMHXr3_stN4vwBwRpicEoXcGJYTb0HJ9A"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

bot.run(TOKEN)
