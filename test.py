import asyncio
import os

from dotenv import load_dotenv
from langchain.schema import HumanMessage

from model import QBEAR

load_dotenv()

q_bear_instance = QBEAR(llm=os.getenv("MODEL"))


async def main():
    messages = [HumanMessage(content="Hello, I am a human")]
    print(q_bear_instance.chat_model.model)
    answ = await q_bear_instance.query(messages)
    print(f"answer: {answ}")


if __name__ == "__main__":
    answ = asyncio.run(main())
