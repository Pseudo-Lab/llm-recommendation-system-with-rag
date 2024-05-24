import logging
import uuid
import os
import json
from typing import Optional, Sequence

from langchain.chains.query_constructor.base import StructuredQueryOutputParser, get_query_constructor_prompt, \
    load_query_constructor_runnable
from langchain.chains.query_constructor.ir import Comparator, Operator
from langchain.chains.query_constructor.prompt import DEFAULT_PREFIX, DEFAULT_SUFFIX, EXAMPLES_WITH_LIMIT, \
    EXAMPLE_PROMPT, DEFAULT_EXAMPLES, DEFAULT_SCHEMA_PROMPT, SCHEMA_WITH_LIMIT_PROMPT
from langchain.retrievers import SelfQueryRetriever
from langchain.retrievers.self_query.elasticsearch import ElasticsearchTranslator
from langchain_core.prompts import FewShotPromptTemplate, BasePromptTemplate
from langchain_openai import ChatOpenAI

from utils.prompts import MOVIE_DATA_SOURCE, MOVIE_DEFAULT_EXAMPLES
from utils.self_query_meta import metadata_field_info
from vector.vector_store import VectorStoreInterface


class RetrievalService:
    def __init__(self, vector: VectorStoreInterface):
        self.vector = vector

    async def similarity_search(self, workspace_id: uuid.UUID, input: str, k: int):
        vs = self.vector.get_vector_store(workspace_id=workspace_id)
        docs = vs.similarity_search_with_score(input, k=k)
        return docs

    async def ensemble_search(self, workspace_id, input, top_k):
        #TODO: bm25 + dense + self-query
        pass

    async def similarity_search_with_self_query(self, workspace_id: uuid.UUID, input: str, k: int):
        # https://github.com/langchain-ai/langchain/blob/master/cookbook/self_query_hotel_search.ipynb
        document_content_description = "영화를 추천해주세요."
        model = ChatOpenAI(
            temperature=0,
            model_name=os.getenv("LLM_MODEL_NAME"),
            verbose=True
        )
        # 자연어 질의 -> filter query
        prompt = self.custom_query_constructor_prompt(
            document_content_description,
            metadata_field_info,
        )

        output_parser = StructuredQueryOutputParser.from_components()
        query_constructor = prompt | model | output_parser
        vs = self.vector.get_vector_store(workspace_id=workspace_id)
        retriever = SelfQueryRetriever(
            query_constructor=query_constructor,  # 이전에 생성한 쿼리 생성기
            vectorstore=vs,  # 벡터 저장소를 지정
            structured_query_translator=ElasticsearchTranslator(),
            search_kwargs={"k": k}
        )
        docs = await retriever.ainvoke(input)
        return docs


    def custom_query_constructor_prompt(
            self,
            document_contents: str,
            attribute_info,
            enable_limit: bool = False,
            schema_prompt: Optional[BasePromptTemplate] = None,
            allowed_operators: Sequence[Operator] = tuple(Operator),
            allowed_comparators: Sequence[Comparator] = tuple(Comparator),
            examples: Optional[Sequence] = None,
    ):
        default_schema_prompt = (
            SCHEMA_WITH_LIMIT_PROMPT if enable_limit else DEFAULT_SCHEMA_PROMPT
        )
        schema_prompt = schema_prompt or default_schema_prompt

        info_dicts = {}
        for i in attribute_info:
            i_dict = dict(i)
            info_dicts[i_dict.pop("name")] = i_dict
        attribute_str = json.dumps(info_dicts, indent=4, ensure_ascii=False).replace("{", "{{").replace("}", "}}")

        schema = schema_prompt.format(
            allowed_comparators=" | ".join(allowed_comparators),
            allowed_operators=" | ".join(allowed_operators),
        )
        examples = examples or (
            # EXAMPLES_WITH_LIMIT if enable_limit else DEFAULT_EXAMPLES
            EXAMPLES_WITH_LIMIT if enable_limit else MOVIE_DEFAULT_EXAMPLES
        )
        example_prompt = EXAMPLE_PROMPT
        prefix = DEFAULT_PREFIX.format(schema=schema)
        suffix = DEFAULT_SUFFIX.format(
            i=len(examples) + 1, content=document_contents, attributes=attribute_str
        )
        return FewShotPromptTemplate(
            examples=list(examples),
            example_prompt=example_prompt,
            input_variables=["query"],
            suffix=suffix,
            prefix=prefix,
        )

