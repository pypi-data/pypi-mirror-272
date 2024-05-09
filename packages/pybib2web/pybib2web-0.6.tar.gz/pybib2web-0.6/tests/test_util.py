# This file is part of pybib2web, a translator of BibTeX to HTML.
# https://gitlab.com/sosy-lab/software/pybib2web
#
# SPDX-FileCopyrightText: 2021 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from pybib2web import util


def test_get_shortform_single_first_name():
    assert util.get_shortform("Dirk Beyer") == "D. Beyer"


def test_get_shortform_no_last_name():
    assert util.get_shortform("Niedner") == "Niedner"


def test_get_shortform_name_with_hyphen():
    assert util.get_shortform("Max-Erwin Mustermann") == "M.-E. Mustermann"


def test_get_shortform_name_with_firstname_apostrophe():
    # Not sure about the expected behavior, but let's stick with M'Erwin -> M'E.
    # until we have something better
    assert util.get_shortform("M'Erwin Mustermann") == "M'E. Mustermann"
    assert util.get_shortform("MC'Erwin Mustermann") == "MC'E. Mustermann"


def test_get_shortform_name_with_lastname_apostrophe():
    # Not sure about the expected behavior, but let's stick with M'Erwin -> M'E.
    # until we have something better
    assert util.get_shortform("Max M'Mustermann") == "M. M'Mustermann"


def test_get_shortform_single_first_name_texified():
    assert util.get_shortform("Dirk~Beyer") == "D. Beyer"


def test_get_shortform_first_names_with_space():
    first_names = ["Max", "Erwin"]
    last_name = "Mustermann"
    delimiters_between_first_names = [" ", "~"]
    delimiters_to_last_name = [" ", "~"]

    mutators_firsts = [
        lambda ns: [f"{n[0]}." for n in ns],
        lambda ns: ns,
    ]

    for delim_last in delimiters_to_last_name:
        for delim_firsts in delimiters_between_first_names:
            for mutator in mutators_firsts:
                name = (
                    f"{delim_firsts.join(mutator(first_names))}{delim_last}{last_name}"
                )
                assert util.get_shortform(name) == "M. E. Mustermann"

def test_get_download_link():
    assert util.get_download_link("10.1007/978-3-030-99527-0_20") == "https://link.springer.com/content/pdf/10.1007/978-3-030-99527-0_20.pdf"
    assert util.get_download_link("10.1145/3368089.3409718")      == "https://dl.acm.org/doi/pdf/10.1145/3368089.3409718"
    assert util.get_download_link("10.48550/arXiv.2107.08038")    == "https://arxiv.org/pdf/2107.08038"

