from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
from agent.tools.pinecone_retrival import retrival
from agent.tools.sql_retrival import list_user_documents
from langsmith import traceable
from agent.prompt_templates import base_system_prompt

@traceable
def setup_agent(system_prompt: str = base_system_prompt):
    agent = create_agent(
        "gpt-5",
        [retrival, list_user_documents],
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt  
    )

    return agent