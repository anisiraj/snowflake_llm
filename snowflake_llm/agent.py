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


def get_query_chain(db: SQLDatabase = None, llm: any = None):
    db = db or get_lagchain_connection()
    llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    execute_query = QuerySQLDataBaseTool(db=db)
    query_writer_chain = create_sql_query_chain(llm, db)
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
    
    return chain, query_writer_chain
