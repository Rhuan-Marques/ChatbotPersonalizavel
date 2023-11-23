import os
import streamlit as st
from lang import IA

st.set_page_config(page_title="Chatbot")

def keyValidation(key):
    if not key:
        try:
            API_KEY = os.environ['OPEN_API_KEY']
        except:
            API_KEY = None
    else:
        API_KEY = key
    return API_KEY

if "ai" not in st.session_state:
    st.session_state["ai"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "text": "Ola, como posso ajudar"}]

def getKnowLvl(know):
    if know == "Basico":
        return 1
    elif know == "Expert":
        return 2
    else:
        return 0

with st.sidebar:
    key = st.text_input("Chave API", "", type="password", disabled=st.session_state.ai != None)
    st.caption("Caso nenhuma chave seja provida, iremos buscar nas variaveis de ambiente")
    key = keyValidation(key)

    knowLvl = getKnowLvl(st.selectbox("Seu nivel de entendimento sobre o assunto em questão:",
                                               ("Nenhum", "Basico", "Expert")))

    with st.expander("Opcoes avancadas:"):
        #st.caption("As seguintes características devem ser definidas *antes* de sua primeira mensagem nesse chat")
        agentToggle = st.toggle("Agentes")
        st.caption("Quando ativado, permite a IA a pesquisar na internet, fazer calculos matematicos, e mais. Porém, deixa o sistema mais devagar")
        roleToggle = st.toggle("IA Roleplay")
        role = st.text_area("Papel da IA", disabled=not roleToggle)
        st.caption("A IA atuará como descrito aqui. Quando ativado juntamente com Agentes, é menos consistente e aumenta o tempo de resposta")
        name = st.text_input("Nome da IA", "SuppaChat")
        username = st.text_input("Nome do Usuario")
    if(st.button("Reset", type="primary")):
        st.session_state.clear()
        st.rerun()


st.title(':space_invader: Chatbot AI :rainbow[Personalizavel] :space_invader:')

for msg in st.session_state["messages"]:

    if msg["role"] == "user":
        coloredMsg = ":blue[" + msg["text"] + "]"
    else:
        coloredMsg = msg["text"]
    st.chat_message(msg["role"]).write(coloredMsg)

if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "text": input})
    st.chat_message("user").write(input)
    if not key:
        response = "Chave da API com erro, certifique de que está correta"
    else:
        if st.session_state.ai == None:
            st.session_state.ai = IA(name=name, role=role, user_name=username, knowledge=knowLvl, key=key)
        #st.text("iaCreated feito!!!, agora eh true")
        st.session_state.ai.name = name
        st.session_state.ai.user_name = username
        st.session_state.ai.user_knowledge = knowLvl
        st.session_state.ai.agentToggle = agentToggle
        st.session_state.ai.roleToggle = roleToggle
        st.session_state.ai.role = role
        #try:
        response = st.session_state.ai.getResponse(input)
        #except:
        #response = "Erro de conexão com a API, tente novamente mais tarde"
    st.session_state.messages.append({"role": "assistant", "text": response})
    st.chat_message("assistant").write(response)
    st.rerun()
