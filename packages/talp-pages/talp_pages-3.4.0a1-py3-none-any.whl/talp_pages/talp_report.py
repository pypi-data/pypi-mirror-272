#!/usr/bin/env python

import argparse
import json
import os
from urllib.request import urlopen, Request
import logging
from .talp_common import TALP_TEMPLATE_PATH,render_template,TALP_POP_METRICS_KEY,TalpRelativeLinks

class TalpReport:
    def __init__(self, talp_file):
        # Now directly try to create a connection
        with open(talp_file, 'r') as json_file:
            # dont catch exception, but fail
            self.raw_data = json.load(json_file)
        
        logging.debug(f"Created TalpReport and read the json: {self.raw_data}")
        # do some sanity checks
        if not self.raw_data[TALP_POP_METRICS_KEY]:
            logging.error(f"No {TALP_POP_METRICS_KEY} found in {talp_file}. Try re-running DLB with arguments --talp --talp-summary=pop-metrics --talp-file={talp_file}")
            raise Exception(f"No {TALP_POP_METRICS_KEY} found")


    def get_html(self,links: TalpRelativeLinks):
        pop_metric_regions = self.raw_data[TALP_POP_METRICS_KEY]
        # Render the template with the data
        return render_template(
            TALP_TEMPLATE_PATH, 'talp_report.jinja', regions=pop_metric_regions,links=vars(links))



def _validate_inputs(args):
    output_file=None
    input_file=None
    # Check if the JSON file exists
    if not os.path.exists(args.input):
        raise Exception(
            f"Error: The specified JSON file '{args.json_file}' does not exist.")
    else:
        input_file= args.input


    # Set output
    if args.output:
        output_file = args.output
        if not args.output.endswith('.html'):
            output_file += ".html"
            logging.info(f"Appending .html to '{args.output}'")
        # Check if the HTML file exists
        if os.path.exists(args.output):
            logging.info(f"Overwriting '{args.output}'")
    else:
        output_file = args.input.replace(".json", "")
        output_file += ".html"

    return output_file,input_file

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Render HTML Table summary of the talp.json')
    parser.add_argument('-i', '--input', dest='input', help='Path to the TALP JSON file')
    parser.add_argument('-o', '--output', dest='output',
                        help='Name of the html file beeing generated. If not specified [input].html will be chosen', required=False)
   
    # Parsing arguments
    try:
        args = parser.parse_args()
        output_file, input_file = _validate_inputs(args)
    except Exception as e:
        logging.error(f"When parsing arguments ecountered the following error: {e}")
        parser.print_help()
        exit(1)

    links=TalpRelativeLinks(output_file,output_file,output_file)
    report = TalpReport(input_file)
    rendered_html = report.get_html(links)
    with open(output_file, 'w') as f:
        f.write(rendered_html)



if __name__ == "__main__":
    main()
