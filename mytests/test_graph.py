from pathlib import Path
from orchestrator.graph import build_graph

graph = build_graph().compile()
real_graph = graph.get_graph()
mermaid_graph = real_graph.draw_mermaid()

output_path = Path("graph.mmd")
output_path.write_text(mermaid_graph, encoding="utf-8")

