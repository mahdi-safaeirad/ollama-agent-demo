import os 
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
api_url = os.getenv("OLLAMA_API_URL")
api_model = os.getenv("OLLAMA_API_MODEL")

llm = init_chat_model(
    model=api_model,
    api_key=api_key,
    base_url=api_url,
)

memory = InMemorySaver()

thread_config={"configurable":{"thread_id": "123"}}

agent = create_agent(
    model=llm,
    checkpointer=memory
)



response = agent.invoke(
    {"messages": [{"role": "user", "content": "my name is mahdi"}]},
    thread_config
)['messages'][-1].content

print(response)


response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is sum of 1+2"}]},
    thread_config
)['messages'][-1].content

print(response)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is my name"}]},
    thread_config
)['messages'][-1].content

print(response)
