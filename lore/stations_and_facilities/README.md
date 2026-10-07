# Stations and Facilities

This directory separates **facility design knowledge** from live gameplay state.

## Core distinction

```text
FACILITY TYPE
!= DESIGN / DESIGN FAMILY
!= INDIVIDUAL FACILITY
!= OWNER
!= OPERATOR
!= CURRENT ASSIGNMENT
```

Examples:

- `starbase` — functional/type layer;
- `starfleet_spacedock_type` — reusable physical design;
- Earth Spacedock / Spacedock One — individual canonical facility;
- Starfleet — operator;
- regional fleet-support hub — current assignment.

A captured or jointly-operated station retains its physical identity unless an explicit refit/reconstruction changes it.

## Main catalogues

- `facility_design_generation_index_v0.1.json`
- `canonical_station_design_catalogue_v0.1.json`
- `canonical_unique_facilities_v0.1.json`
- `station_life_profiles_v0.1.json`

## Current reusable canonical design baseline

### Pike
- Starbase 1-type — controlled major-hub reuse.
- Bavali Station-type — restricted deuterium-refinery/outpost reuse.

### Kirk
- Starbase 6-type — restricted regional-starbase reuse.
- Starbase 25-type — restricted large-hub reuse.
- Regula I-type — reusable scientific station.
- Spacedock-type — reusable but rare major hub.
- Starbase 375-type — reusable research/regional-support design where era/configuration fits.

### TNG / DS9 / Voyager
- Regula I-type.
- Spacedock-type.
- McKinley-type drydock.
- Starbase 375-type.
- Relay Station 47-type.
- Terok Nor-type.
- Ty'Gokor orbital-facility design family.
- Monac-type Dominion/Cardassian shipyard.

The Dominion ketracel-white installation is modeled as a **functional facility family**, not one universal physical class.

## Reserved unique identities

Examples include:
- Starbase One;
- Deep Space Station K-7;
- Regula I;
- Earth Spacedock;
- Jupiter Station;
- Utopia Planitia Fleet Yards;
- Starbase 375;
- Relay Station 47;
- Deep Space 9 / Terok Nor;
- Empok Nor;
- Ty'Gokor orbital complex;
- Monac shipyards.

The generator may reuse an allowed design. It may never copy a reserved station's **name, facility_id, inhabitants, damage, ownership history or biography**.

## Procedural station rule

```text
sustained world need
→ alternatives check
→ existing coverage
→ smallest sufficient scale
→ operator/sponsor
→ site
→ canonical/authored design if valid
→ procedural reusable design only if needed
→ construction
→ commissioning
→ staff/residents/services
→ causal traffic
→ persistent history
```

A station is never generated because the player wants fuel, repair, shopping, an interesting location or a shorter trip.
