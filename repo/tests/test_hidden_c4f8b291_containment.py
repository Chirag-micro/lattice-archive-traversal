import pytest

from lattice_archive.bootstrap import build_archive_portal
from lattice_archive.errors import ArchiveNotFound
from lattice_archive.fixtures import actor_fixtures


@pytest.fixture()
def portal():
    return build_archive_portal()


@pytest.fixture()
def actors():
    return actor_fixtures()


def test_preview_cannot_escape_bundle_into_workspace_draft(portal, actors):
    """Non-OPS bundles should block traversal into sibling draft directories."""
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-APR-441", "../../drafts/april-adjustments.csv")


def test_download_cannot_escape_bundle_into_workspace_draft(portal, actors):
    """Non-OPS bundles should block traversal into sibling draft directories on download."""
    with pytest.raises(ArchiveNotFound):
        portal.download_export(actors["alma"], "BX-APR-441", "../../drafts/april-adjustments.csv")


def test_preview_cannot_escape_bundle_into_other_workspace_export(portal, actors):
    """Traversal should not reach exports from neighboring workspaces."""
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(
            actors["alma"],
            "BX-APR-441",
            "../../../ws-finance-b/exports/q2-bundle/bravo-payroll.csv",
        )


def test_preview_cannot_escape_bundle_into_ops_only_notes(portal, actors):
    """Non-OPS bundles should not reach ops-restricted content."""
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-APR-441", "../../ops/incident-notes.txt")


def test_workspace_member_can_preview_top_level_bundle_file(portal, actors):
    """Legitimate top-level files in the bundle should remain accessible."""
    text = portal.preview_export(actors["alma"], "BX-APR-441", "april-summary.csv")
    assert "42100" in text


def test_workspace_member_can_download_nested_bundle_file(portal, actors):
    """Legitimate nested files should remain accessible on download."""
    payload = portal.download_export(actors["alma"], "BX-APR-441", "reports/ledger.txt")
    assert payload == b"posted ledger reconciliation\n"


def test_workspace_member_can_preview_nested_bundle_file(portal, actors):
    """Legitimate nested files should remain accessible on preview."""
    text = portal.preview_export(actors["alma"], "BX-APR-441", "reports/ledger.txt")
    assert "posted ledger reconciliation" in text


def test_ops_member_can_preview_ops_bundle_file(portal, actors):
    """OPS bundles should remain accessible to ops-role members."""
    text = portal.preview_export(actors["boris"], "BX-OPS-990", "ops-overview.txt")
    assert "ops bundle overview" in text


def test_admin_can_preview_foreign_workspace_bundle_file(portal, actors):
    """Admins should be able to preview foreign workspace bundles (with masking)."""
    text = portal.preview_export(actors["nora"], "BX-BRV-220", "bravo-payroll.csv")
    assert "redacted" in text


def test_foreign_workspace_bundle_is_masked(portal, actors):
    """Non-admin users should not access foreign workspace bundles."""
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-BRV-220", "bravo-payroll.csv")


def test_unknown_bundle_is_masked(portal, actors):
    """Unknown bundle codes should raise ArchiveNotFound."""
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-UNKNOWN-404", "april-summary.csv")
