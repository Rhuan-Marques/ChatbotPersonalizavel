"""
This file manages GeneralAgent and it tools
"""
from agents.agentABC import AbstractAgent
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.tools import StructuredTool, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
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
    def __init__(self, keys, llm):
        self.keys=keys
        self.llm = llm
        """
            Initialized agent
            :param llm: Large Language Model the Agent will use it function
        """
        self.MAX_RETRIES = 5
        from agents.generalAgent import GeneralAgent
        self.agent = GeneralAgent(llm=llm, keys=keys)


    def run(self, prompt):
        """Runs the agent based on the input text given
        :param prompt: Input prompt for agent to observe
        :return: Output text of agents response"""

        import time
        import random
        from openai._exceptions import RateLimitError
        # Agent retries to call the API multiple times waiting exponentially longer for the Rate_Limit
        for i in range(self.MAX_RETRIES):
            #print("Creating agent\n")
            try:
                time.sleep(5)
                #print("Times Up!\n")
                result = self.agent(prompt)
                #print("Agent Done!\n")
            except RateLimitError:
                wait_time = (5 ** (i+1)) + random.random()
                #print("Rate Limit hit!")
                #print(f"Will Retry {i+1}th time in {wait_time}")
                time.sleep(wait_time)
            except Exception as e:
                error_result = f"Unexpected error with agent: {e}. Communicate to the user"
                return error_result
            else:
                return result["output"]
        error_result = "Still hitting OpenAi APIs Rate Limit after max retries, inform the user"
        return error_result





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


        if self.keys["ALPHAVANTAGE_API_KEY"]:
            def financeAgentCall(input=""):
                from agents.financeAgent import FinanceAgent
                self.agent = FinanceAgent(llm=self.llm, keys=self.keys)
                return input

            tools.append(
                Tool(
                    name="FinanceAgent",
                    func=financeAgentCall,
                    description="Calls agent for information about current finance market, blockchain, real state, etc. Describe exactly what you need for your input"
                )
            )

        return tools