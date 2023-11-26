"""
This file manages GeneralAgent and it tools
"""

from agents.agentABC import AbstractAgent
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.tools import StructuredTool, DuckDuckGoSearchRun
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

        def search(input=""):
            """
                Function for tool searchTool\n
                Uses DuckDuckGo API to search the internet
            """
            return DuckDuckGoSearchRun()

        tools.append(
            Tool(
                name="Search",
                func=search,
                description= "Useful when you need to search the internet for information you can't get alone, be specific with your input"
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

        def wikipedia(input=""):
            """
                Function for tool wikiTool\n
                Uses Wikipedia API
            """
            return WikipediaAPIWrapper()

        tools.append(
            Tool(
                name="Wikipedia",
                func=wikipedia,
                description="Useful to look up specifc information about a person, country or topic on wikipedia"
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

        def callFinanceAgent(input=""):
            from agents.financeAgent import FinanceAgent
            agent = FinanceAgent( keys=self.keys)
            return agent.run(input)

        if self.keys["ALPHAVANTAGE_API_KEY"]:
            tools.append(
                Tool(
                    name="FinanceAgent",
                    func=callFinanceAgent,
                    description="Useful to get info about the current financial market. Generate a detailed text of what you need to know as your input"
                )
            )

        return tools