import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from lattice_archive.bootstrap import build_archive_portal
from lattice_archive.errors import ArchiveNotFound
from lattice_archive.fixtures import actor_fixtures


@pytest.fixture()
def portal():
    return build_archive_portal()


@pytest.fixture()
def actors():
    return actor_fixtures()


def test_workspace_member_can_preview_top_level_export_file(portal, actors):
    text = portal.preview_export(actors["alma"], "BX-APR-441", "april-summary.csv")
    assert "42100" in text


def test_workspace_member_can_download_nested_export_file(portal, actors):
    payload = portal.download_export(actors["alma"], "BX-APR-441", "reports/ledger.txt")
    assert payload == b"posted ledger reconciliation\n"


def test_ops_member_can_preview_ops_bundle_file(portal, actors):
    text = portal.preview_export(actors["boris"], "BX-OPS-990", "ops-overview.txt")
    assert "ops bundle overview" in text


def test_foreign_workspace_bundle_is_masked(portal, actors):
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-BRV-220", "bravo-payroll.csv")


def test_unknown_bundle_is_masked(portal, actors):
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-UNKNOWN-404", "april-summary.csv")
