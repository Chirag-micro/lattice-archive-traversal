from pathlib import Path

from lattice_archive.errors import ArchiveNotFound
from lattice_archive.models import ResolvedBundle
from lattice_archive.repositories.bundle_store import BundleStore


class BundleResolutionService:
    def __init__(self, bundle_store: BundleStore, data_root: Path) -> None:
        self._bundle_store = bundle_store
        self._data_root = data_root

    def resolve(self, code: str) -> ResolvedBundle:
        bundle = self._bundle_store.get(code)
        if bundle is None:
            raise ArchiveNotFound("archive not found")
        return ResolvedBundle(
            code=bundle.code,
            workspace_id=bundle.workspace_id,
            root_path=self._data_root / bundle.workspace_id / bundle.relative_root,
            entries=bundle.entries,
            audience=bundle.audience,
        )
