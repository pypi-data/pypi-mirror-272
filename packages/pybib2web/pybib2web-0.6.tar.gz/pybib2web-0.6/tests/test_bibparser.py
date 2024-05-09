# This file is part of pybib2web, a translator of BibTeX to HTML.
# https://gitlab.com/sosy-lab/software/pybib2web
#
# SPDX-FileCopyrightText: 2021 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for bibparser"""

import itertools

from pybib2web import bibparser

BIB_FILE = "test/test1.bib"
BIB2_FILE = "test/test2.bib"

EXAMPLE_KEYS = ("TACAS21", "ISoLA20c", "WRTP00")
EXAMPLE_KEYS2 = (
    "ThomasSymbolicExecution",
    "AbdullaSARD",
    "KarlheinzDomainTypes",
)


def test_parse_single_file():
    db = bibparser.parse(BIB_FILE, do_detex=False)

    _check_all_exist(db, EXAMPLE_KEYS)


def test_parse_two_files():
    db = bibparser.parse(BIB_FILE, BIB2_FILE, do_detex=False)

    _check_all_exist(db, EXAMPLE_KEYS, EXAMPLE_KEYS2)


def test_parse_with_detexification():
    db = bibparser.parse(BIB_FILE, do_detex=True)

    _check_all_exist(db, EXAMPLE_KEYS)


def _check_all_exist(db, *keys):
    for expected_key in itertools.chain(*keys):
        assert any(
            e["ID"] == expected_key for e in db.entries
        ), f"Missing: {expected_key}"


def test_split_authors_space():
    assert bibparser._split_authors("Foo Bar and Lo Ipsum") == ["Foo Bar", "Lo Ipsum"]


def test_split_authors_newline():
    assert bibparser._split_authors("Foo Bar and\nLo Ipsum") == ["Foo Bar", "Lo Ipsum"]
    assert bibparser._split_authors("Foo Bar\nand Lo Ipsum") == ["Foo Bar", "Lo Ipsum"]
    assert bibparser._split_authors(
        "Dirk Beyer and Matthias Dangl and Daniel Dietsch and Matthias Heizmann and\n Andreas Stahlbauer"
    ) == [
        "Dirk Beyer",
        "Matthias Dangl",
        "Daniel Dietsch",
        "Matthias Heizmann",
        "Andreas Stahlbauer",
    ]
    assert bibparser._split_authors(
        "Dirk Beyer and Stefan Löwe and Evgeny Novikov and Andreas Stahlbauer and Philipp Wendler"
    ) == [
        "Dirk Beyer",
        "Stefan Löwe",
        "Evgeny Novikov",
        "Andreas Stahlbauer",
        "Philipp Wendler",
    ]
