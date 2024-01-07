from langchain.schema import AIMessage
from langchain_community.chat_models import ChatOllama


class QBEAR:
  def __init__(self, llm: str):
    self.chat_model = ChatOllama(
      model=llm,
    )

  async def query(self, text: list) -> str:
    try:
      answ = self.chat_model.invoke(text)
      return answ
    except Exception as e:
      print(f"Error in query: {e}")
      return AIMessage(content="Sorry, I encountered an Error")
