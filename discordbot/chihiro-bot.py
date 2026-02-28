import discord
from discord.ext import commands
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
allowed_channels_raw = os.getenv("ALLOWED_CHANNEL_IDS", os.getenv("ALLOWED_CHANNEL_ID", "1476578414126174480,1367829004354060339"))
ALLOWED_CHANNEL_IDS = {
    int(channel_id.strip())
    for channel_id in allowed_channels_raw.split(",")
    if channel_id.strip().isdigit()
}
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

def is_allowed_channel(channel_id: int) -> bool:
    if not ALLOWED_CHANNEL_IDS:
        return True
    return channel_id in ALLOWED_CHANNEL_IDS

def allowed_channels_text() -> str:
    return ", ".join(f"<#{channel_id}>" for channel_id in sorted(ALLOWED_CHANNEL_IDS))

async def gooi6(interaction: discord.Interaction):
    await interaction.response.send_message(str(random.randint(1, 6)))

# Commands
# ______________________________________________________________________________________________


@bot.tree.command(name="roll", description="Throw a dice and see what you get!")
async def roll(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    await gooi6(interaction)

@bot.tree.command(name="meow", description="Make Fujisaki meow!")
async def meow(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    meow_responses = [
        "Meow! :3",
        "Mrrrow~ :3",
        "Nyaa~ :3",
        "*purrs softly* :3",
        "Mew mew! :3",
        "*tilts head* ...meow? :3",
        "MEOOOW! >:3",
        "*nuzzles* Meow~ :3",
    ]
    await interaction.response.send_message(random.choice(meow_responses))


@bot.tree.command(name="ping", description="Speel ping pong met Fujisaki!")
async def ping(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    ping_responses = [
        "Pong! :3",
        "Pong! ...did I win? :3",
        "*hits the ball back* Pong! :3",
        "P-pong! :3",
        "Pong pong pong! :3",
        "🏓 Pong! :3",
        "*swings racket* Pong! :3",
    ]
    await interaction.response.send_message(random.choice(ping_responses))

@bot.tree.command(name="help", description="Show all bot commands.")
async def help(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="Help",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )

    embed.add_field(name="/help", value="Show this help message", inline=False)
    embed.add_field(name="/roll", value="Roll a dice!", inline=False)
    embed.add_field(name="/meow", value="Make Fujisaki meow :3", inline=False)
    embed.add_field(name="/suggest", value="Post a suggestion with yes/no voting", inline=False)
    embed.add_field(name="/ping", value="Play ping pong with Fujisaki!", inline=False)
    embed.add_field(name="/sing", value="Make Fujisaki sing a song!", inline=False)
    embed.add_field(name="/say", value="Make Fujisaki say something!", inline=False)
    embed.add_field(name="/throw", value="Make Fujisaki throw someone!", inline=False)
    embed.add_field(name="/greet", value="Make Fujisaki greet someone!", inline=False)
    embed.add_field(name="/wruff", value="Make Fujisaki wruff!", inline=False)
    embed.add_field(name="/eight-ball", value="Ask the magic eight ball a question!", inline=False)

    embed.set_footer(text="Made with <3 by Kiki :3")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="throw", description="Make Fujisaki throw someone!")
@app_commands.describe(target="Mention the person you want Fujisaki to throw")
async def throw(interaction: discord.Interaction, target: discord.Member):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    throw_responses = [
        f"{interaction.user.mention} throws {target.mention} into the air! :3",
        f"{interaction.user.mention} yeets {target.mention} into orbit! :3",
        f"{interaction.user.mention} gently tosses {target.mention} into a pile of pillows! :3",
        f"{interaction.user.mention} launches {target.mention} into the stratosphere! :3",
        f"{target.mention} got thrown by {interaction.user.mention}! Ouchie! :3",
        f"{interaction.user.mention} picks up {target.mention} and spins them around! Wheee~ :3",
        f"{interaction.user.mention} tried to throw {target.mention}... but {target.mention} was too heavy! :3",
    ]
    await interaction.response.send_message(random.choice(throw_responses))

@bot.tree.command(name="suggest", description="Post a suggestion with yes/no voting")
@app_commands.describe(idea="Type your suggestion")
async def suggest(interaction: discord.Interaction, idea: str):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="New Suggestion",
        description=idea,
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Suggested by {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)
    suggestion_message = await interaction.original_response()
    await suggestion_message.add_reaction("✅")
    await suggestion_message.add_reaction("❌")

@bot.tree.command(name="say", description="Make Fujisaki say something!")
@app_commands.describe(text="Type what you want Fujisaki to say")
async def say(interaction: discord.Interaction, text: str):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    await interaction.response.send_message(text)

@bot.tree.command(name="greet", description="Make Fujisaki greet someone!")
@app_commands.describe(target="Mention the person you want Fujisaki to greet!")
async def greet(interaction: discord.Interaction, target: discord.Member):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    greet_responses = [
        f"Fujisaki greets {target.mention}!",
        f"Fujisaki says: Hello {target.mention}!",
        f"Fujisaki says: Haiiii {target.mention}!",
        f"Fujisaki waves at {target.mention} and says: Konnichiwa~!",
        f"Fujisaki bows to {target.mention} and says: Yoroshiku onegaishimasu~!",
        f"Fujisaki gives {target.mention} a big smile and says: Nice to meet you, {target.mention}!",
    ]
    await interaction.response.send_message(random.choice(greet_responses))

@bot.tree.command(name="wruff", description="Make Fujisaki wruff!")
async def wruff(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    wruff_responses = [
        "Wruff! :3",
        "Fujisaki wruffs at you! :3",
        "*wruffs softly* :3",
        "Wruff wruff! :3",
    ]
    await interaction.response.send_message(random.choice(wruff_responses))

@bot.tree.command(name="sing", description="Make Fujisaki sing a song!")
async def sing(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    sing_responses = [
        "Lalalalala~ :3",
        "Fujisaki is singing a song! :3",
        "🎵 Do re mi fa sol la ti do~ :3",
        "*hums a gentle melody* :3",
        "🎶 Twinkle twinkle little star~ :3",
        "*grabs microphone* AAAAAAA— I mean... la la la~ :3",
        "*singing softly* You are my sunshine~ :3",
        "🎤 *clears throat* ...meow meow meow meow~ :3",
    ]
    await interaction.response.send_message(random.choice(sing_responses))

@bot.tree.command(name="eight-ball", description="Ask the magic eight ball a question!")
@app_commands.describe(question="Type your question for the magic eight ball")
async def eight_ball(interaction: discord.Interaction, question: str):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    eight_ball_responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await interaction.response.send_message(f"🎱 {random.choice(eight_ball_responses)}")

# _____________________________________________________________________________________________
# End of commands

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not hasattr(bot, "synced"):
        if GUILD_ID != 0:
            guild = discord.Object(id=GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"Synced slash commands to guild {GUILD_ID}")
        else:
            await bot.tree.sync()
            print("Synced slash commands globally")
        bot.synced = True

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

import os as _os
_token_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "token.txt")
with open(_token_path, "r", encoding="utf-8") as token_file:
    DISCORD_TOKEN = token_file.read().strip()

if not DISCORD_TOKEN:
    raise ValueError("token.txt is leeg. Zet je Discord bot token in .token.txt")

bot.run(DISCORD_TOKEN)