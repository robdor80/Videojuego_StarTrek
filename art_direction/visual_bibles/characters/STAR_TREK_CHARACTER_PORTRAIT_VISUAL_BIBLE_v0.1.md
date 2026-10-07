# STAR TREK — CHARACTER PORTRAIT VISUAL BIBLE v0.1

**Status:** FOUNDATION APPROVED FOR PROCEDURAL TESTING  
**Type:** Category Visual Bible — Character Portrait  
**Version:** 0.1  
**Inherits:** STAR_TREK_GLOBAL_VISUAL_BIBLE_v0.1

---

## 1. Purpose

Defines the reusable portrait language for persistent and generic Star Trek characters.

A portrait represents **the person**, not a complete narrative scene.

It must allow identity recognition across:
- years;
- uniform changes;
- promotions;
- transfers;
- injuries;
- aging;
- different locations and lighting.

---

## 2. Standard output

Default orientation: vertical.  
Default aspect ratio: **4:5**.

Default framing:
- head complete;
- shoulders;
- upper torso;
- enough clothing/insignia to communicate institutional context where relevant.

Alternative framing requires category/use justification.

---

## 3. Camera

Preferred:
- eye-level or near eye-level;
- frontal or mild three-quarter;
- portrait-lens perspective without fashion-photo exaggeration.

Avoid as default:
- extreme low/high angle;
- fisheye distortion;
- profile-only identification;
- cinematic action pose.

---

## 4. Expression

Base portraits favor reusable states:
- neutral;
- attentive;
- calm;
- reserved;
- mildly warm;
- serious;
- tired where contextually valid.

Strong emotion belongs to scene/state variants, not the base identity portrait.

---

## 5. Persistent facial identity

The visual identity record must preserve stable recognition anchors such as:
- skull/face proportions;
- jaw/chin;
- nose;
- eyes and spacing;
- brows;
- ears where relevant;
- species cranial/facial structures;
- characteristic skin color/texture;
- persistent markings/scars;
- body/neck proportions visible in portrait.

Later images may evolve these through:
- age;
- weight;
- persistent injury;
- surgery/prosthetics;
- species lifecycle;
- explicit transformative events.

They may not replace them with a new unrelated face.

---

## 6. Species morphology

Species profiles override human assumptions.

Species traits must be:
- anatomically integrated;
- consistent across views;
- individually varied where canon allows;
- preserved across the same character's images.

Do not paste a species “feature” onto an otherwise random human face without anatomical integration.

---

## 7. Age

Chronological age is interpreted through the character's species/lifecycle profile.

Aging may affect:
- skin;
- hair;
- soft tissue;
- posture;
- facial volume;
- species-specific traits.

Do not model every species using human aging speed or visual cues.

A later portrait must read as the **same individual later**, not a replacement.

---

## 8. Hair and grooming

Hair/grooming can be temporary or semi-persistent style state.

It may change with:
- era;
- personal choice;
- duty standards;
- culture;
- field conditions;
- elapsed time.

Hair changes do not authorize face changes.

---

## 9. Uniform and clothing

Portrait context resolves:
- organization;
- era;
- division;
- rank;
- duty/off-duty;
- special equipment;
- current condition.

Uniform is a layer over identity.

Do not bake one uniform permanently into a character's visual identity.

---

## 10. Rank and insignia

If visible:
- rank must match authoritative character state;
- insignia must match project visual rule/profile;
- division color/function must match organization and era profile.

Malformed or inconsistent insignia is a rejection reason.

---

## 11. Background

Default: contextual, restrained, softly readable.

Possible contexts:
- ship interior;
- station;
- Academy;
- office;
- laboratory;
- engineering;
- sickbay;
- planetary environment;
- neutral profile environment.

Background may establish context but must not invent:
- a specific location not assigned;
- unauthorized technology;
- unseen events;
- extra personnel with implied relationships.

---

## 12. Lighting

Prioritize:
- facial readability;
- natural volume;
- species-relevant skin/material response;
- believable environmental source.

Avoid automatic:
- heroic rim light;
- colored sci-fi glow;
- emergency red light;
- holographic spill.

Those require actual state/context.

---

## 13. Skin and biological surface

Human/humanoid skin:
- real texture;
- pores/variation;
- age and health cues where visible;
- no plastic smoothing.

Non-human surfaces:
- follow species morphology/material profile;
- preserve biological plausibility and continuity;
- avoid cosmetic “monster makeup” exaggeration beyond profile.

---

## 14. State overlays

Temporary overlays may include:
- fatigue;
- recent injury;
- medical treatment;
- dirt;
- sweat;
- environmental exposure;
- contamination;
- wetness;
- emergency gear.

Each overlay requires current-state cause.

The base identity asset should avoid extreme temporary state unless explicitly requested.

---

## 15. Diversity

Character pools should vary deliberately in:
- facial structure;
- body frame;
- age;
- grooming;
- attractiveness;
- skin/surface details;
- individual species morphology within allowed bounds.

Goal:

> People from the same species/organization should look like different individuals in the same world, not variations of one generated face.

---

## 16. Canonical vs procedural characters

Canonical characters:
- must use validated identity/reference policy;
- may not be approximated by a random procedural face.

Procedural persistent characters:
- receive stable visual_identity_id;
- once approved, future imagery derives from that identity.

Latent background population may remain aggregate/unmaterialized until needed.

---

## 17. Prompt composition

Recommended composition order:

`GLOBAL → ERA → CHARACTER PORTRAIT → SPECIES → CULTURE → AFFILIATION/ORGANIZATION → UNIFORM/ROLE/RANK → INDIVIDUAL VISUAL IDENTITY → CURRENT STATE → LOCATION/LIGHTING → CAMERA → OUTPUT`

No lower profile may overwrite an authoritative higher-level identity fact.

---

## 18. Rejection criteria

Reject:
- face drift;
- wrong species anatomy;
- wrong era;
- wrong uniform/division/rank;
- generic beauty homogenization;
- unsupported accessories;
- duplicate face from another persistent character;
- uncaused injury/dirt;
- malformed hands/ears/antennae/forehead structures visible in portrait;
- invented symbols/text;
- background that contradicts assignment/location.

