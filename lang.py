from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from agent import conversationAgent

class IA:

    def __init__(self, key, name = "SuppaChat", role = "", user_name = "",knowledge=0, convHistory = None):
        self.chatModel = ChatOpenAI(openai_api_key=key)
        self.name = name
        self.role = role
        self.user_name = user_name
        self.user_knowledge = knowledge
        self.convHistory = convHistory
        self.historyLenght = 0
        self.HISTORY_MAX_SIZE = 500
        self.agentToggle=False
        self.roleToggle=False

    def getTemplate(self):
        template = ""
        if self.role and self.roleToggle:
            template = template + "You are a {role}"
        else:
            template = template + "You are an AI chatbot"
        template = template + " named {name}"
        if self.user_name:
            template = template+ "\nYou are talking to someone named {user_name}"
        else:
            template = template+ "\nYou don't know the name of whoever you are talking to"
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
        if not self.convHistory:
            self.convHistory = [(sender, text)]
        else:
            self.convHistory.append((sender, text))

        self.historyLenght += len(text)
        while self.historyLenght > self.HISTORY_MAX_SIZE and len(self.convHistory) > 1:
            msg = self.convHistory.pop(0)
            self.historyLenght -= len(msg[1])

        return

    def getResponse(self, prompt):
        self.addInteraction("human", prompt)
        fullTemplate = [("system", self.getTemplate())] + self.convHistory
        chat_prompt = ChatPromptTemplate.from_messages(fullTemplate)
        messages = chat_prompt.format_messages(role=self.role, name=self.name, user_name=self.user_name)
        if not self.agentToggle:
            response = self.chatModel.invoke(messages).content
        else:
            response = conversationAgent(self.chatModel, messages)
            if self.roleToggle:
                template = [("system", self.getTemplate())]
                template += [("system", "Now, re-write the following text considering you're role and limitations:")]
                template += [("ai", response)]
                chat_prompt = ChatPromptTemplate.from_messages(template)
                messages = chat_prompt.format_messages(role=self.role, name=self.name, user_name=self.user_name)
                response = self.chatModel.invoke(messages).content

        print(response)
        self.addInteraction("ai", response)
        return response


class APIConectionError(Exception):
    "Raised when cant connect to API"
    pass


