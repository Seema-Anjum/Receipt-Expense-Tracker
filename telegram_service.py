import asyncio
import os
import streamlit as st
from telegram import Bot


async def _send_message(chat_id, text):

    bot_token = st.secrets[
        "TELEGRAM_BOT_TOKEN"
    ]

    bot = Bot(
        token=bot_token
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text
    )


def send_telegram(chat_id, text):

    asyncio.run(
        _send_message(
            chat_id,
            text
        )
    )