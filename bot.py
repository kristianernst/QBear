import asyncio
import os
import discord
from langchain.schema import AIMessage, HumanMessage
from model import QBEAR
from dotenv import load_dotenv; load_dotenv()
import logging; logging.basicConfig(level=logging.INFO)

d_client = discord.Client(intents=discord.Intents.default())
q_bear_instance = QBEAR(os.getenv("MODEL"))
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))


@d_client.event
async def on_ready():
  print(f"We have logged in as {d_client.user}")


@d_client.event
async def on_message(message):
  if (message.author == d_client.user or message.author.bot or not await is_bot_mentioned(message)): return
  
  async with message.channel.typing(): 
    conversation_history = await build_conversation_history(message)
    try:
      response = await q_bear_instance.query(conversation_history)
      if len(response.content) > 2000:
        response.content = response.content[:1800]
        await message.reply(f"Truncated output\n\n{response.content} ")
      else:  
        await message.reply(response.content)
    except Exception as e:
      logging.error(f"Error in generating response: {e}")
      await message.reply("Sorry, I encountered an error.")


async def is_bot_mentioned(message):
  current_message = message
  while current_message:
    if d_client.user in current_message.mentions:
      return True
    current_message = await get_referenced_message(current_message)
  return False


async def get_referenced_message(message):
  try:
    return (
      await message.channel.fetch_message(message.reference.message_id)
      if message.reference
      else None
    )
  except discord.NotFound:
    return None


async def build_conversation_history(message):
  history, current_message = [], message
  while current_message and len(history) < MAX_MESSAGES:
    content = current_message.content
    message_type = (
      AIMessage if current_message.author == d_client.user else HumanMessage
    )
    history.append(message_type(content=content))
    current_message = await get_referenced_message(current_message)
  return history[::-1]


async def main():
  await d_client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
  asyncio.run(main())
