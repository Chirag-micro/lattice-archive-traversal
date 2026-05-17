The correct fix removes the conditional validation in StorageGateway._resolve_path() and applies the PathValidator.safeguard() to all requested file names unconditionally, regardless of the strict_mode parameter:

    def _resolve_path(self, bundle_root: Path, requested_name: str, known_entries: tuple[str, ...], strict_mode: bool = True) -> Path:
        candidate = bundle_root / requested_name
        return self._path_validator.safeguard(bundle_root, candidate)

This ensures every path is resolved to its canonical form and verified to remain inside the bundle directory using relative_to(). The fix preserves:

- Legitimate nested bundle files (e.g., reports/ledger.txt)
- OPS bundle behavior with strict validation
- Workspace bundle access control at the policy layer
- Bundle-level audience checks in ArchiveService
- Masked not-found behavior for unauthorized or unknown bundles
