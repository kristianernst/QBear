# QBear
- Edgy tech bro, discord bot, and a friend to all.
- Run it locally blazingly fast on your M1 Max or equivalent.
- Only 100 lines of python code.

![demo](/assets/example.png)

## Instructions
This is a discord bot that is meant to be hosted locally from your PC.
It leverages the discord.py library to interact with the discord API.
It also uses the ``langchain`` library together with ``Ollama`` to connect local Chat-based LLMS to the discord bot. Instead of this procedure, you could also directly utilize the RESTAPI of other LLMs locally or remotely.

### Installation
1. Clone the repository
2. Install the requirements.txt
3. Create a ``.env`` file in the root directory of the project, based on the ``.env.example`` file
4. Create a discord bot and add it to your server, give it all bot permissions as specified in this [video](https://www.youtube.com/watch?v=ztyRvknzQaM&t=336s) by a man with a fancy mustache.
5. Install the [Ollama](https://ollama.ai/) app, and create a local chat-based LLM. You can find the instructions [here](https://github.com/jmorganca/ollama), I have included my Modelfile for inspiration.
6. Run ollama by simply opening the app.
7. Run the bot with ``python main.py``
8. You should be good to go!, ``@<bot>`` to get the bot's attention in the channel.
