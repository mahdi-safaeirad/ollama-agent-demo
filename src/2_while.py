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


agent = create_agent(
    model=llm,
    checkpointer=memory
)

thread_config={"configurable":{"thread_id": "123"}}


while True:
    user_message = input("tell me how can i help you?(for exit press exit or quit): ")
    if user_message.lower() == "exit" or user_message.lower() == "quit":
        print("EXITING... , bye bye \n")
        break
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        thread_config
    )['messages'][-1].content
    print(response)
