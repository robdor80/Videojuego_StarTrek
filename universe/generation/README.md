# Procedural universe generation

This directory contains the authoritative procedural-world contracts used by gameplay systems.

## Purpose

Procedural generation creates persistent world entities that can later be observed and affected by gameplay systems. It does not create ad-hoc answers for UI prompts.

Current implementation order:

1. observable entity model;
2. detectable-signature model;
3. generation rules;
4. minimal v0.0.1 generation profile;
5. deterministic generator implementation;
6. sensor-resolution model.

## Core rule

**Generate reality first. Observe it second.**

Sensor consoles, tricorders, science analysis and NPC reports consume the generated world state. They never become the source of truth themselves.
