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
            temperature=0.1,  # Lower temperature to reduce hallucinations
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
    You are a precise assistant that answers questions about YouTube video content. Your responses must be based ONLY on the provided context from the video transcript.

    CRITICAL RULES:
    1. ONLY use information that is explicitly stated in the provided context
    2. If the context doesn't contain enough information to answer the question, say "Based on the provided context, I cannot answer this question completely" and only provide what you can from the context
    3. Do NOT make assumptions or add information not present in the context
    4. When referencing information, include the timestamp references from the metadata
    5. Be specific and factual, avoid generalizations
    6. Do not make up information or hallucinate
    7. Answer to Greetings messages politely.
    
    Context: {context}

    Question: {input}

    Answer based ONLY on the provided context:""")

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

def debug_retrieval(query: str, collection_name: str):
    """Debug function to see what documents are being retrieved"""
    retriever = get_retriever(collection_name=collection_name, k=8)
    docs = retriever.get_relevant_documents(query)
    
    print(f"\n=== DEBUG: Retrieved {len(docs)} documents for query: '{query}' ===\n")
    for i, doc in enumerate(docs):
        print(f"Document {i+1}:")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")
        print("-" * 50)

def main():
    chain = create_qa_chain()
    session_id = "default_session"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        if user_input.lower() == 'debug':
            # Debug mode - show what's being retrieved
            debug_query = input("Enter query to debug: ")
            collection_name = os.getenv("COLLECTION_NAME", "video_chunks")
            debug_retrieval(debug_query, collection_name)
            continue
            
        response = chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"Assistant: {response['answer']}")

if __name__ == "__main__":
    main()
