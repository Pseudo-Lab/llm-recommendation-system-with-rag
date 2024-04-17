import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.service.vector_service import VectorService
from langchain_openai import ChatOpenAI

class GenService:
    def __init__(self, vector_service: VectorService):
        self.vector_service = vector_service

        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_API_KEY")
        )

    def gen_response(self, workspace_id, input):
        vector_store = self.vector_service.get_vector(workspace_id=workspace_id)
        retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
                                             search_kwargs={"k": 2, "score_threshold": 0.1})

        from langchain import hub
        prompt = hub.pull("rlm/rag-prompt")

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
        )
        print(prompt)
        response = rag_chain.invoke(input=input)
        print(response)
        return response