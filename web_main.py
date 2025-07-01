# web_main.py  (new)
import os, asyncio, nest_asyncio
from fastapi import FastAPI
from discord.ext import commands, tasks

app = FastAPI()

@app.get("/")
async def health():
    return {"ok": True}

# ---- Import bot instance and related logic from main.py ----
# Importing `main` sets up the bot, cronjob, and event handlers, but (after the
# previous edit) does **not** start the bot automatically. We can therefore
# reuse the same code base for both cli-only and web-service executions.

import main  # noqa: E402  (must come after setting up FastAPI)

# `main.bot` is the fully configured discord.py bot instance.
bot = main.bot

async def run_bot():
    await bot.start(os.environ["DISCORD_BOT_TOKEN"])

if __name__ == "__main__":
    # make the existing event loop re-entrant for FastAPI + discord.py
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))