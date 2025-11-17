from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_react_agent
from langchain_community.tools import TavilySearchResults
from langchain import hub
import datetime
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model = "gpt-4.1-mini"
)

search_tool = TavilySearchResults(
    search_depth = "basic"
)

# Docstring needs to be given for a tool
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system date time in the specified Format"""
    curr_time = datetime.datetime.now()
    format_time = curr_time.strftime(format)
    return format_time

tools = [search_tool, get_system_time]
react_prompt = hub.pull("hwchase17/react")

react_agent_runnable = create_react_agent(
                        llm = llm,
                        tools = tools,
                        prompt = react_prompt
                    )