"""
This file is for the streamlit front-end of the project.
It draws elements on screen and keeps the human input
"""

import os
import streamlit as st


# Seta nome da página
st.set_page_config(page_title="Chatbot")

# Setting up the AI as permanent element
if "ai" not in st.session_state:
    st.session_state["ai"] = None
# Setting up the (visual) Message History as permanent element
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "text": "Hello, how can i help you"}]
# Setting up keys dictionary to pass to the AI
if "keys" not in st.session_state:
    st.session_state["keys"] = {}
# Stores the current values of fill-able camps so that you can save/load states easily
if "camps" not in st.session_state:
    st.session_state["camps"] = {}
# # Stores the loading messages like "Connecting to API"
# if "loading" not in st.session_state:
#     st.session_state["loading"] = ""

def getKnowLvl(know):
    """
    Translates KnowledgeLvl options (str) to their int counterparts
    :param know: Knowledge as text ("Nenhum", "Basico", "Expert")
    :return: Knowledge Level as number: 0, 1, 2
    """
    if know == "Basico":
        return 1
    elif know == "Expert":
        return 2
    else:
        return 0

def getHistoryStr():
    """Returns the message history as human-readable String instead of messy dictionary"""
    history = ""
    for msg in st.session_state["messages"]:
        history+= msg["role"] + ": " + msg["text"] + "\n\n"
    return history

def checkForEnvVar(key: str, envar_pos: str):
    """
    If the key provided is empty, checks for a key in the environment variables
    :param key: An API Key, possibly empty
    :param envar_pos: Where to check in the EnvVariables (String)
    :return: The key provided or found, None if it doesn't find any keys
    """
    if key:
        return key
    else:
        try:
            API_KEY = os.environ[envar_pos]
        except:
            return None
        else:
            return API_KEY

# ----------------------------------------- SIDE BAR ---------------------------------------------------------------
with st.sidebar:
    def getValue(textCamp):
        """
        Checks for campValues on st.session_state["camps"]
        Enables Saving/Loading States
        :param textCamp: The text camp name
        :return: Whatever is in memory for that camp, Empty str if nothing
        """
        if textCamp not in st.session_state["camps"]:
            return None
        else:
            return st.session_state["camps"][textCamp]


    connected = (st.session_state["ai"] != None)
    # Stores if you already connected to the AI connection
    # Used to disable fill-able camps for API Keys

    # Create input bar for OpenAI API Key
    # After the first message, it connects to the API for the rest of the chat and this camp is disabled
    st.session_state["camps"]["OpenAI"] = st.text_input(label="Chave API",
                                                        value=getValue("OpenAI"),
                                                        type="password",
                                                        disabled=connected)
    st.caption("Caso nenhuma chave seja provida, iremos buscar nas variaveis de ambiente")
    # Checks for environmental variables of the OpenAI API KEY
    st.session_state["keys"]["OPENAI_API_KEY"] = checkForEnvVar(key=getValue("OpenAI"),
                                                                envar_pos="OPENAI_API_KEY")

    # Gets KnowledgeLvl (as integer) from the selectable text box
    knowledge_str = st.selectbox(label="Seu nivel de entendimento sobre o assunto em questão:",
                                 options=["Nenhum", "Basico", "Expert"],
                                 index=getValue("know_lvl"))
    st.session_state["camps"]["know_lvl"] = getKnowLvl(knowledge_str)

    with st.expander("Opcoes avancadas:"):
        # Toggle to activate/desactivate Langchain agents
        st.session_state["camps"]["agent_toggle"] = st.toggle(label="Agentes",
                                                              value=getValue("agent_toggle"))
        st.caption("Quando ativado, permite a IA a pesquisar na internet, fazer calculos matematicos, e mais. Porém, deixa o sistema mais devagar")

        # Toggle and text bar for AI roles.
        # If activated, the AI should act as whatever is written in this area
        st.session_state["camps"]["roleToggle"] = st.toggle(label="IA Roles",
                                                            value=getValue("roleToggle"))
        if getValue("roleToggle"):
            st.session_state["camps"]["role"] = st.text_area(label="Papel da IA",
                                                             disabled=not st.session_state["camps"]["roleToggle"],
                                                             value=getValue("role"))
            st.caption("A IA atuará como descrito aqui. Quando ativado juntamente com Agentes, é menos consistente e aumenta o tempo de resposta")
        else:
            st.session_state["camps"]["role"] = ""
        # Names for how the AI should address itself and its user
        st.session_state["camps"]["name"] = st.text_input(label="Nome da IA",
                                                          value=getValue("name"))
        st.session_state["camps"]["username"] = st.text_input(label="Nome do Usuario",
                                                              value=getValue("username"))

    with st.expander("Outras chaves de API:"):
        st.caption("Alguns recursos precisarão de chaves de API extras."
        "Preencha os campos antes de sua primeira interação com a AI caso deseje usá-los")
        # Key for finance news API AlphaVantage.
        # If empty, won't use this agent
        st.session_state["camps"]["AlphaVantage"] = st.text_input(
            label="Alpha Vantage API Key",
            type="password",
            value=getValue("AlphaVantage"),
            disabled=connected)
        st.session_state["keys"]["ALPHAVANTAGE_API_KEY"] = getValue("AlphaVantage")
        st.caption("Usefull integration for finance news/predictions. Get for free at: https://www.alphavantage.co/support/#api-key")

    # creates colums for different buttons
    col1, col2 = st.columns(2)
    import json
    with col1:
        # Save State button saves json file of the "camps" dictionary
        state_data = json.dumps(st.session_state["camps"])
        st.download_button(label="Salvar estado", data=state_data, file_name="chatbotState.json",)
    with col2:
        # Switch "LoadStateMode" which shows-up the file uploader
        # Must be a session_state so that it doesn't reset before loading
        if st.button("Carregar estado"):
            if not getValue("LoadStateMode"):
                st.session_state["camps"]["LoadStateMode"] = True
            else:
                st.session_state["camps"]["LoadStateMode"] = False
    st.caption("Carrega e salva estado atual das variaveis preenchidas. (Nomes, APIs, etc)")
    # Creates the FileUploader, checks for file, and possibly loads file content
    if getValue("LoadStateMode"):
        uploaded_file = st.file_uploader("Escolha arquivo de template", type="json")
        if uploaded_file is not None:
            json_file = json.load(uploaded_file)
            st.session_state["camps"] = dict(json_file)
            # Resets AI to deal with API Key changes
            st.session_state["ai"] = None
            # Reruns to apply changes
            st.session_state["camps"]["LoadStateMode"] = False
            st.rerun()

    col1, col2 = st.columns(2)
    # Save Conversation button to save messageHistory
    with col1:
        conversation_data = getHistoryStr()
        st.download_button("Salvar Conversa", data= conversation_data, file_name="messageHistory.txt")

    # Reset button logic
    with col2:
        if st.button("Reset", type="primary"):
            del st.session_state["messages"]
            del st.session_state["ai"]
            st.rerun()


# ----------------------------------------- CHAT VISUALS ---------------------------------------------------------------
st.title(':computer: Chatbot AI :blue[Personalizavel] :computer:')

# Writes the whole conversation back from memory
# Users messages are colored blue
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        coloredMsg = ":blue[" + msg["text"] + "]"
    else:
        coloredMsg = msg["text"]
    st.chat_message(msg["role"]).write(coloredMsg)


#
# if st.session_state["loading"]:
#     st.write(st.session_state["loading"] + "...")
#     st.session_state["loading"] = ""
#
# def loading(loading_msg: str):
#     """
#     Other files can call this function to add a "loading" message to the screen
#     :param loading_msg: The message to be added
#     """
#     st.session_state["loading"]= loading_msg
#     st.rerun()

# ------------------------------------------ CHAT INPUT -------------------------------------------------------------
if input := st.chat_input():
    from baseAI import AI
    # Add user message to the visual screen
    st.session_state.messages.append({"role": "user", "text": input})
    st.chat_message("user").write(input)
    response= ""
    # If there isn't an connected AI, tries to connect to it
    # Connection errors or Key errors will be passed to user as messages on the chat
    if st.session_state.ai == None:
        from baseAI import KeyNotFound, APIConectionError
        try:
            st.session_state.ai = AI(keys=st.session_state["keys"],
                                     name=getValue("name"),
                                     role=getValue("role"),
                                     user_name=getValue("username"),
                                     knowledge=getValue("know_lvl"),
                                     agent_toggle=getValue("agent_toggle"))
        except KeyNotFound:
            response = "Chave nao reconhecida na barra lateral nem nas variáveis de ambiente"
        except APIConectionError:
            response = "Erro de autentificação OpenAI, certifique-se de que a chave está correta"
    else:

        # If there is a connected AI, updates values the user could have changed between messages
        st.session_state.ai.update(name=getValue("name"),
                                   role=getValue("role"),
                                   user_name=getValue("username"),
                                   knowledge=getValue("know_lvl"),
                                   agent_toggle=getValue("agent_toggle"))
    if not response:
        # If no other response was forced as output (like errors) it calls the AI to respond
        response = st.session_state.ai.getResponse(input)
    # Adds response message to the screen
    st.session_state.messages.append({"role": "assistant", "text": response})
    st.chat_message("assistant").write(response)

