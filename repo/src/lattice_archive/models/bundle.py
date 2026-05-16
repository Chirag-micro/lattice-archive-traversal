from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArchiveBundle:
    code: str
    workspace_id: str
    relative_root: str
    entries: tuple[str, ...]
    audience: str


@dataclass(frozen=True)
class ResolvedBundle:
    code: str
    workspace_id: str
    root_path: Path
    entries: tuple[str, ...]
    audience: str
