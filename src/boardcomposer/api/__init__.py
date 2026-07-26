"""Public API packages for BoardComposer (EP-001).

Prefer the versioned submodule ``boardcomposer.api.v1``. Breaking changes
land in a new major package (``v2``), not by mutating ``v1`` in place.
"""

from boardcomposer.api import v1

__all__ = ["v1"]
