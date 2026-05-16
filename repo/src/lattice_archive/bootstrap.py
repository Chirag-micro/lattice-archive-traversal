from pathlib import Path

from lattice_archive.api.endpoints import ArchiveEndpoints
from lattice_archive.policies.bundle_access import BundleAccessPolicy
from lattice_archive.repositories.bundle_store import BundleStore
from lattice_archive.services.archive_service import ArchiveService
from lattice_archive.services.bundle_resolution import BundleResolutionService
from lattice_archive.services.storage_gateway import StorageGateway


def build_archive_portal() -> ArchiveEndpoints:
    repo_root = Path(__file__).resolve().parents[2]
    data_root = repo_root / "data" / "workspaces"
    bundle_store = BundleStore()
    policy = BundleAccessPolicy()
    resolver = BundleResolutionService(bundle_store, data_root)
    storage = StorageGateway()
    service = ArchiveService(resolver, policy, storage)
    return ArchiveEndpoints(service)
