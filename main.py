import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI


def initializer():
    if "generated" not in st.session_state:
        # To store the model outputs
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        # To store the user inputs
        st.session_state["past"] = []
    if "input" not in st.session_state:
        # To store the current user input
        st.session_state["input"] = ""
    if "api_key" not in st.session_state:
        st.session_state["api_key"]= "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"
    return True


def main():
    st.title("Prototype ChatBot🤖")
    model = 'gpt-3.5-turbo'
    llmObj = ChatOpenAI(openai_api_key=st.session_state["api_key"],
    model_name=model)

    k= 5
    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(
                llm=llmObj, k=k)
            
            # The ConversationChain object
    Conversation = ConversationChain(
            llm=llmObj,
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory
        )
    user_input = st.text_input("You: ", st.session_state["input"],key="input",
    placeholder="Your Chatbot friend! Ask away ...",label_visibility='hidden')

    if user_input:
        output = Conversation.run(input=user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")

if __name__ == '__main__':
    st.set_page_config(page_title="Chatbot",layout="centered")
    session_initilizer= initializer()

    if session_initilizer:
        main()