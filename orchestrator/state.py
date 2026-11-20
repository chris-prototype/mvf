"""

 - Contains the FactoryState definition used by LangGraph

"""
from typing_extensions import TypedDict


# define the shape for the FactoryState passed to LangGraph's StateGraph
class FactoryState(TypedDict):
    ticket_id: str
    title: str
    error: str
    current_state: str
