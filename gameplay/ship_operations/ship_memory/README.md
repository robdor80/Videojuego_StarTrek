# Ship memory — persistent contact dossiers

The ship maintains persistent records for observed contacts.

This is a shared knowledge layer, not a Sensors-only database. Sensors creates and updates sensor observations; Tactical, Science, Communications and Computer may append their own authorized findings.

## Principles

- Contact identity persists when evidence supports re-identification.
- Every fact keeps provenance, confidence and observation time.
- Losing a contact does not erase its record.
- Reacquiring a compatible contact may reopen the same dossier.
- Different systems may know different things about the same contact.
- The shared record must not leak authoritative world truth that has never been observed.

The Computer/Base de datos console can expose archival search and comparison; Sensors exposes the operational contact view.
