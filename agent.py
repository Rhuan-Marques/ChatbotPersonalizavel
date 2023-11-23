from langchain.agents import initialize_agent, AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.llms import OpenAI
import random

def calculator(input=""):
    llm = OpenAI(temperature=0)
    mathChain = LLMMathChain.from_llm(llm, verbose=True)
    return mathChain.run(input)

mathTool = Tool(
    name="Math",
    func=calculator,
    description="Useful for doing complex math problems, be specific with your input"
)

search = DuckDuckGoSearchRun()

searchTool = Tool(
    name="Search",
    func=search.run,
    description="Useful when you need to search the internet for information you can't get alone, be specific with your input"
)

wikipedia = WikipediaAPIWrapper()

wikiTool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="Useful to look up specifc information about a person, country or topic on wikipedia"
)

def generateRandom(min=0, max=100):
    return random.randint(min, max)

randomTool = Tool(
    name="Random",
    func=generateRandom,
    description="Useful when you need to generate a random number in a range. input should be the minimum and maximum number of the specific range"
)

tools = [searchTool, randomTool, wikiTool, searchTool, mathTool]
def conversationAgent(llm, input):
    myAgent = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm = llm,
        verbose=True,
        max_iterations=3
    )

    #executor = AgentExecutor(agent=myAgent, tools=tools)
    #executor.invoke({"input": input})
    result = myAgent(input)

    return result["output"]