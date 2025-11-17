from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from basic_chains import generation_chain, reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE  = "generate"

graph = MessageGraph()

# state -> list of messages that happened in the past
def generate_node(state):
    return generation_chain.invoke({
        "messages": state
    })

def reflection_node(state):
    response = reflection_chain.invoke({
        "messages": state
    })

    return [HumanMessage(content = response.content)]           # Trick the model into thinking that the critique is being given by a Human

def should_continue(state):
    if(len(state) > 4):
        return END
    return REFLECT

# Building the graph
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflection_node)

graph.set_entry_point(GENERATE)
graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

# Invoke the Graph
response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))
print(response)