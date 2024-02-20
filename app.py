import random
import gradio as gr
from snowflake_llm.agent import get_query_chain


def respond(query, history):
    chain, query_writer_chain = get_query_chain()
    try:
        res = chain.invoke({"question": query})
        return res
    except Exception as e:
        print(e)
        return f"Sorry, I had error executing your query {e}."
    



if __name__ == "__main__": 
    print("starting app") 
    gr.ChatInterface(respond).launch()