from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import datetime

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

search_tool = TavilySearchResults(
    search_depth = "basic"
)

# Docstring needs to be given for a tool
@tool
def system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system date time in the specified Format"""
    curr_time = datetime.datetime.now()
    format_time = curr_time.strftime(format)
    return format_time

# Initialize the Zero Shot ReACT Agent with required tools
# Prompt - https://smith.langchain.com/hub/hwchase17/react?organizationId=d249de7b-ca3c-4265-b3bd-6b655478a206
agent = initialize_agent(
    tools = [search_tool, system_time],
    llm = llm,
    agent = "zero-shot-react-description",
    verbose = True
)

agent.invoke("When was the last SpaceX launch and how long ago was it from this instant?")