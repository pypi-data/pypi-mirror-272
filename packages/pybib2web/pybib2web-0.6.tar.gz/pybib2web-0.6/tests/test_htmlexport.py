# This file is part of pybib2web, a translator of BibTeX to HTML.
# https://gitlab.com/sosy-lab/software/pybib2web
#
# SPDX-FileCopyrightText: 2022 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from collections import namedtuple
from pybib2web import htmlexport, bibparser, config

BIB_TECHREPORT = "test/test-techreport.bib"
BIB_THESIS = "test/test-thesis.bib"

CONFIG = config.Config({}, namedtuple("Cmdline", ["create_single_page"])(False))


def test_publication_venue_to_html_techreport():
    for bibfile in (BIB_TECHREPORT, BIB_THESIS):
        check_export_succeeds(bibfile, CONFIG)


def check_export_succeeds(bibfile, config):
    db = bibparser.parse(bibfile, do_detex=False)

    html_result = [
        htmlexport.publication_venue_to_html(entry, config) for entry in db.entries
    ]

    assert all(html_result)
