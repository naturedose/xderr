import discord
from discord.ext import commands

TOKEN = "MTM1NjY1NDA3NTExNDAzMzMwMg.GLTq4f.V8Ygc14bVynS2cmO3b2Z1JLiuw-ydQC_rUW1ck"

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
