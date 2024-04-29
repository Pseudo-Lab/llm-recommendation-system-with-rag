import uuid
from abc import ABC, abstractmethod

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.vectorstores import VectorStoreRetriever


class RagInterface(ABC):
    def __init__(self, prompt_service, vector_service):
        self.vector_service = vector_service
        self.prompt_service = prompt_service

    def run(self, workspace_id: uuid.UUID, top_k: int, threshold: float):
        vector_store = self.get_vector_store(workspace_id=workspace_id)
        retriever = self.set_retriever(vector_store=vector_store, top_k=top_k, threshold=threshold)
        prompt = self.get_prompt(workspace_id=workspace_id)
        model = self.get_model()
        chain = self.create_chain(prompt, model, retriever)
        return chain

    def get_vector_store(self, workspace_id: uuid.UUID):
        return self.vector_service.get_vectorstore(workspace_id=workspace_id)

    def set_retriever(self, vector_store: VectorStoreRetriever, top_k: int, threshold: float):
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": top_k, "score_threshold": threshold})
        return retriever

    def get_prompt(self, workspace_id: uuid.UUID):
        prompt = self.prompt_service.get_by_workspace_id(workspace_id=workspace_id)
        system_message_prompt = SystemMessagePromptTemplate.from_template(prompt.sys_prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template(prompt.user_prompt)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        return chat_prompt

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @abstractmethod
    def get_model(self):
        pass

    def create_chain(self, prompt, model, retriever):
        rag_chain_from_docs = (
                RunnablePassthrough.assign(context=(lambda x: self.format_docs(x['context'])))
                | prompt
                | model
                | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": retriever, "input": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)
        return rag_chain_with_source
