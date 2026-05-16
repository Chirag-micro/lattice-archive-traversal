from lattice_archive.models import Actor
from lattice_archive.services.archive_service import ArchiveService


class ArchiveEndpoints:
    def __init__(self, service: ArchiveService) -> None:
        self._service = service

    def preview_export(self, actor: Actor, code: str, requested_name: str) -> str:
        return self._service.preview_bundle_file(actor, code, requested_name)

    def download_export(self, actor: Actor, code: str, requested_name: str) -> bytes:
        return self._service.download_bundle_file(actor, code, requested_name)
