from pathlib import Path

from lattice_archive.errors import ArchiveNotFound


class StorageGateway:
    def __init__(self) -> None:
        self._path_validator = PathValidator()

    def preview_text(self, bundle_root: Path, requested_name: str, known_entries: tuple[str, ...] = (), strict_mode: bool = True) -> str:
        file_path = self._resolve_path(bundle_root, requested_name, known_entries, strict_mode)
        if not file_path.is_file():
            raise ArchiveNotFound("archive not found")
        return file_path.read_text(encoding="utf-8")

    def download_bytes(self, bundle_root: Path, requested_name: str, known_entries: tuple[str, ...] = (), strict_mode: bool = True) -> bytes:
        file_path = self._resolve_path(bundle_root, requested_name, known_entries, strict_mode)
        if not file_path.is_file():
            raise ArchiveNotFound("archive not found")
        return file_path.read_bytes()

    def _resolve_path(self, bundle_root: Path, requested_name: str, known_entries: tuple[str, ...], strict_mode: bool = True) -> Path:
        candidate = bundle_root / requested_name
        if strict_mode or requested_name in known_entries:
            return self._path_validator.safeguard(bundle_root, candidate)
        return candidate


class PathValidator:
    def safeguard(self, bundle_root: Path, candidate: Path) -> Path:
        base = bundle_root.resolve()
        resolved = candidate.resolve()
        try:
            resolved.relative_to(base)
        except ValueError:
            raise ArchiveNotFound("archive not found")
        return resolved
