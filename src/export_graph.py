from pathlib import Path
import json
import networkx as nx
from networkx.readwrite import json_graph

from build_tsif_graph import build_tsif_graph


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    demo_path = root / "data" / "demo_dynasties.json"
    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    G = build_tsif_graph(demo_path)

    # GraphML (good for Gephi)
    graphml_path = out_dir / "tsif.graphml"
    nx.write_graphml(G, graphml_path)

    # Node-link JSON
    data = json_graph.node_link_data(G)
    json_path = out_dir / "tsif_node_link.json"
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"Wrote: {graphml_path}")
    print(f"Wrote: {json_path}")