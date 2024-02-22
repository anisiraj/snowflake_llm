
from langchain_openai import ChatOpenAI
from snowflake_llm.agent import get_simple_query_chain, get_metadata_rag_query_chain, create_answer_chain_from_query
from snowflake_llm.snowflake_utils import get_lagchain_connection


class QueryChatEngine(object):
    def __init__(self, query_builder_chain=None, chat_llm=None, db=None):
        self.query_builder_chain = query_builder_chain
        self.chat_llm = chat_llm or ChatOpenAI(
            model="gpt-3.5-turbo", temperature=0)
        self.db = db or get_lagchain_connection()

    @property
    def answer_chain(self):
        return create_answer_chain_from_query(self.query_builder_chain,
                                              llm=self.chat_llm,
                                              db=self.db)

    def answer(self, question):
        try:
            return self.answer_chain.invoke({"question": question})

        except Exception as e:
            print(e)
            return "Sorry, I could not answer your question"

    def generate_query(self, question):
        pass
