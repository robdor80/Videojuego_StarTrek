# Starfleet Personnel Model

Status: **APPROVED ARCHITECTURE**

The project models Starfleet personnel through independent fields:

```text
RANK
DIVISION
DEPARTMENT
POSITION
ASSIGNMENT
DUTY_STATION
```

## Meaning

- **Rank** — personal grade: Alférez, Teniente, Comandante, Capitán...
- **Division** — broad branch: Mando, Operaciones, Ciencias.
- **Department** — functional specialty: Ingeniería, Seguridad, Medicina...
- **Position** — current job: Primer Oficial, Jefe de Ingeniería...
- **Assignment** — organizational posting/destino: USS Enterprise-D, Deep Space 9, Academia...
- **Duty station** — physical/operational workstation during a shift: Conn, Tactical, Main Engineering, Sickbay...

A person may hold more than one position when canon or campaign state requires it.

This lets CoreRPG answer independently:
- who outranks whom,
- who commands whom,
- what a character is trained to do,
- what job they currently hold,
- where they are posted,
- where they should physically be during a shift.
