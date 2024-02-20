import random
import gradio as gr
from snowflake_llm.agent import get_query_chain
import sys
import os


def respond(query, history):
    chain, query_writer_chain = get_query_chain()
    try:
        res = chain.invoke({"question": query})
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
    gr.ChatInterface(respond).launch(
        server_name=server_name, auth=simple_auth_function)
