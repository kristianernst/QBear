import asyncio
import logging
import os

import discord
from dotenv import load_dotenv
from langchain.schema import AIMessage, HumanMessage

from model import QBEAR

logging.basicConfig(level=logging.INFO)
load_dotenv()

MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
MODEL = os.getenv("MODEL")

intents = discord.Intents.default()
intents.message_content = True
d_client = discord.Client(intents=intents)

message_nodes = {}
in_progress_message_ids = []


class MessageNode:
    def __init__(self, msg_id, content, replied_to=None):
        self.msg_id = msg_id
        self.content = content
        self.replied_to = replied_to


messages = []
q_bear_instance = QBEAR(MODEL)


@d_client.event
async def on_ready():
    print("We have logged in as {0.user}".format(d_client))


@d_client.event
async def on_message(message):
    if message.author == d_client.user or message.author.bot:
        return

    bot_mentioned = await is_bot_mentioned(message)

    if not bot_mentioned:
        logging.info("Bot not mentioned, won't reply")
        return

    # If user replied to a message that's still generating, wait until it's done
    while message.reference and message.reference.message_id in in_progress_message_ids:
        await asyncio.sleep(0)

    async with message.channel.typing():
        # build conv hist
        conversation_history = []
        current_message = message

        while current_message and len(conversation_history) < MAX_MESSAGES:
            if current_message.author == d_client.user:
                conversation_history.append(AIMessage(content=current_message.content))
            else:
                conversation_history.append(
                    HumanMessage(content=current_message.content)
                )
            if current_message.reference:
                ref_msg_id = current_message.reference.message_id
                current_message = (
                    await message.channel.fetch_message(ref_msg_id)
                    if ref_msg_id
                    else None
                )
            else:
                break

        # reverse conversation history to get the chronological order
        conversation_history = conversation_history[::-1]

        # generate response
        try:
            response = await q_bear_instance.query(
                conversation_history
            )  # Ensure this is the correct way to call your QBEAR instance
            await message.reply(response.content)
        except Exception as e:
            logging.error(f"Error in generating response: {e}")
            await message.reply("Sorry, I encountered an error.")


async def is_bot_mentioned(message):
    """
    Checks if the bot is mentioned in the message or any message in the reply chain.
    """
    current_message = message
    while current_message:
        if d_client.user in current_message.mentions:
            return True
        if current_message.reference:
            try:
                ref_msg_id = current_message.reference.message_id
                current_message = await message.channel.fetch_message(ref_msg_id)
            except discord.NotFound:
                break  # If the referenced message can't be found, break the loop
        else:
            break
    return False


async def main():
    await d_client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
