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

@bot.tree.command(name="roll", description="Gooi een dobbelsteen")
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
    await interaction.response.send_message("Meow! :3")


@bot.tree.command(name="ping", description="Speel ping pong met Fujisaki!")
async def ping(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    await interaction.response.send_message("Pong! :3")

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

    embed.add_field(name="/roll", value="Roll a dice!", inline=False)
    embed.add_field(name="/meow", value="Make Fujisaki meow :3", inline=False)
    embed.add_field(name="/suggest", value="Post a suggestion with yes/no voting", inline=False)
    embed.add_field(name="/ping", value="Play ping pong with Fujisaki!", inline=False)
    embed.add_field(name="/sing", value="Make Fujisaki sing a song!", inline=False)
    embed.add_field(name="/say", value="Make Fujisaki say something!", inline=False)

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
    await interaction.response.send_message(f"{interaction.user.mention} throws {target.mention} into the air! :3")

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

@bot.tree.command(name="sing", description="Make Fujisaki sing a song!")
async def sing(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message(
            f"Use this command in {allowed_channels_text()}.",
            ephemeral=True
        )
        return
    await interaction.response.send_message("Lalalalala :3")

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

with open("token.txt", "r", encoding="utf-8") as token_file:
    DISCORD_TOKEN = token_file.read().strip()

if not DISCORD_TOKEN:
    raise ValueError("token.txt is leeg. Zet je Discord bot token in token.txt")

bot.run(DISCORD_TOKEN)