#!/usr/bin/env python

import argparse
import os
import logging

from .talp_common import TALP_PAGES_INDEX_SITE, TALP_PAGES_REPORT_SITE, TALP_PAGES_TIME_SERIES_SITE, TALP_PAGES_BAGDE, render_template, TALP_TEMPLATE_PATH, TalpRelativeLinks
from .talp_badge import TalpBadge
from .talp_report import TalpReport
from .talp_report_ts import TalpTimeSeriesReport

class TalpIndexPage:

    
    def get_html(self,links:TalpRelativeLinks):
        return render_template(
            TALP_TEMPLATE_PATH,
            'talp_index_page.jinja',
            links=vars(links),
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
    try:
        args = parser.parse_args()
        json_file,db_file,prefix = _verify_input(args)
    except Exception as e:
        logging.error(f"When parsing arguments ecountered the following error: {e}")
        parser.print_help()
        exit(1)
    
    output_report_ts=_add_prefix(prefix,TALP_PAGES_TIME_SERIES_SITE)
    output_report=_add_prefix(prefix,TALP_PAGES_REPORT_SITE)
    badge_file=_add_prefix(prefix,TALP_PAGES_BAGDE)
    output_index=_add_prefix(prefix,TALP_PAGES_INDEX_SITE)
    links=TalpRelativeLinks(output_index,output_report,output_report_ts,render_navbar=True)
    index = TalpIndexPage()
    report_ts= TalpTimeSeriesReport(db_file)    
    report = TalpReport(json_file)
    bagde = TalpBadge(json_file)
 
    with open(output_index, 'w') as f:
        f.write(index.get_html(links))

    with open(output_report_ts, 'w') as f:
        f.write(report_ts.get_html(links))

    with open(output_report, 'w') as f:
        f.write(report.get_html(links))
    
    with open(badge_file, 'wb') as f:
        f.write(bagde.get_badge_svg())
    
    
    
