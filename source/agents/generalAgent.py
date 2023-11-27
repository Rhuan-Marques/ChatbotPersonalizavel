"""
This file manages GeneralAgent and it tools
"""
from agents.agentABC import AbstractAgent
from langchain.chains import LLMMathChain
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.tools import StructuredTool, DuckDuckGoSearchRun, WikipediaQueryRun
import random


class GeneralAgent(AbstractAgent):
    """
            Agent meant to be the head that chooses broadly what to do\n
            Calls other agents for more specific purposes\n

            Tools:

            - Wikipedia: Look info on Wikipedia
            - Search: Use DuckDuckGo to search info
            - Math: Can solve complex math problems
            - Random: Emulates RNG
    """


    def getTools(self):
        """
        Returns the list of tools of the specific agent\n
        Overrides abstract method getTools() from AbstractAgent
        """
        llm = self.llm  # Sets up accessible llm for tools that need it
        tools = []      # Creates empty list

        search = DuckDuckGoSearchRun()

        tools.append(
            Tool(
                name="Search",
                func=search.run,
                description= "Useful when you need to search the internet for information, be specific with your input"
            )
        )

        def calculator(input=""):
            """
            Function for tool mathTool\n
            Uses self.llm to generate a LLMMathChain
            """
            try:
                mathChain = LLMMathChain.from_llm(llm, verbose=True)
                mathChain.run(input)
            except ValueError:
                return "Error occured, not all the values needed are known. Maybe search before trying Math?"
            except:
                return "Unexpected error occured, tell this to the user"

            return

        tools.append(
            Tool(
                name="Math",
                func=calculator,
                description="Useful for doing complex math problems. Only use it when you already know all the numbers needed in the equation"
            )
        )

        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

        tools.append(
            Tool(
                name="Wikipedia",
                func=wikipedia.run,
                description="Useful to look up information about a person, country or event on wikipedia, but only use it if you already know the specific name of whoever/whatever you are looking for. Be precise with your input, only the name, not the characteristics of the request. For exemple, if you want to know \"Age of Leonardo Di Caprio\" Input only: \"Leonardo Di Caprio\", if you want to know \"How many people died in World War II\" Input only: \"World War 2\""
            )
        )

        def generateRandom(min: int, max: int):
            """
                Function for tool randomTool\n
                Generates a random number between the two given ints
            """
            result = random.randint(min, max)
            return result

        tools.append(
            StructuredTool.from_function(  # Structured because needs multiple inputs
                name="Random",
                func=generateRandom,
                description="Generates a random number between two given ints"
            )
        )


        if self.keys["ALPHAVANTAGE_API_KEY"]:
            def financeAgentCall(input=""):
                from agents.financeAgent import FinanceAgent
                agent = FinanceAgent(llm=self.llm, keys=self.keys)
                result = agent.run(input)
                return result

            tools.append(
                Tool(
                    name="FinanceAgent",
                    func=financeAgentCall,
                    description="Calls agent for information about current finance market, blockchain, real state, etc. Describe what you need for your input, talk like a human, don't be too brief"
                )
            )

        return tools