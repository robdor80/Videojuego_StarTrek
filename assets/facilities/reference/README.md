# Facility reference assets

This directory is reserved for station, starbase, shipyard, outpost and other facility reference material that has been reviewed for use by the Star Trek universe pack.

## Important separation

```text
DOWNLOADED REFERENCE
        ≠
CANON FACT
        ≠
GAMEPLAY MODEL
```

A downloaded sheet may be valuable for:
- spatial layout;
- docking geometry;
- service locations;
- internal topology;
- section/deck organization;
- gameplay location graphs.

It does **not** automatically validate every label, dimension, capacity or technical claim printed on the image.

## Expected workflow

```text
BlueprintGrabber/local download
        ↓
human/project review
        ↓
source registry entry
        ↓
copy selected set into this repository
        ↓
reference-set metadata
        ↓
extract only supported gameplay data
        ↓
validation
```

## Suggested layout

```text
assets/facilities/reference/
└── <faction>/
    └── <facility_or_design>/
        └── <reference_set_id>/
            ├── README.md
            ├── reference_index.json
            └── sheets/
                ├── 01.jpg
                ├── 02.jpg
                └── ...
```

Do not bulk-import every downloaded image automatically. Only reviewed material needed by the project should enter this repository.
