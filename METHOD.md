# TSIF — Temporal Structural Inheritance Framework (v0.1)

## Motivation
Most genealogy tools model lineage as a **biological tree** (parent → child).  
Digital history often needs a model of **structural inheritance**: how people inherit and expand positions across *places, institutions, and domains* over generations.

TSIF proposes:
> A generation inherits not only persons, but also **structural embedding** within geography, institutions, and activity domains.

## Core Entities (Node Types)
- **Person**: historical actor with (birth_year, death_year, generation)
- **Generation**: dynasty-scoped generation index (1,2,3…)
- **Place**: city/region nodes
- **Institution**: banks, companies, guilds, houses, etc.
- **Domain**: finance, brewing, trade, politics, etc.
- *(Optional)* **Event**: wars, reforms, policy shifts (context anchors)

## Relations (Edge Types)
- `PARENT_OF`, `SPOUSE_OF`
- `EMBEDDED_IN` (Person → Place)
- `AFFILIATED_WITH` (Person → Institution)
- `ACTIVE_IN` (Person → Domain)
- `BELONGS_TO_GENERATION` (Person → Generation)
- *(Optional)* `CONTEXTUALIZED_BY` (Person/Institution → Event)

## TSIF Metrics

### Structural Footprint (per generation)
For dynasty D and generation g:
- `places_count(g)` = distinct places linked by persons in g
- `institutions_count(g)` = distinct institutions linked by persons in g
- `domains_count(g)` = distinct domains linked by persons in g
- `reach_2hop_count(g)` = unique nodes reachable within 2 hops from persons in g

### Inheritance Shift (between generations)
Between consecutive generations:
- `Δplaces = places_count(g+1) - places_count(g)`
- `Δinstitutions = institutions_count(g+1) - institutions_count(g)`
- `Δdomains = domains_count(g+1) - domains_count(g)`
- `Δreach_2hop = reach_2hop_count(g+1) - reach_2hop_count(g)`

## Demo Dataset Notice
This repository includes a minimal illustrative dataset (Rothschild, Guinness) to demonstrate TSIF mechanics.  
It is not intended as exhaustive historical reconstruction.