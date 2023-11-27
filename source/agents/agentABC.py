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
        :var MAX_RETRIES: Maximum number of retries in case of RateLimit
        :var MAX_RPM: Maximum number of Requests Per Minute permited by OpenAI
        :var requests: List of requests on the last minute, to keep track on RPM
    """
    MAX_RETRIES = 3
    MAX_RPM = 3
    requests = []
    def __init__(self, keys, llm):
        """
            Initialized agent
            :param llm: Large Language Model the Agent will use it function
        """
        self.keys=keys
        self.llm= llm
        self.agent = initialize_agent(
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            tools=self.getTools(),
            llm=self.llm,
            verbose=True,
            max_iterations=5,
            max_execution_time=140
        )
        # Updates the requests as to have a request on startup
        # This compensates the request to validate API Keys
        import time
        AbstractAgent.requests.append(time.time())


    def run(self, prompt):
        """Runs the agent based on the input text given
        :param prompt: Input prompt for agent to observe
        :return: Output text of agents response"""

        import time
        import random
        from openai._exceptions import RateLimitError
        # Agent retries to call the API multiple times for the Rate_Limit
        for i in range(self.MAX_RETRIES):
            try:
                # Keeps track of requests that might have expired the 1min limit
                # 1min = 65 seconds to let more room for error
                current_time = time.time()
                while (AbstractAgent.requests and
                       current_time - AbstractAgent.requests[0] > 65):
                    AbstractAgent.requests.pop(0)
                # If it ever gets to the RPM Limit, waits for the next request to expires
                if(len(AbstractAgent.requests) >= AbstractAgent.MAX_RPM):
                    wait_time = 65 - (current_time - AbstractAgent.requests[0])
                    AbstractAgent.requests.pop(0)
                else:
                    # A bit of wait-time between non-RPM reaching requests. Seems to help with consistency
                    wait_time = 5
                time.sleep(wait_time)
                # Append current time on the requests list before requesting
                AbstractAgent.requests.append(time.time())
                print(f"Requests :{AbstractAgent.requests}")
                result = self.agent(prompt)
            except RateLimitError:
                # If it hits rate-limit, waits exponentially more each time before trying again
                # Also adds a bit of randomness to the wait to not be as predictable
                wait_time = (3 ** i) + random.random()
                print("Rate Limit hit!")
                print(f"Will Retry {i+1}th time in {wait_time}\n")
                time.sleep(wait_time)
            except Exception as e:
                error_result = f"Unexpected error with agent: {e}. Communicate to the user"
                return error_result
            else:
                return result["output"]
        # If it gets out of the for loop, it returns to that it got stuck by the Rate Limit
        error_result = "Still hitting OpenAi APIs Rate Limit after max retries, inform the user"
        return error_result


    @abstractmethod
    def getTools(self):
        """Should return the list of tools of the specific agent"""
        pass