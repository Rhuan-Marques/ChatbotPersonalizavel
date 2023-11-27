"""
This file manages FinanceAgent and it tools
"""

from agents.agentABC import AbstractAgent
from langchain.agents import Tool

class FinanceAgent(AbstractAgent):
    """
            Agent meant to search for finance-related questions

            Tools:

            - Finance News: Search for news about the current financial market
                - Topic: Search about specific topics
                - Tickers: Searches about specific tickers
    """

    def getTools(self):
        """
        Returns the list of tools of the specific agent\n
        Overrides abstract method getTools() from AbstractAgent
        """
        ALPHAVILE_API_KEY = self.keys["ALPHAVANTAGE_API_KEY"]
        tools = []      # Creates empty list

        def getImportantNewsInfo(data):
            result = "Here are some relevant articles about your search: "
            i=0
            for article in data["feed"]:
                year = article["time_published"][0:4]
                month = article["time_published"][4:6]
                day = article["time_published"][6:8]
                hour = article["time_published"][9:11]
                minute = article["time_published"][11:13]
                time = f"{month}\\{day}\\{year} - {hour}:{minute}"

                result += time + " "
                result += article["title"] + " "
                result += article["summary"] + " "
                i+=1
            if len(result) > 4000:
                result = result[0:4000]
            result += "\n\nNow, use these articles info to reach a conclusion and report it to the user. If you can't find any important info in these articles, include this in your response: 'Sadly, i couldn't find any relevant information on recent articles online, please notify the user immediatly about this'"
            return result


        def requestNewsData(type="", input=""):
            """
                Function to request data about news of any topic,ticker,etc \n
                Uses AlphaVantage to get news headlines about finances in a specific topic
            """

            url = ("https://www.alphavantage.co/query?function=NEWS_SENTIMENT&" + type + "=" + input
                    + "&apikey=" + ALPHAVILE_API_KEY + "&limit=5")
            result = ""
            import requests
            try:
                r = requests.get(url)
                data = r.json()
            except Exception as e:
                result = f"""Failed to connect to the AlphaVantage API for finance information
                Exception: {e}.
                Notify the user about this"""
            else:
                result = getImportantNewsInfo(data)
            finally:
                return result

        def newsTopic(input=""):
            return requestNewsData("topics", input)

        tools.append(
            Tool(
                name="FinanceTopicNews",
                func=newsTopic,
                description= ("""Use it when you need recent financial news about specific topics, the supported topics are:
                'technology',
                'blockchain',
                'finance',
                'economy_macro',
                'financial_markets',
                'real_estate'
                'retail_wholesale'
                'earnings'.
                Always use these exact names for input, separated by a comma if you need multiple topics at once, for exemple: finalcial_markets,technology,blockchain""")
            )
        )

        def newsTicker(input=""):
            return requestNewsData("tickers", input)

        tools.append(
            Tool(
                name="FinanceTickerNews",
                func=newsTicker,
                description= ('Use it when you need recent financial news about one or more specific stock ticker, be precise with your input, it should be a single string and only use the ticker symbols, for exemple: instead of "Dolar" use "FOREX:USD", instead of "Bitcoin" use "CRYPTO:BTC", etc. For multiple tickers, separate them by a single comma')
            )
        )

        return tools