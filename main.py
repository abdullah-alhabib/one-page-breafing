import streamlit as st
import langchain 
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
        st.session_state["api_key"]= ""
    return True


def main():
    st.title("Bohakooom GPT")
    model = 'gpt-3.5-turbo'
    api_key = st.text_input(label="API Key",key="api_key", placeholder="Enter Your API key ",label_visibility='hidden', type="password")
   
    if api_key:
        llmObj = ChatOpenAI(openai_api_key=st.session_state["api_key"],
        model_name=model)
        st.write("llmObj has been created")
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
        st.write("conversation has been created")

        st.header("Ask anything..")
        user_input = st.text_input("You: ", st.session_state["input"],key="input",
        placeholder="Your Chatbot friend! Ask away ...",label_visibility='hidden')
        st.header(user_input)
        if user_input:
            st.header("Running...")
            output = Conversation.run(input=user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

        with st.expander("Conversation", expanded=True):
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                st.info(st.session_state["past"][i], icon="🧐")
                st.success(st.session_state["generated"][i], icon="🤖")
    else :
        st.write("Bro you have to provide api key!")

if __name__ == '__main__':
    st.set_page_config(page_title="Chatbot",layout="centered")
    session_initilizer= initializer()

    if session_initilizer:
        main()