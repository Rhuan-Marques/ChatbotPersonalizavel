# ChatbotPersonalizavel
Projeto de um simples chatbot usando API da OpenAI implementada com LangChain e Streamlit

Por enquanto, requer Streamlit local para rodar: "streamlit run app.py" no terminal
Precisa de Chave de API da OpenAI, ou via variavel de ambiente (OPENAI_API_KEY) ou colocada manualmente.

# Features implementadas por enquanto:
Nivel de Entendimento:
- Nenhum: IA vai tratar como se o usuário não tivesse nenhum conhecimento prévio em qualquer assunto técnico

- Basico: IA vai partir do pressuposto que o usuário tem intendimento prévio do assunto, em nivel casual

- Expert: IA vai usar termos quaisquer técnicos que achar necessário para explicações

Nomes constantes:
  Caso preenchido os campos "Nome da IA" e "Nome do usuário", estes valores serão conhecimento constante da LLM para caso necessário.

IA Roleplay:
  Similarmente aos nomes, caso seja preenchido, a IA agirá como expecificado neste campo. Usando quaisquer maneirimos e atuando personagens que desejado.
  Como agentes impedem a IA de agit de qualquer maneira expecifica, enquanto a opção de Agentes estiver ligado, essas expecificações serão aplicadas após o resultado final dos Agentes.
  Portanto, gastará mais tempo e será menos efetiva que a geração do texto já com este campo em mente.

Agentes:

  Utiliza sistema de Agentes capaz de tomar decisões e selecionar entre sua lista de possíveis ações, assim dividindo o problema em partes aceitáveis
  Ferramentas
  
- Matematica: Capaz de solucionar operações algébricas e fazer calculos caso for necessário
    
- Wikipedia: Capaz de pesquisar sobre pessoas, coisas, lugares na Wikipedia
    
- Pesquisa: Capaz de pesquisar na internet sobre quaisquer tópicos que julgar necessário (usando DuckDuckGO)

- Random: Capaz de gerar números aleatórios
