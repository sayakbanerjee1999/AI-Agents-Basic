from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model = "gpt-4.1-mini",
)

################################### Using Pydantic Base Model #########################################

class Country(BaseModel):
    """Information about a Country"""
    name: str = Field(description="Name of the country")
    language: str = Field(description="Language spoken predominantly in the Country")
    capital: str = Field(description="Capital of the country")

structured_llm = llm.with_structured_output(Country)
print(structured_llm)

# The pydantic function is sent as a tool in the backend to the LLM to generate the structured response.
response = structured_llm.invoke("Tell me about India")
print(response)





################################### Using Typed Dict #########################################

from typing_extensions import Annotated, TypedDict
from typing import Optional

class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke)

response = structured_llm.invoke("Tell me a joke about cats")
print(response)



################################### Using A JSON Schema #########################################

json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}
structured_llm = llm.with_structured_output(json_schema)

response = structured_llm.invoke("Tell me a joke about the Argentine National Football Team")
print(response)