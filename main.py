import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands, tasks

load_dotenv()

intents = nextcord.Intents.all()
members = []
bot = commands.Bot(intents=intents)


@bot.listen()
async def on_ready():
    global members
    members = list(bot.get_all_members())


@tasks.loop(seconds=5)
async def called_once_a_day():
    message_channel = bot.get_channel(537263126526164992)
    print(f"Got channel {message_channel}")
    await message_channel.send("Your message")


@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


@bot.listen()
async def on_member_join(member):
    global members
    members.append(member)
    print(f"{member} joined")


@bot.listen()
async def on_member_leave(member):
    global members
    members.remove(member)
    print(f"{member} left")


@bot.slash_command(description="Replies with pong!")
async def ping(interaction: nextcord.Interaction):
    global members
    members = list(bot.get_all_members())
    await interaction.send("Pong!", ephemeral=True)

called_once_a_day.start()
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
