'''

In the graph reducers, a refer to the current value, and b refers to the new value

'''

from typing import TypedDict, Annotated


def _last(a: str, b: str) -> str:
    return b if b else a


def _last_list(a: list, b: list) -> list:
    return b if b else a


def _last_dict(a: dict, b: dict) -> dict:
    return b if b else a


class FactoryState(TypedDict):
    ticket_id: Annotated[str, _last]
    title: Annotated[str, _last]
    current_state: Annotated[str, _last]
    error: Annotated[str, _last]
    parent_issue_id: Annotated[str, _last]
    subtasks: Annotated[list[dict], _last_list]
    stage_sub_issues: Annotated[dict[str, str], _last_dict]
    repo_name: Annotated[str, _last]
    workspace_path: Annotated[str, _last]


TRIGGER_STATES: frozenset[str] = frozenset(
    {"In Spec", "In Arch", "In Dev", "In QA", "In Deploy"}
)
