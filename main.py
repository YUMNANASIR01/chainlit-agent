import os 
from dotenv import load_dotenv
from agents import Agent,OpenAIChatCompletionsModel, Runner,set_tracing_disabled
from openai import AsyncOpenAI
import chainlit as cl

load_dotenv()

set_tracing_disabled(disabled=True)

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
#----------------------------------------
history = []
# ---------------

client = AsyncOpenAI(
    api_key=OPEN_ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

agent = Agent(
     model = OpenAIChatCompletionsModel(model="deepseek/deepseek-chat-v3-0324:free", openai_client=client),
     name = "my_agent",
     instructions = "you are a helpful assistant",
)

# ----------------------------------------------

@cl.on_message
async def main(message: cl.Message):
    ui_question = message.content  

    # User ka message history mein add karo
    history.append({"role": "user", "content": ui_question})

    res = Runner.run_sync(agent, history)  # async call

    # Assistant ka jawab bhi history mein add karo
    history.append({"role": "assistant", "content": res.final_output})

    await cl.Message(content=res.final_output).send()



# @cl.on_message
# async def main(message: cl.Message):
#     ui_question = message.content
    
#     res =  Runner.run_sync(agent, ui_question)
#     print(res.final_output)

#     await cl.Message(content=res.final_output).send()
    # await cl.Message(content="What is your name?").send()

# jawab = Runner.run_sync(agent, "What is your name?")
# print(jawab.final_output)