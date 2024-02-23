from snowflake_llm.snowflake_utils import get_lagchain_connection
from snowflake_llm import config
from snowflake_llm.prompts import snowflake_prompt_template
from snowflake_llm.agent import get_metadata_rag_query_chain
from langchain_openai import ChatOpenAI
from snowflake_llm.metadata import build_faiss_metadata_store
from langchain_core.language_models import BaseChatModel
from snowflake_llm.engine import QueryChatEngine
from langchain_core.vectorstores import VectorStore


def get_meta_store(database=None, schema=None):
    database = database or config.DB_NAME
    schema = schema or config.SCHEMA_NAME
    db = get_lagchain_connection(database, schema)
    return build_faiss_metadata_store(db)



def build_metadata_rag_query_engine(
        metastore: VectorStore,
        database=None,
        schema=None,
        query_builder_prompt: str = None,
        query_llm: BaseChatModel = None,
        chat_llm: BaseChatModel = None
):

    database = database or config.DB_NAME
    schema = schema or config.SCHEMA_NAME
    db = get_lagchain_connection(database, schema)
    query_builder_prompt = query_builder_prompt or snowflake_prompt_template
    query_llm = query_llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chat_llm = chat_llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    query_chain = get_metadata_rag_query_chain(
        retriver=metastore.as_retriever(),
        llm=query_llm,
        prompt_template=query_builder_prompt,
        db_name=database,
        schema_name=schema

    )
    return QueryChatEngine(query_chain, chat_llm, db)
