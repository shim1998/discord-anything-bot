import os
import random
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands, tasks

from preprocess import get_list
from cron import tweet

load_dotenv()

intents = nextcord.Intents.all()
members = []
bot = commands.Bot(intents=intents)


def generate_random_text():
    text = random.choice(get_list())
    ctr = text.count(-1)
    nums = random.sample(range(0, len(members)), ctr)
    members_needed = []
    x_ctr = 0
    for member in members:
        if x_ctr in nums:
            members_needed.append(member.name)
        x_ctr += 1
    x_ctr = 0
    # print(text, ctr, members_needed)
    for i in range(len(text)):
        if text[i] == -1:
            text[i] = members_needed[x_ctr]
            x_ctr += 1
    return " ".join(text)


@bot.listen()
async def on_ready():
    global members
    members = list(bot.get_all_members())


@tasks.loop(hours=6)
async def call_every_6_hours():
    message_channel = bot.get_channel(1025040536513548439)
    text = generate_random_text()
    await message_channel.send(text)


@call_every_6_hours.before_loop
async def before():
    await bot.wait_until_ready()
    print("TWEET")


@tasks.loop(hours=12)
async def call_every_12_hours():
    tweet()


@call_every_12_hours.before_loop
async def cron():
    await bot.wait_until_ready()
    print("CRON")


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


call_every_6_hours.start()
call_every_12_hours.start()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
