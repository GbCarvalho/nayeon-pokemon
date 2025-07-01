from discord.ext import commands, tasks
import os, random, asyncio

SPECIFIED_USER_ID = int(os.getenv("SPECIFIED_USER_ID", "0"))
CRON_JOB_HOURS = int(os.getenv("CRON_JOB_HOURS", "1"))
POKEMON_CHANNEL = int(os.getenv("POKEMON_CHANNEL"))
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is required")

if not POKEMON_CHANNEL:
    raise RuntimeError("POKEMON_CHANNEL is required")

EMOJIS = ['❤️', '💖', '💗', '💓', '💕', '💞', '💘', '😍', '🥰', '😘', '😻']

# Counter to track how many times the cronjob has executed.
# After six executions, a different set of commands will be dispatched.
execution_count = 0

bot = commands.Bot(command_prefix='Ipe ', bot=False)

@tasks.loop(hours=CRON_JOB_HOURS)
async def cronjob1():
    global execution_count
    execution_count += 1
    print(f'Cronjob 1 executed (count={execution_count})')

    channel = bot.get_channel(POKEMON_CHANNEL)

    if channel is None:
        print('Channel not found.')
        return

    # Every sixth execution, send the special commands instead of the default one.
    if execution_count >= 3:
        await channel.send('$p')
        await asyncio.sleep(1)
        await channel.send('$arl')
        # Brief delay to avoid rate-limit issues and preserve order.
        await asyncio.sleep(1)
        await channel.send('$p 25')
        execution_count = 0  # Reset the counter after the special execution.
    else:
        await channel.send('$p')


@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    if not cronjob1.is_running():
        cronjob1.start()


@bot.event
async def on_message(message):
    is_expected_user_message = (message.author.id == SPECIFIED_USER_ID and message.content.startswith("$p"))
    if is_expected_user_message and random.random() < 0.7:
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await message.add_reaction(random.choice(EMOJIS))

    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


# When executed directly (e.g. `python main.py`), run the bot as a standalone
# background process without a web server.
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
