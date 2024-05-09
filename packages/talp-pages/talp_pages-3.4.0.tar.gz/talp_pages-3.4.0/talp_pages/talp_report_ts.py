#!/usr/bin/env python

import argparse
import json
import pandas as pd
import os
import logging
import sqlite3
from datetime import datetime

from .talp_common import TALP_DB_COLUMN_METADATA, TALP_DB_COLUMN_TALP_OUPUT, TALP_DB_COLUMN_TIMESTAMP, TALP_DEFAULT_REGION_NAME, TALP_TABLE_NAME, TALP_TEMPLATE_PATH, TALP_POP_METRICS_KEY, date_time_to_string, render_template


class TalpTimeSeriesReport:
    def __init__(self, databases_file):
        # Now directly try to create a connection
        conn = sqlite3.connect(databases_file)

        # and read the contents
        self.df = pd.read_sql(f"SELECT * FROM {TALP_TABLE_NAME}", conn)
        logging.debug(
            f"Created TalpTimeSeries with and instantiated the df: {self.df}")

    def _extract_region_names_from_df(self):
        region_names = set()
        talp_outputs = self.df[TALP_DB_COLUMN_TALP_OUPUT].tolist()
        for talp_output in talp_outputs:
            raw_data = json.loads(talp_output)
            for entry in raw_data[TALP_POP_METRICS_KEY]:
                region_names.add(entry['name'])
        return list(region_names)

    def _get_formatted_timestamps(self):
        timestamps_df = self.df[TALP_DB_COLUMN_TIMESTAMP].tolist()
        timestamps = []
        for timestamp in timestamps_df:
            parsed_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            formatted_date = date_time_to_string(parsed_date)
            timestamps.append(formatted_date)
        return timestamps

    def _extract_metadata_from_df(self):
        metadata_obj = {}
        timestamps = self._get_formatted_timestamps()
        metadatas = self.df[TALP_DB_COLUMN_METADATA].tolist()

        for timestamp, metadata in zip(timestamps, metadatas):
            metadata_obj[timestamp] = json.loads(metadata)
            metadata_obj[timestamp]['date'] = timestamp

        return metadata_obj

    @staticmethod
    def _pack_series_data(name, data):
        return {
            'name': name,
            'type': 'line',
            'data': data}

    def _extract_dataseries(self, metric):
        timestamps = self._get_formatted_timestamps()
        regions = self._extract_region_names_from_df()
        talp_outputs = self.df[TALP_DB_COLUMN_TALP_OUPUT].tolist()
        series = []

        for region in regions:
            data = []
            for talp_output in talp_outputs:
                raw_data = json.loads(talp_output)
                for entry in raw_data[TALP_POP_METRICS_KEY]:
                    if entry['name'] == region:
                        try:
                            data.append(entry[metric])
                        except:
                            data.append(None)
                            logging.debug(
                                "WHOOPS not every timestamp has a data point, appending none")
            if len(timestamps) != len(data):
                logging.critical(
                    "Apparently not every timestamp has a data point!")
            series.append(self._pack_series_data(region, data))
        return series

    def get_html(self):
        # Render the template with the data
        region_names = self._extract_region_names_from_df()
        metadata = self._extract_metadata_from_df()
        pe_series = self._extract_dataseries('parallelEfficiency')
        et_series = self._extract_dataseries('elapsedTime')
        ipc_series = self._extract_dataseries('averageIPC')
        timestamps = self._get_formatted_timestamps()
        return render_template(TALP_TEMPLATE_PATH, 'talp_time_series.jinja',
                               timestamps=timestamps,
                               region_names=region_names,
                               metadata=metadata,
                               pe_series=pe_series,
                               et_series=et_series,
                               ipc_series=ipc_series,
                               default_region_name=TALP_DEFAULT_REGION_NAME)


def _validate_inputs(args):
    output_file = None
    input_file = None

    # Check if the SQLITE file exists
    if not os.path.exists(args.input):
        logging.error(
            f"The specified SQLITE file '{args.input}' does not exist.")
        raise Exception("Not existing input file")
    else:
        input_file = args.input

    # Set output
    if args.output:
        output_file = args.output
        if not args.output.endswith('.html'):
            output_file += ".html"
            logging.info(f"Appending .html to '{args.output}'")
        # Check if the HTML file exists
        if os.path.exists(args.output):
            logging(f"Overwriting '{args.output}'")
    else:
        output_file = args.input.replace(".json", "")
        output_file += ".html"

    return output_file, input_file


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Render html summary of the historic TALP data in the provided talp database')
    parser.add_argument('-i', '--input', dest='input',
                        help='Path to the TALP.db file')
    parser.add_argument('-o', '--output', dest='output',
                        help='Name of the html file beeing generated. If not specified [input].html will be chosen', required=False)
    args = parser.parse_args()

    output_file, input_file = _validate_inputs(args)
    timeseries = TalpTimeSeriesReport(input_file)
    rendered_html = timeseries.get_html()

    # Save or display the rendered HTML as needed
    with open(output_file, 'w') as f:
        f.write(rendered_html)


if __name__ == "__main__":
    main()
