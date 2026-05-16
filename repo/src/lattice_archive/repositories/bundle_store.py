from lattice_archive.models import ArchiveBundle


class BundleStore:
    def __init__(self) -> None:
        self._bundles = {
            "BX-APR-441": ArchiveBundle(
                code="BX-APR-441",
                workspace_id="ws-finance-a",
                relative_root="exports/q2-bundle",
                entries=("april-summary.csv", "reports/ledger.txt"),
                audience="workspace",
            ),
            "BX-OPS-990": ArchiveBundle(
                code="BX-OPS-990",
                workspace_id="ws-finance-a",
                relative_root="exports/ops-bundle",
                entries=("ops-overview.txt",),
                audience="ops",
            ),
            "BX-BRV-220": ArchiveBundle(
                code="BX-BRV-220",
                workspace_id="ws-finance-b",
                relative_root="exports/q2-bundle",
                entries=("bravo-payroll.csv",),
                audience="workspace",
            ),
        }

    def get(self, code: str) -> ArchiveBundle | None:
        return self._bundles.get(code)
