from typing import Annotated, TypedDict, Union
import operator

from langchain_core.agents import AgentAction, AgentFinish

# Agent Outcome (Output by the runnable) is either AgentAction / AgentFinish. Initially it is None
# Intermediate Steps holds all the history 
class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]