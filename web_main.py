# FastAPI app that also runs the Discord bot inside the same event loop.

import os, asyncio
from fastapi import FastAPI

# ---- Import bot instance and related logic from main.py ----
# Importing `main` sets up the bot, cronjob, and event handlers without starting it.
import main  # noqa: E402

bot = main.bot


app = FastAPI()


@app.get("/")
async def health():
    return {"ok": True}


# Start the Discord bot when the FastAPI application starts, and close it on
# shutdown. This keeps everything within Uvicorn's event loop and avoids
# warnings about un-awaited coroutines.


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(os.environ["DISCORD_BOT_TOKEN"]))


@app.on_event("shutdown")
async def shutdown_event():
    await bot.close()


# When executed directly (`python web_main.py`), run Uvicorn.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("web_main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8080")))