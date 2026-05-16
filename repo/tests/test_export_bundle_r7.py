import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

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

# FAIL_TO_PASS Tests
def test_edge_case_empty_bundle(portal, actors):
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-EMPTY-000", "empty-bundle.csv")

def test_edge_case_large_bundle(portal, actors):
    with pytest.raises(ArchiveNotFound):
        portal.preview_export(actors["alma"], "BX-LARGE-999", "large-bundle.csv")

# PASS_TO_PASS Tests
def test_nested_bundle_with_special_characters(portal, actors):
    text = portal.preview_export(actors["alma"], "BX-SPC-777", "nested/special-@file$.csv")
    assert "special characters" in text