"""
This file manages the Langchain Agent(s) and it(s) tool(s)
"""
from langchain.agents import initialize_agent, AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.tools import StructuredTool, DuckDuckGoSearchRun
from langchain.llms import OpenAI
import random

def calculator(input=""):
    """
    Function for tool mathTool\n
    Creates an MathChainLLM with the key from stApp.py
    """
    from stApp import getKey
    key = getKey()
    try:
        llm = OpenAI(temperature=0, openai_api_key=key)
        mathChain = LLMMathChain.from_llm(llm, verbose=True)
    except:
        return "Error occured, couldn't connect to API, tell this to the user"
    return mathChain.run(input)

mathTool = Tool(
    name="Math",
    func=calculator,
    description="Useful for doing complex math problems, be specific with your input"
)

def search(input=""):
    """
        Function for tool searchTool\n
        Uses DuckDuckGo API to search the internet
    """
    return DuckDuckGoSearchRun()

searchTool = Tool(
    name="Search",
    func=search,
    description="Useful when you need to search the internet for information you can't get alone, be specific with your input"
)

def wikipedia(input=""):
    """
        Function for tool wikiTool\n
        Uses Wikipedia API
    """
    return WikipediaAPIWrapper()

wikiTool = Tool(
    name="Wikipedia",
    func=wikipedia,
    description="Useful to look up specifc information about a person, country or topic on wikipedia"
)

def generateRandom(min:int, max:int):
    """
        Function for tool randomTool\n
        Generates a random number between the two given ints
    """
    result = random.randint(min, max)

    return result

randomTool = StructuredTool.from_function( #Structured because needs multiple inputs
    name="Random",
    func=generateRandom,
    description="Generates a random number between two given ints"
)

tools = [searchTool, randomTool, wikiTool, mathTool]
def runAgent(llm, input):

    """
        Creates and runs an Agent
        :param llm: The Large Language Model that will power the agent
        :param input: Initial input of what to do
        :return: Output text of what the agents response
    """
    myAgent = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm = llm,
        verbose=True,
        max_iterations=3
    )
    result = myAgent(input)
    return result["output"]