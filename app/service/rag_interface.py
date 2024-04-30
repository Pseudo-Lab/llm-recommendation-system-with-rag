import uuid
import os
from abc import ABC, abstractmethod
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

from app.database.chroma_db import ChromaDB


class RagInterface(ABC):
    def __init__(self, vector_service):
        self.vector_service = vector_service

    async def run(self, workspace_id: uuid.UUID, top_k: int, threshold: float, input: str, stream: bool = False):
        retriever = self.set_retriever(workspace_id=workspace_id, top_k=top_k, threshold=threshold)
        prompt = '''template="You are an assistant for question-answering tasks. 
                Use the following pieces of retrieved context to answer the question. 
                If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

                \nQuestion: {question} 

                \nContext: {context} 

                \nAnswer:"'''
        model = self.get_model()
        chain = self.create_chain(prompt, model, retriever)
        if not stream:
            response = await self.gen_text(chain, input=input)
            return response

    def set_retriever(self, workspace_id: uuid.UUID, top_k: int, threshold: float):
        vector_path = f'{os.getenv("VECTOR_DB_PATH_PREFIX")}{workspace_id}'
        vs = ChromaDB.get_vectorstore(vector_path)
        retriever = vs.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": top_k, "score_threshold": threshold})
        return retriever

    # def get_prompt(self, workspace_id: uuid.UUID):
    #     prompt = self.prompt_service.get_by_workspace_id(workspace_id=workspace_id)
    #     system_message_prompt = SystemMessagePromptTemplate.from_template(prompt.sys_prompt)
    #     human_message_prompt = HumanMessagePromptTemplate.from_template(prompt.user_prompt)
    #     chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    #     return chat_prompt

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

    async def gen_text(self, chain, input: str):
        response = await chain.ainvoke(input)
        return response


class OpenAIRag(RagInterface):
    def get_model(self):
        return ChatOpenAI(
            temperature=os.getenv("LLM_TEMPERATURE"),
            model_name=os.getenv("LLM_MODEL"),
        )
