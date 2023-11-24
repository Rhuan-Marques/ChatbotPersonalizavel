"""
This file is for the main AI components
It keeps any important variables for the AI as well as the chatbot itself.
It uses the data to manage the AI prompts accordingly to any modification made in front-end.
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

class IA:
    """Manages an instance of an OpenAPI Chatbot
    :var chatModel: The Chat iself, must be initialized by passing API key through constructor
    :var name: How the Chatbot will address itself
    :var user_name: How the Chatbot will address the user
    :var role: The role the chatbot will be playing as. "" = for generic AI chatbot
    :var user_knowledge: How much the user knows about the topic at hand
    (0 = No experience; 1 = Basic understanding; 2 = Expert!)
    :var convHistory: List of the last messages and senders.
    :var historyLenght: Current lenght of the message history
    :var HISTORY_MAX_SIZE: Max size the history should get
    :var agentToggle: Will agents be used
    """
    def __init__(self, key, name = "SuppaChat", role = "", user_name = "",knowledge=0, agentToggle=False):
        """
        :param key: API Key
        :param name: Name of the Chatbot
        :param role: Role it will be playing as
        :param user_name: How to address user
        :param knowledge: User understand of topic at hand
        :param agentToggle: Should it use agents
        :raise KeyNotFound: Given key is blank
        :raise APIConnectionError: Cant connect to API
        """
        if not key:
            raise KeyNotFound
        try:
            print("Testando conexao com a API")
            self.chatModel = ChatOpenAI(openai_api_key=key)
            self.chatModel.invoke("") # Checks if the key is valid
            print("Conexao estabelecida")
        except Exception as e:
            print(f"Exception {e}")
            raise APIConectionError
        # Sets initial values to the object
        self.update(name, role, user_name, knowledge, agentToggle)
        self.convHistory = None
        self.historyLenght=0
        self.HISTORY_MAX_SIZE = 500

    def update(self, name="SuppaChat", role = "", user_name = "",knowledge=0, agentToggle=False):
        """
        Updates the variables of the AI
        :param name: Name of the Chatbot
        :param role: Role it will be playing as
        :param user_name: How to address user
        :param knowledge: User understanding of topic at hand
        :param agentToggle: Should it use agents
        """
        self.name = name
        self.role = role
        self.user_name = user_name
        self.user_knowledge = knowledge
        self.agentToggle = agentToggle


    def getTemplate(self):
        """
        Returns the correct System Template for how the AI should act based on the variables:
        :var:
        - name
        - user_name
        - role
        - user_knowledge
        """
        template = ""
        # Checks if it has a role, if not, defaults to basic AI Chatbot
        if self.role:
            template = template + "You are a {role}"
        else:
            template = template + "You are an AI chatbot"

        # Adds its name in (if it exists)
        if self.name:
            template = template + " named {name}"
        # Checks if it has a defined user_name, if not, specifies that it shouldn't know
        if self.user_name:
            template = template+ "\nYou are talking to someone named {user_name}"
        else:
            template = template+ "\nYou don't know the name of whoever you are talking to"

        # Specifies how the AI should treat the users knowledge of the subject
        # Will use necessary technical terms if the user is an expert but not if it is a novice
        if self.user_knowledge == 0:
            template= template+ """\nYou are talking to a user without any technical knowldge.
                Be sure to use simple terms anyone can understand"""
        elif self.user_knowledge == 1:
            template = template + """\nYou are talking to a user with basic technical knowldgebe.
                Talk as you would with someone who isn't from the field in question, don't use too complicated or uncommon terms"""
        elif self.user_knowledge == 2:
            template = template + """\nYou are talking to an expert user.
            Use any technical terms necessary to explain what you need in a professional manner"""
        return template

    def addInteraction(self, sender, text:str):
        """
        Adds given message to the conversation History\n
        If the memory is too high, will remove older messages
        :param sender: The sender of the message ("ai", "user"...)
        :param text: Content of the message
        """
        # Adds to convHistory
        if not self.convHistory:
            self.convHistory = [(sender, text)]
        else:
            self.convHistory.append((sender, text))

        # Removes older messages from memory until the size is below the limit or there's only 1 message
        self.historyLenght += len(text)
        while self.historyLenght > self.HISTORY_MAX_SIZE and len(self.convHistory) > 1:
            msg = self.convHistory.pop(0)
            self.historyLenght -= len(msg[1])

    def transcribe(self, prompt):
        """
        Transcribe received text for something that matches AIs current variables
        :param prompt: What should the AI re-write
        :return: Prompt transcribed to match the current state of the AI
        """
        template = [("system", self.getTemplate())]
        template += [("system", "Now, re-write the following text considering you're role and limitations:")]
        template += [("ai", prompt)]
        chat_prompt = ChatPromptTemplate.from_messages(template)
        messages = chat_prompt.format_messages(role=self.role, name=self.name, user_name=self.user_name)
        response = self.chatModel.invoke(messages).content
        return response

    def getResponse(self, prompt):
        """
        Manages how the AI should respond to questions
        :param prompt: The prompt the to respond
        :return: AIs response about the prompt at hand
        """
        self.addInteraction("human", prompt) # Add to memory

        # Creates a full template using the System Template and the messages in memory
        fullTemplate = [("system", self.getTemplate())] + self.convHistory
        chat_prompt = ChatPromptTemplate.from_messages(fullTemplate)
        messages = chat_prompt.format_messages(role=self.role, name=self.name, user_name=self.user_name)

        # Defines if it will use normal responses or call agent(s)
        if not self.agentToggle:
            response = self.chatModel.invoke(messages).content
        else:
            from agent import runAgent
            print("-- Agent Initialized --")
            response = runAgent(self.chatModel, messages)
            """
            Agents won't follow the roles for their thought
            To get a similar effect, we re-write their final response to match
            the current role
            """
            if self.role:
                response = self.transcribe(response)

        # Adds response to the memory and returns it
        print(response)
        self.addInteraction("ai", response)
        return response


class APIConectionError(Exception):
    "Raised when cant connect to API"
    pass

class KeyNotFound(Exception):
    "Raised when cant find key"
    pass

