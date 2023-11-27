# ChatbotPersonalizavel
Projeto de um chatbot usando API da OpenAI implementada com LangChain e Streamlit.
## Como utilizar:
  Tenha Python, Langchain e Streamlit instalados localmente.
  
  Abrir terminal no caminho que estejam os arquivos do projeto
  
  Utilizar "streamlit run stApp.py" no terminal.
  
  Precisa de Chave de API da OpenAI, colocada manualmente na barra lateral do programa, ou via variavel de ambiente (OPENAI_API_KEY).

# Features implementadas:

## Nomes constantes:
  Caso preenchido os campos "Nome da IA" e "Nome do usuário", estes valores serão conhecimento constante da IA para caso necessário.
  
## Escolher nível de Entendimento do usuário:
- Nenhum: IA vai tratar como se o usuário não tivesse nenhum conhecimento prévio em qualquer assunto técnico

- Básico: IA vai partir do pressuposto que o usuário tem intendimento prévio do assunto, em nivel casual

- Expert: IA vai usar termos quaisquer técnicos que achar necessário para explicações

## Agentes:

  Utiliza sistema de Agentes capaz de tomar decisões e selecionar entre sua lista de possíveis ações, assim dividindo o problema em partes
  
  **Ferramentas:**
  
- Matemática: Capaz de solucionar operações algébricas e fazer cálculos caso for necessário
    
- Wikipedia: Capaz de pesquisar sobre pessoas, coisas, lugares na Wikipedia
    
- Pesquisa: Capaz de pesquisar na internet sobre quaisquer tópicos que julgar necessário (usando DuckDuckGO)

- Random: Capaz de simular aleatoridade

## AI Roles:
  Similarmente aos nomes, caso seja preenchido, a IA agirá como especificado neste campo. Usando quaisquer maneirimos e atuando como desejado.
  Como agentes impedem a IA de agir de qualquer maneira específica, enquanto a opção de Agentes estiver ligado, essas especificações serão aplicadas após o resultado final dos Agentes.
  Portanto, gastará mais tempo e será menos efetiva que a geração do texto sem agentes.
