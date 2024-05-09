#!/usr/bin/env python

import argparse
import os
import logging

from .talp_common import TALP_PAGES_INDEX_SITE, TALP_PAGES_REPORT_SITE, TALP_PAGES_TIME_SERIES_SITE, TALP_PAGES_BAGDE, render_template, TALP_TEMPLATE_PATH
from .talp_badge import TalpBadge
from .talp_report import TalpReport
from .talp_report_ts import TalpTimeSeriesReport

class TalpIndexPage:
    def __init__(self,report,report_ts,badge):
        self.report=report
        self.report_ts=report_ts
        self.badge = badge

    
    def get_html(self):
        return render_template(
            TALP_TEMPLATE_PATH,
            'talp_index_page.jinja',
            report=self.report,
            report_ts=self.report_ts,
            badge=self.badge,
        )










def _verify_input(args):
    json_file = None
    db_file = None
    prefix = None

    # Check if the JSON file exists
    if not os.path.exists(args.json_input):
        logging.error(
            f"The specified JSON file '{args.json_input}' does not exist.")
        raise Exception("Not existing input file")
    else:
        json_file = args.json_input

    # Check if the SQLITE file exists
    if not os.path.exists(args.db_input):
        logging.error(
            f"The specified SQLITE file '{args.db_input}' does not exist.")
        raise Exception("Not existing input file")
    else:
        db_file = args.db_input


    prefix = args.prefix

    return json_file,db_file,prefix

def main():

    def _add_prefix(pref,inp)->str:
        if pref:
            return pref + "_" + inp
        else:
            return inp

    # Creating the main argument parser
    parser = argparse.ArgumentParser(description='Render the complete static html pages including a index page.' )
    # Adding argument for JSON file
    parser.add_argument('-j', '--json', dest='json_input', help='Path to the TALP JSON file')
    # Adding argument for DB file
    parser.add_argument('-d', '--db', dest='db_input', help='Path to the TALP.db file')
    # Adding argument for prefix
    parser.add_argument('-p', '--prefix', dest='prefix', help=f"Prefix used in front of the (_){TALP_PAGES_REPORT_SITE}, (_){TALP_PAGES_TIME_SERIES_SITE} and (_){TALP_PAGES_INDEX_SITE}", required=False)

    # Parsing arguments
    args = parser.parse_args()

    json_file,db_file,prefix = _verify_input(args)

    ouput_report_ts=_add_prefix(prefix,TALP_PAGES_TIME_SERIES_SITE)
    ouput_report=_add_prefix(prefix,TALP_PAGES_REPORT_SITE)
    badge_file=_add_prefix(prefix,TALP_PAGES_BAGDE)
    ouput_index=_add_prefix(prefix,TALP_PAGES_INDEX_SITE)

    index = TalpIndexPage(ouput_report,ouput_report_ts,badge_file)
    report_ts= TalpTimeSeriesReport(db_file)    
    report = TalpReport(json_file)
    bagde = TalpBadge(json_file)
 
    with open(ouput_index, 'w') as f:
        f.write(index.get_html())

    with open(ouput_report_ts, 'w') as f:
        f.write(report_ts.get_html())

    with open(ouput_report, 'w') as f:
        f.write(report.get_html())
    
    with open(badge_file, 'wb') as f:
        f.write(bagde.get_badge_svg())
    
    
    
