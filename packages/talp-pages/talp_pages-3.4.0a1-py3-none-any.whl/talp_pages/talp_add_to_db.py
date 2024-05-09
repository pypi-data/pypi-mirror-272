# myapp/app.py
import argparse
import json
import os

from datetime import datetime
import sqlite3
import logging
from .talp_common import TALP_TABLE_NAME, TALP_TABLE_COLUMNS_WITH_DATATYPES, TALP_TABLE_COLUMNS


# Function to insert data into the SQLite database
def insert_data(conn, timestamp, talp_output, metadata):
    # Connect to the SQLite database
    cursor = conn.cursor()

    try:
        # Create a table if it doesn't exist
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {TALP_TABLE_NAME} {TALP_TABLE_COLUMNS_WITH_DATATYPES}")

        # Create an index on the timestamp column
        cursor.execute(
            f"CREATE INDEX IF NOT EXISTS idx_timestamp ON {TALP_TABLE_NAME} (timestamp)")

        # Convert JSON objects to string format

        # Insert data into the table
        cursor.execute(f"INSERT INTO {TALP_TABLE_NAME} {TALP_TABLE_COLUMNS} VALUES (?, ?, ?)", (
            timestamp, json.dumps(talp_output), json.dumps(metadata)))

        # Commit changes and close the connection
        conn.commit()
        logging.debug("Data inserted successfully")
    except sqlite3.Error as e:
        logging.critical("ERROR inserting data:", e)
    finally:
        # Close the connection
        conn.close()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Add talp.json to the local time series database')
    parser.add_argument('-i', '--input', dest='talp',
                        help='talp.json file to be added', required=True)
    parser.add_argument('-m', '--metadata', dest='metadata',
                        help='metadata.json file to be added', required=False)
    parser.add_argument('-db', '--database', dest='database',
                        help='TALP.db file. If not specified a new one will be generated', required=False)
    # TODO add timestamp mechanism
    args = parser.parse_args()

    # Check if the JSON file exists
    if not os.path.exists(args.talp):
        logging.error(f"The specified JSON file '{args.talp}' does not exist.")
        return

    if args.metadata:
        if not os.path.exists(args.metadata):
            logging.error(
                f"The specified JSON file '{args.metadata}' does not exist.")
            return

    # Set output
    if args.database:
        DB_FILE = args.database
    else:
        DB_FILE = "TALP.db"

    # Connect to database
    conn = sqlite3.connect(DB_FILE)

    current_timestamp = datetime.now()

    with open(args.talp, 'r') as json_file:
        try:
            talp_output = json.load(json_file)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return
    if args.metadata:
        with open(args.metadata, 'r') as json_file:
            try:
                metadata = json.load(json_file)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                return
    else:
        metadata = {}

    insert_data(conn, current_timestamp, talp_output, metadata)


if __name__ == "__main__":
    main()
