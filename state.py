from typing import TypedDict

# define the shape for the FactoryState passed to LangGraph's StateGraph
class FactoryState(TypedDict):
    ticket_id: str
    title: str
