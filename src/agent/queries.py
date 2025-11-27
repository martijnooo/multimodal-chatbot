def run_query_with_memory(agent, prompt, memory_id, file_context):
    messages = []

    # Add dynamic context as assistant message if available
    if file_context:
        file_input = (
            "A new document has been uploaded.\n"
            f"- Type: {file_context['type']}\n"
            f"- Source: {file_context['source']}\n"
            f"- Summary: {file_context['summary']}\n"
            "You may use the `retrival` tool to explore more details."
        )
        messages.append({"role": "assistant", "content": file_input})

    # Add user query
    messages.append({"role": "user", "content": prompt})

    # Call agent with memory
    response = agent.invoke(
        {"messages": messages},
        config={"configurable": {"thread_id": memory_id}}
    )

    return response["messages"][-1].content