from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain import hub
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import Runnable
from dotenv import load_dotenv
from langchain_core.runnables import RunnableWithMessageHistory

import os
from retriever import get_retriever


checkpointer = SqliteSaver.from_conn_string("chat_memory.db")

#Session store 
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def create_qa_chain() -> Runnable:

    load_dotenv()
    # Initializing chatmodel

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,  # Add some creativity while staying factual
            
        )
    except Exception as e:
        raise Exception(f"Failed to initialize LLM: {e}")

    collection_name:str = os.getenv("COLLECTION_NAME", "")
    if not collection_name:
        raise ValueError("COLLECTION_NAME environment variable is required")

    # initializing retriever with more context
    retriever = get_retriever(collection_name=collection_name, k=8)  # Increased from 5 to 8

    ## Chat history aware prompt
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(
                                llm, retriever, rephrase_prompt
                                )
    qa_prompt = ChatPromptTemplate.from_template("""
    You are an expert at analyzing YouTube video content. Your job is to help users understand what they've watched.

    Use the provided context from the video transcript to answer questions. Be comprehensive and helpful. 
    If the context contains relevant information, use it to provide a thorough answer.
    If information is missing, acknowledge what you don't know but provide what you can from the context.

    Context: {context}

    Question: {input}

    Provide a helpful, comprehensive answer based on the video content:""")

    combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)

    retrieval_chain = create_retrieval_chain(
                        history_aware_retriever,
                        combine_docs_chain,
                        )
    
    chain_with_memory = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    
    return chain_with_memory

def main():
    chain = create_qa_chain()
    session_id = "default_session"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"Assistant: {response['answer']}")

if __name__ == "__main__":
    main()
