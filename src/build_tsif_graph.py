import json
from pathlib import Path
import networkx as nx


def load_demo_data(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def add_event_nodes(G: nx.MultiDiGraph, dynasty_id: str, events: list[dict]) -> None:
    """
    Add Event nodes for a dynasty.
    Event node id format: event::<dynasty_id>::<event_id>
    """
    for ev in events:
        ev_node = f"event::{dynasty_id}::{ev['event_id']}"
        G.add_node(
            ev_node,
            node_type="Event",
            dynasty_id=dynasty_id,
            event_id=ev["event_id"],
            label=ev["name"],
            start_year=ev.get("start_year"),
            end_year=ev.get("end_year"),
        )


def add_person_node(G: nx.MultiDiGraph, dynasty_id: str, person: dict) -> None:
    G.add_node(
        person["person_id"],
        node_type="Person",
        dynasty_id=dynasty_id,
        name=person["name"],
        birth_year=person.get("birth_year"),
        death_year=person.get("death_year"),
        generation=person.get("generation"),
    )

    # Attach Place/Institution/Domain nodes + edges
    for place in person.get("places", []):
        place_id = f"place::{place}"
        G.add_node(place_id, node_type="Place", label=place)
        G.add_edge(person["person_id"], place_id, key="EMBEDDED_IN", rel_type="EMBEDDED_IN")

    for inst in person.get("institutions", []):
        inst_id = f"inst::{inst}"
        G.add_node(inst_id, node_type="Institution", label=inst)
        G.add_edge(person["person_id"], inst_id, key="AFFILIATED_WITH", rel_type="AFFILIATED_WITH")

    for dom in person.get("domains", []):
        dom_id = f"dom::{dom}"
        G.add_node(dom_id, node_type="Domain", label=dom)
        G.add_edge(person["person_id"], dom_id, key="ACTIVE_IN", rel_type="ACTIVE_IN")

    # Generation node
    gen = person.get("generation")
    if gen is not None:
        gen_id = f"gen::{dynasty_id}::{gen}"
        G.add_node(gen_id, node_type="Generation", dynasty_id=dynasty_id, generation=gen)
        G.add_edge(person["person_id"], gen_id, key="BELONGS_TO_GENERATION", rel_type="BELONGS_TO_GENERATION")

    # Optional: Event context edges
    for ev_id in person.get("event_context", []):
        ev_node = f"event::{dynasty_id}::{ev_id}"
        if G.has_node(ev_node):
            G.add_edge(person["person_id"], ev_node, key="CONTEXTUALIZED_BY", rel_type="CONTEXTUALIZED_BY")


def add_relations(G: nx.MultiDiGraph, person: dict) -> None:
    src = person["person_id"]
    for rel in person.get("relations", []):
        rtype = rel["type"]
        tgt = rel["target"]
        G.add_edge(src, tgt, key=rtype, rel_type=rtype)


def build_tsif_graph(demo_json_path: Path) -> nx.MultiDiGraph:
    data = load_demo_data(demo_json_path)
    G = nx.MultiDiGraph(model="TSIF")

    for dyn in data["dynasties"]:
        dynasty_id = dyn["dynasty_id"]

        # Dynasty node
        dyn_node = f"dyn::{dynasty_id}"
        G.add_node(
            dyn_node,
            node_type="Dynasty",
            label=dyn["dynasty_name"],
            origin_place=dyn.get("origin_place"),
        )

        # Add Event nodes (before people so we can connect event_context edges)
        add_event_nodes(G, dynasty_id, dyn.get("events", []))

        # Add people nodes
        for person in dyn["people"]:
            add_person_node(G, dynasty_id, person)
            G.add_edge(person["person_id"], dyn_node, key="MEMBER_OF", rel_type="MEMBER_OF")

        # Add person-to-person relations (parent/child, spouse, etc.)
        for person in dyn["people"]:
            add_relations(G, person)

    return G


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    demo_path = root / "data" / "demo_dynasties.json"
    G = build_tsif_graph(demo_path)
    print(f"Built TSIF graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")