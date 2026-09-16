import os 
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import AIMessageChunk
from langchain.tools import tool

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
api_url = os.getenv("OLLAMA_API_URL")
api_model = os.getenv("OLLAMA_API_MODEL")

llm = init_chat_model(
    model=api_model,
    api_key=api_key,
    base_url=api_url,
)

@tool(
    'get_user_department_info',
    description="LOOK FOR USER DEPATMENT",
    return_direct=False
)

def get_user_department_info (user_Id: str) -> str: 
    match user_Id:
        case "1":
            return "HR" 
        case "2":
            return "Marketing" 
        case "3":
            return "Sale" 
        case _ : 
            return " NOT " 
            


memory = InMemorySaver()

thread_config={"configurable":{"thread_id": "123"}}

agent = create_agent(
    model=llm,
    tools=[get_user_department_info],
    checkpointer=memory
)


while True:
    print("="*30)
    user_message = input("USER: [for exit press exit or quit]: \n")
    if user_message.lower() == "exit" or user_message.lower() == "quit":
        print("EXITING... , bye bye \n")
        break
    
    elif user_message.lower() == "clear" :
        memory.delete_thread(thread_config["configurable"]["thread_id"])
        print("memory clear \n")
        continue

    for chunck , metadata in agent.stream(
        {"messages": [{"role": "user", "content": user_message}]},
        thread_config,
        stream_mode="messages"
    ): 
        if chunck.content and isinstance(chunck, AIMessageChunk):
             print(chunck.content , end='', flush=True)
    
    print('\n')
