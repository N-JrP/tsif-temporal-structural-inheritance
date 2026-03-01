from __future__ import annotations
from pathlib import Path
from collections import defaultdict

import pandas as pd
import networkx as nx

from build_tsif_graph import build_tsif_graph


def _dynasty_persons(G: nx.MultiDiGraph, dynasty_id: str) -> list[str]:
    return [
        n for n, d in G.nodes(data=True)
        if d.get("node_type") == "Person" and d.get("dynasty_id") == dynasty_id
    ]


def centrality_by_generation(G: nx.MultiDiGraph, dynasty_id: str) -> pd.DataFrame:
    """
    Compute centrality metrics on an undirected projection of the TSIF graph,
    then summarize per generation for persons in the dynasty.
    """
    persons = _dynasty_persons(G, dynasty_id)
    if not persons:
        return pd.DataFrame()

    # Undirected simple graph projection (multi-edges collapsed)
    UG = nx.Graph()
    for u, v, _k, edata in G.edges(keys=True, data=True):
        UG.add_edge(u, v, rel_type=edata.get("rel_type"))

    # Centralities (keep it lightweight + stable)
    degree_c = nx.degree_centrality(UG)
    between_c = nx.betweenness_centrality(UG, normalized=True)

    # Group persons by generation
    by_gen = defaultdict(list)
    for p in persons:
        gen = G.nodes[p].get("generation")
        if gen is not None:
            by_gen[int(gen)].append(p)

    rows = []
    for gen, gen_people in sorted(by_gen.items()):
        rows.append({
            "dynasty_id": dynasty_id,
            "generation": gen,
            "people_count": len(gen_people),
            "avg_degree_centrality": sum(degree_c.get(p, 0.0) for p in gen_people) / len(gen_people),
            "avg_betweenness_centrality": sum(between_c.get(p, 0.0) for p in gen_people) / len(gen_people),
            "top_person_by_betweenness": max(gen_people, key=lambda p: between_c.get(p, 0.0)),
            "top_person_by_betweenness_name": G.nodes[max(gen_people, key=lambda p: between_c.get(p, 0.0))].get("name"),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    demo_path = root / "data" / "demo_dynasties.json"
    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    G = build_tsif_graph(demo_path)

    frames = []
    for did in ["rothschild", "guinness"]:
        frames.append(centrality_by_generation(G, did))

    df = pd.concat(frames, ignore_index=True)
    out_path = out_dir / "centrality_by_generation.csv"
    df.to_csv(out_path, index=False)

    print(f"Wrote: {out_path}")
    print(df.to_string(index=False))