from snowflake_llm.helpers import build_metdata_rag_query_engine

if __name__ == '__main__':
    engine = build_metdata_rag_query_engine()
    print(engine.generate_query("How many tables are in the database?"))
    print(engine.answer("How many tables are in the database?"))
