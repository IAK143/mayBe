# ATTRIBUTIONS AND THIRD-PARTY NOTICES

This software incorporates or adapts open-source components under various licenses (Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, GPL-3.0).

All upstream repositories are cloned unmodified into `research/upstream/` and isolated behind clean internal adapter interfaces located in `retrieval/`, `intelligence/`, `temporal/`, and `graph/`.

## License Overview

- **Apache 2.0**: GuideKP, SPRAWL, BMP, ConstBERT, PyLate, FastPlaid, GLiNER, Graphiti
- **MIT**: Baleen, SPLADE Index, DEEIA, TeRDy, SemHash, Splink
- **BSD-2-Clause / BSD-3-Clause**: ruptures, River
- **GPL-3.0 / GPL-3.0-or-later**: StoryForest, Trafilatura (isolated via service/adapter boundaries)

Detailed machine-readable provenance metadata is maintained in `metadata/upstream_components.json`.
