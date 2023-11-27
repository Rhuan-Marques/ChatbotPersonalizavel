# ChatbotPersonalizavel
Projeto de um chatbot usando API da OpenAI implementada com LangChain e Streamlit.
## Como utilizar:
  Tenha Python, Langchain e Streamlit instalados localmente.
  
  Abrir terminal no caminho que estejam os arquivos de codigo do projeto (Por padrão, ./source)
  
  Utilizar "streamlit run stApp.py" no terminal.
  
  Precisa de Chave de API da OpenAI, colocada manualmente na barra lateral do programa, ou via variavel de ambiente (OPENAI_API_KEY).

  Após isso, só conversar!
  
  *Nota: O chatbot é capaz de se comunicar em qualquer língua, porém, algumas funções do Chatbot funcionarão melhor com conversas em inglês, sendo esta a linguagem usada internamente e a linguagem com mais conteudo disponível on-line.

# Features implementadas:

## Nomes constantes:
  Caso preenchido os campos "Nome da IA" e "Nome do usuário", estes valores serão conhecimento constante da IA para caso necessário.
  
## Escolher nível de Entendimento do usuário:
- Nenhum: IA vai tratar como se o usuário não tivesse nenhum conhecimento prévio em qualquer assunto técnico

- Básico: IA vai partir do pressuposto que o usuário tem intendimento prévio do assunto, em nivel casual

- Expert: IA vai usar termos quaisquer técnicos que achar necessário para explicações

## Agentes:

  Utiliza sistema de Agentes capaz de tomar decisões e selecionar entre sua lista de possíveis ações, assim dividindo o problema em partes
  
  **Ferramentas (Agente geral):**
  
- Matemática: Capaz de solucionar operações algébricas e fazer cálculos caso for necessário
    
- Wikipedia: Capaz de pesquisar sobre pessoas, coisas, lugares na Wikipedia
    
- Pesquisa: Capaz de pesquisar na internet sobre quaisquer tópicos que julgar necessário (usando DuckDuckGO)

- Random: Capaz de simular aleatoridade
    - Por exemplo: "Aleatorize um numero entre 1 e 25", "Simule uma chançe de 50% de uma moeda cair cara ou coroa e me diga o resultado", etc

**Ferramentas (Agente de Finanças):**

Utiliza da AlphaVantage API para receber informações atualizadas do mercado financeiro para ajudar o usuário a tomar decisões

  *Nota: Esta feature está em estado experimental
  
  - Notícias por Tópico: Pesquisa as notícias mais recentes sobre determinado tópico e dá informações sobre se é um bom investimento
    - Por exemplo: "Como está o mercado de Blockchain no momento, vale a pena investir?"

  - Notícias por Ticker: Pesquisa as notícias mais recentes sobre um ou mais Tickers e dá informações sobre seu valor atual
    - Por exemplo: "Como está o valor do Yen Japonês?"

## AI Roles:
  Similarmente aos nomes, caso seja preenchido, a IA agirá como especificado neste campo. Usando quaisquer maneirimos e atuando como desejado.
  Como agentes impedem a IA de agir de qualquer maneira específica, enquanto a opção de Agentes estiver ligado, essas especificações serão aplicadas após o resultado final dos Agentes.
  Portanto, gastará mais tempo e será menos efetiva que a geração do texto sem agentes.

## Salvar e Carregar Estado:

Te permite fácilmente salvar seu seteup(nomes, chaves de API, AI roles, etc) em um .json de facil acesso, para carregá-los de volta quando quiser.

Também é possível baixar sua conversa em um arquivo de texto legível.
