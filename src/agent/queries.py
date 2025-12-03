def run_query_with_memory(agent, prompt, memory_id, file_context):
    messages = []

     # Inject file metadata as a system-level memory block
    if file_context:
        context_block = "New files have been uploaded:\n\n"
        for file in file_context:
            context_block += (
                f"File: {file['source']}\n"
                f"UUID: {file['uuid']}\n"
                f"Type: {file['type']}\n"
                f"Summary: {file['summary']}\n"
                "Use the tools 'retrival' or 'time_based_retrieval' to access details.\n\n"
            )
        
        messages.append({"role": "system", "content": context_block})

    # Add user query
    messages.append({"role": "user", "content": prompt})

    # Call agent with memory
    response = agent.invoke(
        {"messages": messages},
        config={"configurable": {"thread_id": memory_id}}
    )

    return response["messages"][-1].content