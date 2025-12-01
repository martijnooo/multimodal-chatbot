from langchain.tools import tool
from data_storage.list_documents import list_documents as list_docs_func

@tool
def list_user_documents(user_id: str = "user1"):
    """
    Lists all documents uploaded by the user, including type, summary and uploaded date.
    """
    docs = list_docs_func(user_id)
    if not docs:
        return "No documents found for this user."
    
    output = []
    for uuid, name, doc_type, summary, upload_time in docs:
        output.append(f"- uuid: {uuid} - Source: {name} ({doc_type}) | {upload_time}: {summary}")
    
    return "\n".join(output)
