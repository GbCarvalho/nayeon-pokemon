# FastAPI app that also runs the Discord bot inside the same event loop.

import os, asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

# ---- Import bot instance and related logic from main.py ----
# Importing `main` sets up the bot, cronjob, and event handlers without starting it.
import main  # noqa: E402

bot = main.bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the Discord bot when the application starts and clean it up on shutdown."""
    bot_task = asyncio.create_task(bot.start(os.environ["DISCORD_BOT_TOKEN"]))
    try:
        yield
    finally:
        # Gracefully close the bot and wait for the task to finish
        await bot.close()
        await bot_task


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    return {"ok": True}


# When executed directly (`python web_main.py`), run Uvicorn.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("web_main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8080")))