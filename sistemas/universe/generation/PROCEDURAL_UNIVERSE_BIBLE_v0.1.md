# Procedural Universe Bible v0.1

Status: **FOUNDATION IN PROGRESS**

## Purpose

Provide enough structured Star Trek knowledge that the game can populate a persistent universe without manually authoring every system, ship, facility or secondary NPC.

This is the Star Trek equivalent of a world-generation bible: the generator must know not only what can exist, but why it would exist there, who built/operates it, what it is doing and what other systems can observe about it.

## Prime rule

> **Generate reality first. Observe it second.**

Procedural truth is materialized before Sensors, Computer, NPC dialogue, missions or UI ask about it.

A scan never creates the thing it is looking for.

## Generation question chain

Every generated entity should be explainable through a chain like:

```text
WHAT CAN EXIST?
      ↓
WHERE CAN IT EXIST?
      ↓
WHEN CAN IT EXIST?
      ↓
WHO / WHAT CREATED OR OPERATES IT?
      ↓
WHY IS IT THERE?
      ↓
WHAT IS ITS CURRENT STATE?
      ↓
WHAT IS IT DOING?
      ↓
WHAT SIGNATURES DOES IT PRODUCE?
      ↓
WHO CAN KNOW ABOUT IT?
```

## Generation context

At minimum, generators may consume:

- campaign seed;
- campaign date;
- playable era;
- galactic region / sector;
- canonical reservations;
- known astrography;
- political/faction context;
- civilization context;
- technology availability;
- local resources;
- traffic/economic context;
- campaign history;
- nearby persistent entities.

## Domain 1 — Cosmic structure and phenomena

The universe generator eventually needs profiles for:

- stars;
- multiple-star systems;
- planets;
- dwarf planets;
- moons;
- ring systems;
- asteroids;
- asteroid belts;
- comets;
- meteoroid/debris populations;
- nebulae;
- stellar nurseries;
- supernova remnants;
- neutron stars;
- pulsars;
- black holes;
- quasars/active galactic phenomena where contextually relevant;
- radiation regions;
- plasma storms;
- gravimetric disturbances;
- subspace phenomena;
- spatial anomalies;
- wormholes;
- other Star Trek-specific phenomena.

Generation must respect physical/context constraints first and Star Trek-specific allowances second.

Not every system needs an anomaly.

## Domain 2 — Habitable worlds and civilizations

A generated world may require:

- physical world profile;
- atmosphere;
- gravity;
- climate envelope;
- hydrosphere;
- biosphere;
- habitability;
- resources;
- intelligent life presence;
- civilization technological level;
- political organization;
- settlement distribution;
- orbital infrastructure;
- contact status;
- known/unknown status to Starfleet;
- relationship to nearby powers.

A civilization does not need to belong to a major canonical faction.

Generated civilizations must be persistent once materialized.

## Domain 3 — Starships of all roles

Procedural traffic must not collapse into warships.

Required role families include, where valid:

- cargo freighter;
- bulk hauler;
- passenger liner;
- personnel transport;
- courier;
- tug;
- salvage vessel;
- mining vessel;
- survey ship;
- scientific vessel;
- medical vessel;
- rescue vessel;
- colony transport;
- diplomatic vessel;
- patrol vessel;
- customs/security vessel;
- training vessel;
- shuttle / runabout / utility craft;
- private civilian vessel;
- trader;
- smuggler/criminal craft when context supports it;
- military scout;
- escort;
- destroyer/frigate analogue;
- cruiser;
- capital/command vessel;
- specialist faction-specific roles.

Generated ships must derive from operator/civilization technology and purpose, not merely receive a faction skin.

## Domain 4 — Facilities and infrastructure

Possible generated infrastructure includes:

- starbases;
- outposts;
- communications relays;
- sensor arrays;
- shipyards;
- repair docks;
- depots;
- fueling/resource facilities;
- mining stations;
- research stations;
- medical facilities;
- colonies;
- orbital habitats;
- trade hubs;
- customs posts;
- defense installations;
- prisons/detention facilities;
- listening posts;
- agricultural/industrial installations;
- civilian ports.

Infrastructure should create believable reasons for traffic.

A mining complex may imply ore transport, worker movement, maintenance and supply traffic.

## Domain 5 — Traffic and logistics

Local traffic is generated from needs and routes, not random decorative spawn.

Possible causes:

- cargo demand;
- passenger movement;
- patrol assignment;
- research mission;
- diplomatic mission;
- medical transfer;
- repair;
- resupply;
- mining output;
- colonization;
- exploration;
- military deployment;
- emergency response.

Traffic state should include origin, destination, purpose, schedule/ETA and current status when appropriate.

## Domain 6 — Crews and populations

Generated ships/facilities require plausible populations.

Population generation proceeds from organizational need:

```text
ENTITY ROLE
  ↓
ORGANIZATION / OPERATOR
  ↓
DEPARTMENTS / FUNCTIONS
  ↓
POSITIONS
  ↓
SHIFTS
  ↓
QUALIFICATION NEEDS
  ↓
CHARACTERS
```

Generated NPCs must respect:

- date;
- location;
- faction/operator;
- rank/role;
- qualifications;
- species/culture context;
- language;
- name profiles;
- staffing constraints.

Species never determines individual personality.

## Domain 7 — Current activity

An entity must not merely exist. It should have a plausible current activity.

Examples:

- transporting supplies;
- surveying a moon;
- waiting for docking clearance;
- conducting repairs;
- following a patrol route;
- performing stellar research;
- responding to distress;
- carrying passengers;
- escorting a convoy;
- conducting diplomacy;
- undergoing refit;
- searching for a missing ship.

Purpose drives behavior and creates mission opportunities.

## Domain 8 — Campaign-conditioned generation

Generation is constrained by live history.

```text
CANON STARTING STATE
+
CAMPAIGN EVENTS
+
ERA
+
REGION
+
POLITICS
+
TECHNOLOGY
+
SEED
→ VALID GENERATION
```

If a war starts, traffic and military presence may change.

If a station is destroyed, later generation must not casually restore it.

If a system has been explored, it remains explored unless knowledge is lost for an explicit reason.

## Canon reservation

Canonical systems, ships, characters, facilities and historical anchors reserve their identity/time-space slot.

Procedural generation must not:

- overwrite them;
- create accidental duplicates;
- contradict known presence;
- use a famous identity for a generated entity.

## Persistence

Once materialized, an entity is persistent.

The generator does not reroll it because the player leaves and returns.

Future state changes occur through simulation/events.

## Simulation LOD

Not all universe entities require the same update fidelity.

### High fidelity
- player ship;
- local contacts;
- current mission entities;
- nearby hazards;
- actively relevant NPCs.

### Medium fidelity
- ships/facilities in the local operational region;
- relevant traffic routes;
- linked mission/support entities.

### Low fidelity
- distant traffic;
- background populations;
- distant facilities;
- entities without immediate player interaction.

LOD changes simulation cost, not canonical existence.

## Offline / catch-up simulation

When campaign time advances without direct player control, deterministic systems may resolve elapsed activity:

- travel progress;
- duty watches;
- repairs;
- traffic movement;
- routine population activity;
- scheduled events;
- resource changes.

Relevant results materialize as authoritative events with timestamps.

## Mission-generation relationship

Missions should preferentially select existing world entities and tensions.

A mission generator may create an explicit new entity only through an authorized generation event that becomes persistent.

It may not secretly spawn an answer when the player scans for it.

## AI relationship

AI may assist with:

- names;
- natural-language descriptions;
- dialogue;
- biographies;
- summaries.

Structured rules decide whether the entity can exist and materialize it.

Generated prose never overrides the underlying entity definition.

## Long-term target

The intended result is that a player can enter a system never manually authored by the project and still encounter a coherent combination of:

- celestial environment;
- civilization/infrastructure;
- local traffic;
- ships;
- crews;
- secondary NPCs;
- ongoing activity;
- observable history;

that appears to have existed before the player arrived.
