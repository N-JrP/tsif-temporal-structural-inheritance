from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pandas as pd
import networkx as nx

from build_tsif_graph import build_tsif_graph


def structural_footprints_by_generation(G: nx.MultiDiGraph, dynasty_id: str) -> pd.DataFrame:
    """
    TSIF Metric: Structural Footprint per generation.

    footprint(g) = (#places, #institutions, #domains, reach_2hop)

    reach_2hop = unique nodes reachable within 2 hops from all persons in generation
                 (using outgoing edges, since our modeling is directed).
    """
    persons = [
        n
        for n, d in G.nodes(data=True)
        if d.get("node_type") == "Person" and d.get("dynasty_id") == dynasty_id
    ]
    if not persons:
        return pd.DataFrame()

    by_gen = defaultdict(list)
    for p in persons:
        gen = G.nodes[p].get("generation")
        if gen is not None:
            by_gen[int(gen)].append(p)

    rows = []
    for gen, gen_people in sorted(by_gen.items()):
        places, insts, doms, reach = set(), set(), set(), set()

        for p in gen_people:
            # Count direct structural embedding
            for _, nbr, _edata in G.out_edges(p, data=True):
                ntype = G.nodes[nbr].get("node_type")
                if ntype == "Place":
                    places.add(nbr)
                elif ntype == "Institution":
                    insts.add(nbr)
                elif ntype == "Domain":
                    doms.add(nbr)

            # 2-hop reach
            one_hop = set(G.successors(p))
            two_hop = set()
            for n1 in one_hop:
                two_hop.update(G.successors(n1))

            reach.update(one_hop)
            reach.update(two_hop)

        rows.append(
            {
                "dynasty_id": dynasty_id,
                "generation": gen,
                "people_count": len(gen_people),
                "places_count": len(places),
                "institutions_count": len(insts),
                "domains_count": len(doms),
                "reach_2hop_count": len(reach),
            }
        )

    return pd.DataFrame(rows)


def inheritance_shift(df: pd.DataFrame) -> pd.DataFrame:
    """
    TSIF Metric: Inheritance Shift = delta of structural footprint
    between consecutive generations.
    """
    if df.empty:
        return df

    df = df.sort_values(["dynasty_id", "generation"]).copy()
    metrics = ["places_count", "institutions_count", "domains_count", "reach_2hop_count"]

    for m in metrics:
        df[f"delta_{m}"] = df.groupby("dynasty_id")[m].diff()

    return df


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    demo_path = root / "data" / "demo_dynasties.json"

    G = build_tsif_graph(demo_path)

    out_dir = root / "outputs"
    out_dir.mkdir(exist_ok=True)

    frames = []
    for did in ["rothschild", "guinness"]:
        frames.append(structural_footprints_by_generation(G, did))

    df = pd.concat(frames, ignore_index=True)
    df = inheritance_shift(df)

    out_path = out_dir / "footprints.csv"
    df.to_csv(out_path, index=False)

    print(f"Wrote: {out_path}")
    print(df.to_string(index=False))