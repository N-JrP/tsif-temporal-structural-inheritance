from pathlib import Path
import networkx as nx

from build_tsif_graph import build_tsif_graph


def time_travel_query(G: nx.MultiDiGraph, dynasty_id: str, year: int):
    """
    Lightweight time-travel query:
    Find persons whose lifespan overlaps the year, then print their structural embedding.
    """
    persons = []
    for n, d in G.nodes(data=True):
        if d.get("node_type") != "Person" or d.get("dynasty_id") != dynasty_id:
            continue
        b = d.get("birth_year")
        de = d.get("death_year")
        if b is None or de is None:
            continue
        if b <= year <= de:
            persons.append(n)

    results = []
    for p in persons:
        context = {
            "person": G.nodes[p]["name"],
            "year": year,
            "places": [],
            "institutions": [],
            "domains": [],
        }
        for _, nbr, _edata in G.out_edges(p, data=True):
            ntype = G.nodes[nbr].get("node_type")
            label = G.nodes[nbr].get("label")
            if ntype == "Place":
                context["places"].append(label)
            elif ntype == "Institution":
                context["institutions"].append(label)
            elif ntype == "Domain":
                context["domains"].append(label)
        results.append(context)

    return results


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    demo_path = root / "data" / "demo_dynasties.json"
    G = build_tsif_graph(demo_path)

    out_path = root / "outputs" / "example_query_output.txt"
    out_path.parent.mkdir(exist_ok=True)

    lines = []
    lines.append("TSIF Demo Query Output\n")
    lines.append("=" * 60 + "\n\n")

    lines.append("Time-travel query: Rothschild @ 1810\n")
    lines.append("-" * 60 + "\n")
    for r in time_travel_query(G, "rothschild", 1810):
        lines.append(str(r) + "\n")

    lines.append("\nTime-travel query: Guinness @ 1790\n")
    lines.append("-" * 60 + "\n")
    for r in time_travel_query(G, "guinness", 1790):
        lines.append(str(r) + "\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote: {out_path}")