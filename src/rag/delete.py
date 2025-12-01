from rag.base import ensure_index


def delete_pinecone_records(uuid: str):
    # Connect to your index
    index = ensure_index()

    # Define the metadata filter
    metadata_filter = {
        "document_uuid": uuid,
    }

    # Perform the delete operation with the filter
    index.delete(filter=metadata_filter, namespace="ns1")

    print("Vectors matching the metadata filter have been deleted.")