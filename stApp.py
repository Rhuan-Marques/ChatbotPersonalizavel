"""
This file is for the streamlit front-end of the project.
It draws elements on screen and keeps the human input
"""
import os
import streamlit as st
from baseAI import AI
from baseAI import KeyNotFound, APIConectionError

# Seta nome da página
st.set_page_config(page_title="Chatbot")

# Setting up the AI and message-list on session state
if "ai" not in st.session_state:
    st.session_state["ai"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "text": "Ola, como posso ajudar"}]

def getKnowLvl(know):
    """
    :param know: Knowledge as text ("Nenhum", "Basico", "Expert")
    :return: Knowldge Level as number: 0, 1, 2
    """
    if know == "Basico":
        return 1
    elif know == "Expert":
        return 2
    else:
        return 0

def checkForEnvVar(key):
    """
    If the key provided is empty, checks for a key in the enviorement variables
    :param key: An API Key, possibly empty
    :return: The key provided or found, None if it doesn't find any keys
    """
    if not key:
        try:
            API_KEY = os.environ['OPENAI_API_KEY']
        except:
            API_KEY = None
    else:
        API_KEY = key
    return API_KEY


with st.sidebar:
    # Create input bar for API Key
    # After the first message, it connects to the API for the rest of the chat and this camp is disabled
    key = st.text_input("Chave API", "", type="password", disabled=st.session_state.ai != None)
    st.caption("Caso nenhuma chave seja provida, iremos buscar nas variaveis de ambiente")
    key = checkForEnvVar(key)

    # Gets true KnowledgeLvl (as integer) from the selectable text box
    knowLvl = getKnowLvl(st.selectbox("Seu nivel de entendimento sobre o assunto em questão:",
                                               ("Nenhum", "Basico", "Expert")))

    with st.expander("Opcoes avancadas:"):
        # Toggle to activate/desactivate Langchain agents
        agentToggle = st.toggle("Agentes")
        st.caption("Quando ativado, permite a IA a pesquisar na internet, fazer calculos matematicos, e mais. Porém, deixa o sistema mais devagar")

        # Toggle and text bar for IA roles.
        # If activated, the IA should act as whatever is writter in this area
        roleToggle = st.toggle("IA Roles")
        role=""
        if roleToggle:
            role = st.text_area("Papel da IA", disabled=not roleToggle)
            st.caption("A IA atuará como descrito aqui. Quando ativado juntamente com Agentes, é menos consistente e aumenta o tempo de resposta")

        # Names for how the AI should address itself and its user
        name = st.text_input("Nome da IA", "SuppaChat")
        username = st.text_input("Nome do Usuario")

    # Button that ressets completely the conversation and AI, allowing you to change API Keys
    # This will wipe it's memory of the old conversation too
    if(st.button("Reset", type="primary")):
        st.session_state.clear()
        st.rerun()


st.title(':space_invader: Chatbot AI :rainbow[Personalizavel] :space_invader:')

# Writes the whole conversation back from memory
# Users messages are colored blue
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        coloredMsg = ":blue[" + msg["text"] + "]"
    else:
        coloredMsg = msg["text"]
    st.chat_message(msg["role"]).write(coloredMsg)

if input := st.chat_input():
    # Add user message to the visual screen
    st.session_state.messages.append({"role": "user", "text": input})
    st.chat_message("user").write(input)
    response= ""
    # If there isn't an connected AI, tries to connect to it
    # Connection errors or Key errors will be passed to user as messages on the chat
    if st.session_state.ai == None:
        try:
            st.session_state.ai = AI(name=name, role=role, user_name=username, knowledge=knowLvl, key=key, agent_toggle=agentToggle)
        except KeyNotFound:
            response = "Chave nao reconhecida na barra lateral nem nas variáveis de ambiente"
        except APIConectionError:
            response = "Erro de autentificação OpenAI, certifique-se de que a chave está correta"
    else:
        # If there is a connected AI, updates values the user could have changed between messages
        st.session_state.ai.update(name, role, username, knowLvl, agentToggle)
    if not response:
        # If no other response was forced as output (like errors) it calls the AI to respond
        response = st.session_state.ai.getResponse(input)
    # Adds response message to the screen
    st.session_state.messages.append({"role": "assistant", "text": response})
    st.chat_message("assistant").write(response)

def getKey():
        """
        Gets key from textbox
        :return: The key found, None if it doesn't find any keys
        """
        return key
