from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from typing import List
from snowflake_llm.snowflake_utils import get_lagchain_connection
from langchain_core.vectorstores import VectorStore


def convert_table_info_to_documents(table_info) -> List[Document]:
    """_summary_

        split db description in per table DDL definition as t follows a specific format starting with create
    """
    s = ['CREATE'+d for d in table_info.split('CREATE') if d.strip()]
    docs = [Document(page_content=x) for x in s]
    return docs


def table_list_document(table_names):
    info = f"tables_in_the_schema [ {','.join(table_names)}]"
    return Document(page_content=info)


def build_faiss_metadata_store(
        db: SQLDatabase) -> VectorStore:
    """_summary_

    Args:
        db (SQLDatabase): connector for SQL engine

    Returns:
        Dict[str, Any]: _description_
    """
    embeddings = OpenAIEmbeddings()
    table_names = db.get_usable_table_names()
    table_info = db.get_table_info(table_names)
    db = db or get_lagchain_connection()

    documents = convert_table_info_to_documents(table_info)
    # if include_table_names_as_metadta:
    #     documents.append(table_list_document(table_names))

    metadata_vector_store = FAISS.from_documents(documents, embeddings)
    return metadata_vector_store
