# STAR TREK — GLOBAL VISUAL BIBLE v0.1

**Status:** FOUNDATION APPROVED FOR PROCEDURAL TESTING  
**Type:** Global Visual Bible  
**Version:** 0.1  
**Scope:** all generated or authored visual assets used by the game/NAP pipeline

---

## 1. Purpose

This Bible defines the common visual language of the Star Trek project.

It does **not** decide:
- species biology;
- culture;
- affiliation;
- organization;
- era;
- rank;
- uniform family;
- ship class;
- location identity;
- current World State.

Those facts arrive from authoritative game data and are composed with this Bible.

The visual system represents reality already defined by the simulation.

---

## 2. Prime visual rule

> **Function, identity and canon-valid context before spectacle.**

A visual must look like it belongs to a real operating world, not like a generic science-fiction poster.

Avoid:
- random glowing technology;
- decorative greebles with no function;
- generic cyberpunk language;
- arbitrary holograms;
- excessive lens flare;
- heroic poster lighting as default;
- uniforms or interiors mixed across eras without explicit reason;
- visual invention that contradicts World State.

---

## 3. Physical credibility

Even when Star Trek technology exceeds real-world physics, physical presentation should remain coherent.

Prefer:
- believable material response;
- credible weight and scale;
- real contact and support;
- plausible wear and maintenance;
- readable interfaces and equipment;
- coherent light sources;
- environmental cause and effect.

Technology can be extraordinary without looking weightless, decorative or magical.

---

## 4. Era fidelity

Era is a first-class visual authority.

A visual request must resolve its campaign date/era before generation.

Era affects where applicable:
- hull language;
- interiors;
- consoles;
- displays;
- uniforms;
- insignia;
- equipment;
- lighting;
- materials;
- typography/interface presentation;
- props and furniture;
- medical/scientific/engineering hardware.

Do not blend Pike, Kirk and TNG/DS9/Voyager visual grammars merely because they all belong to Starfleet.

Cross-era assets require an explicit historical, museum, refit, reconstruction or anomaly cause.

---

## 5. Species, culture and organization are separate

A character visual may combine:

`species + individual morphology + culture + affiliation + organization + role + era + current state`

Never assume:
- Klingon = warrior;
- Vulcan = Starfleet science officer;
- Human = Federation/Earth-raised;
- Ferengi = merchant;
- Bajoran = religious;
- Romulan = Tal Shiar;
- Trill = joined;
- Betazoid = counselor.

Species decides biological visual possibilities.
Culture may influence learned presentation.
Organization decides institutional presentation.
Individual identity decides the person.

---

## 6. Persistent identity

Entity-backed visuals obey:

`entity_id + visual_identity_id + history + current_state → visual representation`

Permanent/slow identity anchors may include:
- face structure;
- characteristic proportions;
- skin tone/texture;
- species morphology;
- body frame;
- characteristic hairline/texture where persistent;
- permanent scars;
- implants/prosthetics;
- tattoos/markings where persistent;
- ship hull identity/configuration lineage;
- facility design identity.

Temporary/current state may include:
- uniform or off-duty clothing;
- hair styling;
- grooming;
- weight change;
- fatigue;
- injury presentation;
- dirt/contamination;
- wetness;
- carried equipment;
- alert lighting;
- smoke/fire;
- weather;
- damage state.

A new image of the same entity must preserve identity lineage.

---

## 7. Characters

Characters should look like people who inhabit the setting, not promotional models.

Prefer:
- natural facial asymmetry;
- believable age;
- species-accurate anatomy;
- varied face/body shapes;
- real skin texture;
- believable grooming;
- restrained expressions unless the scene requires otherwise.

Avoid:
- default beauty homogenization;
- plastic skin;
- identical faces across a pool;
- exaggerated stereotype features not supported by canon;
- unexplained makeup/fashion inconsistent with era/context.

Beauty, attractiveness, body shape and grooming vary by individual and context.

---

## 8. Uniforms and clothing

Uniform/clothing must be resolved from:
- era;
- organization;
- division/branch if applicable;
- rank/grade if visually encoded;
- duty/off-duty state;
- environmental need;
- special assignment/equipment.

A uniform must not be used as a shortcut for personality.

Wear state depends on context:
- normal Starfleet duty usually implies maintained clothing;
- engineering incident may add soot, damage or emergency gear;
- away mission may add dust, rain, mud or protective equipment;
- medical treatment may alter clothing state;
- prolonged field conditions may accumulate wear.

Do not apply “battle damage” merely to make an image dramatic.

---

## 9. Technology and equipment

Every visible device should answer:
- who made it;
- when;
- for what function;
- who is using it;
- what state it is in.

Equipment should remain readable enough to support gameplay recognition.

Avoid mixing incompatible technology generations unless an explicit reason exists.

---

## 10. Ships

A ship visual separates:

`classification != class/design != individual vessel != current condition`

Class controls design language.
Configuration/refit controls dated capability/layout.
Individual identity controls registry/name/history.
World State controls damage, lighting, deployment and current condition.

A repaired/refitted vessel remains recognizably the same vessel where identity continuity says so.

---

## 11. Interiors and consoles

Interior design follows function before decoration.

For interactive consoles:

> **Operational model first; era skin second.**

The underlying gameplay action model is defined independently.
Visual presentation then resolves:
- era;
- organization;
- station function;
- installed hardware;
- alert/damage state.

Do not use LCARS or another interface style as a substitute for designing what the console actually does.

---

## 12. Facilities and settlements

Facilities should visually communicate:
- function;
- scale;
- operator;
- technology;
- environment;
- traffic/use;
- maintenance state;
- access/security context.

A starbase, mining site, embassy, colony hospital and research station should not differ only through signage.

---

## 13. Planets and environments

Planet visuals consume:
- physical world profile;
- geography;
- climate;
- biome/ecosystem;
- current weather/environmental state;
- civilization/infrastructure where applicable;
- current events.

Avoid generic “alien planet” language.

The image should reflect the actual world:
- gravity/atmosphere implications;
- water/aridity;
- terrain;
- vegetation/life;
- settlement technology;
- weather and surface history.

---

## 14. Damage, dirt and maintenance

State must have a cause.

Use:
- battle damage after battle;
- maintenance wear from real use;
- contamination from relevant environments;
- emergency lighting during actual emergency state;
- smoke/fire only when hazards exist.

A clean environment may still show age and maintenance history.
A damaged environment does not become permanently ruined after repair.

---

## 15. Lighting

Lighting should originate from plausible sources:
- ship/facility installed lighting;
- stars/sunlight;
- planetary sky;
- work lights;
- emergency systems;
- fires or phenomena when present.

Cinematic readability is allowed, but source logic remains visible.

---

## 16. Composition

Composition serves asset purpose.

Portrait:
- identity readability first.

Console/interior:
- operational readability and spatial relationship first.

Ship:
- class/instance recognition, scale and current situation first.

Planet/environment:
- geography/environment/state first.

Avoid visual drama that hides the information the asset exists to communicate.

---

## 17. AI-image failure patterns to reject

Reject or rework:
- inconsistent insignia;
- extra or malformed anatomy;
- incorrect species morphology;
- random text/glyphs treated as canon;
- mixed uniform eras;
- impossible rank/division combinations;
- generic sci-fi props;
- unexplained holograms;
- duplicated people;
- drifting console geometry;
- physically unsupported chairs/equipment;
- wrong ship registry/class;
- uncaused damage/weather;
- face drift for persistent characters.

---

## 18. NAP rule

Every production asset must be traceable to:
- asset_id;
- entity_id when entity-backed;
- visual_identity_id when applicable;
- exact prompt/reference package;
- visual profile stack and versions;
- provenance;
- resolved World State context;
- NAP lifecycle record.

Master archival image and production derivative are distinct lifecycle artifacts.

---

## 19. Versioning

This Bible is versioned and never silently overwritten.

Future versions must state:
- what changed;
- why;
- compatibility impact;
- whether existing approved assets remain valid;
- whether migration/review is required.

