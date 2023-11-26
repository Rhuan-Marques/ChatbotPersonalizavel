"""
This file manages the abstract concept of a Langchain Agent(s) and it(s) tool(s)
Agents must inhert from this class for organization
"""
from abc import ABC, abstractmethod
from langchain.agents import initialize_agent, AgentType

class AbstractAgent(ABC):
    """
            Abstract class for creation of agents\n
            Useful for centralization and so that it's methods can have information like its llm
    """

    def __init__(self, keys):
        from langchain.chat_models import ChatOpenAI
        self.keys=keys
        self.llm = ChatOpenAI(openai_api_key=keys["OPENAI_API_KEY"])
        """
            Initialized agent
            :param llm: Large Language Model the Agent will use it function
        """
        self.MAX_RETRIES = 5
        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=self.getTools(),
            llm=self.llm,
            verbose=True,
            max_iterations=3
        )


    def run(self, prompt):
        """Runs the agent based on the input text given
        :param prompt: Input prompt for agent to observe
        :return: Output text of agents response"""

        import time
        import random
        # Agent retries to call the API multiple times waiting exponentially longer for the Rate_Limit
        for i in range(self.MAX_RETRIES):
            from openai._exceptions import RateLimitError
            try:
                time.sleep(5)
                result = self.agent(prompt)
            except RateLimitError:
                wait_time = (5 ** (i+1)) + random.random()
                print("Rate Limit hit!")
                print(f"Will Retry {i+1}th time in {wait_time}")
                time.sleep(wait_time)
            except Exception as e:
                error_result = f"Unexpected error with agent: {e}. Communicate to the user"
                return error_result
            else:
                return result["output"]
        error_result = "Still hitting OpenAi APIs Rate Limit after max retries, inform the user"
        return error_result

    @abstractmethod
    def getTools(self):
        """Should return the list of tools of the specific agent"""
        pass