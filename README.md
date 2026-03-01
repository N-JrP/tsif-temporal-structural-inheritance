# TSIF — Temporal Structural Inheritance Framework

TSIF (Temporal Structural Inheritance Framework) models genealogy as **structural inheritance across generations**, not only biological lineage.

Instead of parent–child trees, TSIF represents individuals as embedded in:

- Places  
- Institutions  
- Activity domains  
- Historical events  

using a typed knowledge graph with computable generational metrics.

---

## Why

Digital history tools often lack formal models for:

- Cross-generational structural embedding  
- Geographic and institutional expansion  
- Event-contextual lineage  
- Measurable generational change  

TSIF provides a minimal, reusable schema + metric layer to address this gap.

---

## What It Implements

### Graph Model
Node types:
- Person
- Generation
- Place
- Institution
- Domain
- Event
- Dynasty

Edge types:
- PARENT_OF
- EMBEDDED_IN
- AFFILIATED_WITH
- ACTIVE_IN
- BELONGS_TO_GENERATION
- CONTEXTUALIZED_BY
- MEMBER_OF

---

## Structural Metrics

**Structural Footprint (per generation)**
- Distinct places
- Distinct institutions
- Distinct domains
- Two-hop network reach

**Inheritance Shift**
- Δ structural embedding across generations

**Generation-Aware Centrality**
- Average degree centrality
- Average betweenness centrality
- Most structurally central individual

---

## Interoperability

Exports:
- GraphML (Gephi / Neo4j compatible)
- Node-link JSON

---

## Quickstart

```bash
pip install -r requirements.txt
python src/build_tsif_graph.py
python src/compute_footprints.py
python src/centrality_metrics.py
python src/export_graph.py```

---

## Positioning

TSIF is designed as a building block for:

- Computational digital history  
- Knowledge graph–based heritage modeling  
- Generational diffusion analysis  

The included dataset is illustrative. The framework is dynasty-agnostic.
