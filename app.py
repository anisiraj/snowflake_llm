import random
import gradio as gr
from snowflake_llm.engine import QueryChatEngine
from snowflake_llm.helpers import (get_meta_store, 
                                   build_metadata_rag_query_engine)
import sys
import os



# set up data base

metastore = get_meta_store()
chat_agent = build_metadata_rag_query_engine(metastore=metastore)


def respond(query, history):    
    try:
        res = chat_agent.answer(query)
        return res
    except Exception as e:
        print(e)
        return f"Sorry, I had error executing your query {e}."


def simple_auth_function(username, password):
    return username == "admin" and password == os.environ.get(
        "LLM_SNOWFLAKE_PASSWORD"
    )


if __name__ == "__main__":
    server_name = "0.0.0.0"

    if len(sys.argv) > 1:
        print("running with command line arguments")
        runtype = sys.argv[1]
        if runtype == "local":
            server_name = "127.0.0.1"

    print("starting app as {server_name}".format(server_name=server_name))
    gr.ChatInterface(respond,
                     title="Snowfox",
                     description="Snowfox is a chatbot that uses language models to answer questions about a Snowflake database.",
                     examples=[["How many entrie are in catalog page"]],
                     ).launch(
        server_name=server_name, auth=simple_auth_function)
