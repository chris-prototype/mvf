from orchestrator.graph import build_graph, should_block
from orchestrator.state import FactoryState

EXPECTED_NODES = {
    "pm_agent", "gate_1", "architect_agent", "gate_2",
    "dev_agent", "review_agent", "test_agent", "gate_3", "deploy_agent",
    "done_handler", "blocked_handler",
}


def test_build_graph_has_all_nodes():
    builder = build_graph()
    assert EXPECTED_NODES.issubset(set(builder.nodes))


def test_build_graph_compiles():
    compiled = build_graph().compile()
    assert compiled is not None


state1 = FactoryState(
    ticket_id="LIN-1",
    title="test ticket",
    error="boom",
    current_state="Spec",
)

state2 = FactoryState(
    ticket_id="LIN-1",
    title="test ticket",
    error="",
    current_state="Spec",
)

def test_should_block_routes_on_error():
    assert should_block(state1) == "blocked_handler"
    assert should_block(state2) == "continue"