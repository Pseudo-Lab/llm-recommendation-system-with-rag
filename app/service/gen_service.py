import asyncio
import os
import uuid
import time
from typing import AsyncIterable, Awaitable
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.retrievers import SelfQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from service.rag_interface import RagTemplate
from langchain_openai import ChatOpenAI
from utils.timer import atimer
from vector.vector_store import VectorStoreInterface


class GenService:
    def __init__(self, rag: RagTemplate):
        self.rag = rag

    # @staticmethod
    async def gen_response_stream(self, input: str, workspace_id: uuid.UUID) -> AsyncIterable[str]:
        print("들어왔다.")
        callback = AsyncIteratorCallbackHandler()
        model = ChatOpenAI(
            temperature=0,
            model_name=os.getenv("LLM_MODEL_NAME"),
            streaming=True,
            verbose=True,
            callbacks=[callback],
        )
        import time
        start_time = time.time()
        vs = self.vector_store.get_vector_store(workspace_id=workspace_id)
        retriever = vs.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 2, "score_threshold": 0.1}
        )

        prompt = '''template="You are an assistant for question-answering tasks. 
                Use the following pieces of retrieved context to answer the question. 
                If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

                \nQuestion: {question} 

                \nContext: {context} 

                \nAnswer:"'''

        from langchain_core.prompts import PromptTemplate
        custom_rag_prompt = PromptTemplate.from_template(prompt)
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | custom_rag_prompt
                | model
                | StrOutputParser()
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("총 소요 시간:", elapsed_time, "초")
        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
            try:
                await fn
            except Exception as e:
                # TODO: handle exception
                print(f"Caught exception: {e}")
            finally:
                # Signal the aiter to stop.
                event.set()

        task = asyncio.create_task(wrap_done(
            rag_chain.ainvoke(input=input),
            callback.done),
        )

        async for token in callback.aiter():
            yield token
        await task

    @atimer
    async def gen_response(self, workspace_id, input):
        response = await self.rag.run(
            workspace_id=workspace_id,
            top_k=2,
            threshold=0.7,
            input=input,
            stream=False
        )
        return response