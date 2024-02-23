from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.runnables.history import RunnableWithMessageHistory


from snowflake_llm.snowflake_utils import get_lagchain_connection
from langchain_core.runnables.history import RunnableWithMessageHistory
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from snowflake_llm.prompts import snowflake_prompt_template
from langchain_core.prompts import PromptTemplate
from snowflake_llm import config


def augment_prompt_with_db_info(prompt, db_name, schema_name):
    prompt = prompt.replace("<<db_name>>", db_name)
    prompt = prompt.replace("<<schema_name>>", schema_name)
    return prompt


def get_simple_query_chain(db: SQLDatabase = None, llm: any = None):
    db = db or get_lagchain_connection()
    llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    query_writer_chain = create_sql_query_chain(llm, db)
    return query_writer_chain


def get_metadata_rag_query_chain(retriver, llm=None, prompt_template=None,
                                 db_name=None, schema_name=None):

    db_name = db_name or config.DB_NAME
    schema_name = schema_name or config.SCHEMA_NAME
    llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print(f"usinf {llm }")
    prompt_template = prompt_template or snowflake_prompt_template
    prompt_template = augment_prompt_with_db_info(
        prompt_template, db_name, schema_name)
    prompt = PromptTemplate.from_template(prompt_template)

    print(prompt)

    rag_query_writer_chain = (
        {
            "context": itemgetter("question") | retriver,
            "question": itemgetter("question"),
        }
        | RunnableParallel(
            question=lambda x: x['question']+"\nSQLQuery: ",
            context=RunnablePassthrough(),
        )
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
        | (lambda text: text.strip())
    )
    return rag_query_writer_chain


def create_answer_chain_from_query(query_writer_chain, llm=None, db=None):
    db = db or get_lagchain_connection()
    llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    execute_query = QuerySQLDataBaseTool(db=db)
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query,
        and SQL result, answer the user question.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )

    answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=query_writer_chain).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )

    return chain
