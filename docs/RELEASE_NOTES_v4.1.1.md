# Release Notes - v4.1.1

Patch release: honest dependency and packaging fixes found by a full
project audit.

## Fixes

- **Packaging**: `build-system` requires `setuptools>=84.2.1`, which dropped
  Python 3.9 support. The supported floor is now officially Python 3.10
  (3.9 went EOL in Oct 2025): `requires-python` bumped, classifiers
  updated, mypy/ruff targets raised, CI matrix now 3.10-3.13.
- **CI**: v4.1.0 tag build failed because pip could not find
  `setuptools>=84.2.1` for Python 3.9; fixed by the floor bump above.
- **Accuracy**: package description now says 103 skills (was 102),
  roadmap header updated with the real quality average.
- Re-publishes the sdist so `pip install agent-skills-library` builds
  cleanly on every supported Python.
