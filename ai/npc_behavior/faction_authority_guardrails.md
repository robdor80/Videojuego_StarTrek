# Faction and diplomacy AI guardrails

## Purpose

Faction data informs what an NPC may plausibly demand, know, fear, negotiate or enforce. It does not replace individual personality or Core-owned political state.

## Required behavior

- Resolve species, citizenship, faction membership and office independently.
- Check date and live campaign relation state before describing another faction as enemy, ally or neutral.
- Check actual authority before allowing an NPC to bind a government, fleet, house, station or commercial body.
- Keep covert intent, infiltration and secret orders hidden unless knowledge state exposes them.
- Use local jurisdiction and treaty state when generating warnings, inspections, arrests, escorts or border demands.
- Treat official diplomatic change as a Core mutation, never a dialogue-side effect.

## Examples

### Klingon
A Klingon captain may invoke honor, house interests or Imperial orders, but those are separate state fields. The AI cannot invent a declaration of war because the captain is angry.

### Romulan
A Romulan officer may bluff or conceal intent, but the AI cannot reveal that bluff to the player unless evidence supports it. A cloaked ship is not automatically identified.

### Cardassian
Occupation history can shape Bajoran reactions, but a Cardassian NPC is not automatically guilty, loyal to the Union or hostile.

### Bajoran
Civil government, militia and religious authority are separate. A Vedek, Militia officer and minister do not share interchangeable authority.

### Ferengi
Commercial negotiation may use profit, contracts and regulation. The AI cannot assume every Ferengi is dishonest, wealthy, a trader or Alliance official.

### Borg
The AI may voice Collective communications but cannot resolve assimilation, adaptation or drone control. Those are Core mechanics.

### Dominion
Founders, Vorta and Jem'Hadar have different authority roles. Hidden Changeling identity is never exposed by narrator convenience.

## Authority boundary

AI may propose:
- demands;
- offers;
- warnings;
- threats;
- ceasefire terms;
- contracts;
- interpretations of known treaties.

Core validates:
- whether the speaker has authority;
- whether terms are legal/possible;
- whether a treaty or war state changes;
- whether borders open/close;
- whether forces comply;
- what becomes persistent World State.
