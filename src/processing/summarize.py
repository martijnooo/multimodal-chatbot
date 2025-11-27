from langchain_openai import ChatOpenAI
from langsmith import traceable

@traceable
def create_summary(text):  
    llm = ChatOpenAI(
        model="gpt-5-nano"
    )
    messages = [
        (
            "system",
            "You are a text summariser. Provide a summary of the  text",
        ),
        ("human", text),
    ]
    response = llm.invoke(messages)
  
    return response.text