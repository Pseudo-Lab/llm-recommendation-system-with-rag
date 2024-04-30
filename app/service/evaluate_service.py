def retrieve_doc_ids(retriever, question: str) -> List[str]:
    docs = retriever.get_relevant_documents(question)
    return [doc.metadata["source"] for doc in docs]