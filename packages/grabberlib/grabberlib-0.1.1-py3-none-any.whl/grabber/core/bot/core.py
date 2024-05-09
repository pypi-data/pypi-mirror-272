import asyncio
from typing import Optional
from aiogram import Bot

from grabber.core.settings import BOT_TOKEN


async def send_message(
    post_text: str,
    retry: Optional[bool] = False,
    posts_counter: Optional[int] = 0,
    retry_counter: Optional[int] = 0,
    sleep_time: Optional[int] = 0,
) -> None:
    try:
        bot = Bot(token=f"{BOT_TOKEN}")
        async with bot.context():
            await bot.send_message(chat_id="@cspmst", text=post_text)
            print(f"Post sent to the channel: {post_text}")
    except Exception:
        sleep_time = 15
        if retry or posts_counter >= 15:
            retry_counter += 1
            asyncio.sleep(sleep_time)
            print(f"Retry number {retry_counter} sending post to channel")

        await send_message(
            post_text=post_text,
            retry=retry and retry_counter <= 50,
            posts_counter=posts_counter,
            retry_counter=retry_counter,
            sleep_time=sleep_time,
        )
