import uuid
import os
import json
from typing import Optional, Sequence

from langchain.chains.query_constructor.base import get_query_constructor_prompt, StructuredQueryOutputParser
from langchain.chains.query_constructor.ir import Comparator, Operator
from langchain.chains.query_constructor.prompt import DEFAULT_PREFIX, DEFAULT_SUFFIX, EXAMPLES_WITH_LIMIT, \
    EXAMPLE_PROMPT, DEFAULT_EXAMPLES, DEFAULT_SCHEMA_PROMPT, SCHEMA_WITH_LIMIT_PROMPT, USER_SPECIFIED_EXAMPLE_PROMPT, \
    PREFIX_WITH_DATA_SOURCE, SUFFIX_WITHOUT_DATA_SOURCE
from langchain.retrievers import SelfQueryRetriever
from langchain.retrievers.self_query.chroma import ChromaTranslator
from langchain_core.prompts import FewShotPromptTemplate, BasePromptTemplate
from langchain_openai import ChatOpenAI

from app.utils.self_query import metadata_field_info


class RetrievalService:
    def __init__(self, vector):
        self.vector = vector

    def similarity_search(self, workspace_id: uuid.UUID, input: str, k: int):
        vs = self.vector.get_vector(workspace_id=workspace_id)
        docs = vs.similarity_search_with_score(input, k=k)
        return docs

    async def similarity_search_with_self_query(self, workspace_id: uuid.UUID, input: str):
        document_content_description = "영화 정보"
        vs = self.vector.get_vector(workspace_id=workspace_id)

        model = ChatOpenAI(
            temperature=0,
            model_name=os.getenv("LLM_MODEL_NAME"),
            verbose=True
        )

        # prompt = get_query_constructor_prompt(
        #     document_content_description,
        #     metadata_field_info,
        # )
        prompt = self.custom_query_constructor_prompt(
            document_content_description,
            metadata_field_info,
        )
        print(prompt.format(query=input))
        output_parser = StructuredQueryOutputParser.from_components()
        query_constructor = prompt | model | output_parser

        retriever = SelfQueryRetriever(
            query_constructor=query_constructor,  # 이전에 생성한 쿼리 생성기
            vectorstore=vs,  # 벡터 저장소를 지정
            structured_query_translator=ChromaTranslator()
        )# 쿼리 변환기
        docs = retriever.invoke(input)
        print(docs)

        # response = await query_constructor.ainvoke(input)
        # print(prompt.format(query=input))
        # print(response)
        # retriever = SelfQueryRetriever.from_llm(
        #     model,
        #     vs,
        #     document_content_description,
        #     metadata_field_info,
        #     enable_limit=True,
        #     search_kwargs={"k": 2}
        # )
        # return await retriever.ainvoke(input)

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
            EXAMPLES_WITH_LIMIT if enable_limit else DEFAULT_EXAMPLES
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