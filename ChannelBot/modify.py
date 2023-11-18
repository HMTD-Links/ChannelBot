import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors.exceptions import FloodWait
from ChannelBot.database.channel_sql import (
    get_buttons
)
from ChannelBot.string_to_buttons import string_to_buttons


# def all_channels():
#     channels = SESSION.query(Channel).all()
#     channels_ids = [channel.channel_id for channel in channels]
#     SESSION.close()
#     return channels_ids


@Client.on_message(filters.channel & ~filters.forwarded)
async def modify(_, msg: Message):
    channel_id = msg.chat.id
    buttons = await get_buttons(channel_id)
    try:
            if buttons:
                buttons = await string_to_buttons(buttons)
            if buttons:
                await msg.edit_text(
                    caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await msg.edit_text(
                    caption,
                    disable_web_page_preview=disable_webpage_preview
                )
    except FloodWait as e:
        await asyncio.sleep(e.x)
