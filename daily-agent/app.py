import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_community.tools.serpapi.tool import SerpAPIWrapper
from langchain.llms import OpenAI

load_dotenv()

llm = OpenAI(temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

tools = [
    Tool(
        name="Web Search",
        func=search.run,
        description="Useful for finding up-to-date information about anything, especially product listings like cars."
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    result = agent.run("How many used electric cars under $25,000 are for sale in Maryland?")
    print("\n--- Summary ---")
    print(result)

