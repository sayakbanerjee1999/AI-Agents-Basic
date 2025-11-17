from typing import TypedDict, List
from langgraph.graph import END, StateGraph

class SimpleState(TypedDict):
    count: int
    sum: int
    history: List[int]

def increment(state: SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    # Example of Manual State Transformation -> Updating the state after every step
    # Calculations and everything performed through here
    return {
        "count": new_count,
        "sum": state["sum"] + new_count,
        "history": state["history"] + [new_count]
    }

def should_continue(state):
    if(state["count"] < 5):
        return "continue"
    else:
        return "stop"

graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.set_entry_point("increment")

# Syntactical Change here - Same as returning "incfement"/"END" in should_continue
graph.add_conditional_edges("increment", should_continue, {
    "continue": "increment",
    "stop": END
})

app = graph.compile()

state = {
    "count": 0,
    "sum": 0,
    "history": []
}

response = app.invoke(state)
print(response)