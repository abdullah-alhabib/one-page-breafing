import streamlit as st
import langchain 
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI


def initializer():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    if "chatbot_api_key" not in st.session_state:
        st.session_state["chatbot_api_key"] = ""
                
    return True


def main():
    st.title("💬 Bohakoom Chatbot") 
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt:=st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        else :
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            output = Conversation.run(input=prompt)
            st.session_state.messages.append({"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)

if __name__ == '__main__':
    st.set_page_config(page_title="Chatbot",layout="centered")
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    session_initilizer= initializer()
    if st.session_state["chatbot_api_key"]!="":
        model = 'gpt-3.5-turbo'
        llmObj = ChatOpenAI(openai_api_key=st.session_state["chatbot_api_key"],
            model_name=model)
        k= 5
        if 'entity_memory' not in st.session_state:
                    st.session_state.entity_memory = ConversationEntityMemory(
                        llm=llmObj, k=k)
        Conversation = ConversationChain(
                    llm=llmObj,
                    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                    memory=st.session_state.entity_memory
                )
        main()
    else:
        st.title("Please provide API key to run the chatbot")
