from lattice_archive.errors import ArchiveNotFound
from lattice_archive.models import Actor
from lattice_archive.policies.bundle_access import BundleAccessPolicy
from lattice_archive.services.bundle_resolution import BundleResolutionService
from lattice_archive.services.storage_gateway import StorageGateway


class ArchiveService:
    def __init__(
        self,
        resolver: BundleResolutionService,
        policy: BundleAccessPolicy,
        storage: StorageGateway,
    ) -> None:
        self._resolver = resolver
        self._policy = policy
        self._storage = storage

    def preview_bundle_file(self, actor: Actor, code: str, requested_name: str) -> str:
        bundle = self._resolver.resolve(code)
        if not self._policy.can_access_bundle(actor, bundle):
            raise ArchiveNotFound("archive not found")
        known = bundle.entries if "OPS" in code else ()
        return self._storage.preview_text(bundle.root_path, requested_name, known)

    def download_bundle_file(self, actor: Actor, code: str, requested_name: str) -> bytes:
        bundle = self._resolver.resolve(code)
        if not self._policy.can_access_bundle(actor, bundle):
            raise ArchiveNotFound("archive not found")
        known = bundle.entries if "OPS" in code else ()
        return self._storage.download_bytes(bundle.root_path, requested_name, known)
