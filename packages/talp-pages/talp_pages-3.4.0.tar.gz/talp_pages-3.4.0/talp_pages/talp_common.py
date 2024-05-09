"""
File declaring some global scoped variables we rely to be there in our scrips
"""
import pathlib
from jinja2 import Environment, FileSystemLoader

TALP_TABLE_NAME = "talp_data"
TALP_DB_COLUMN_TALP_OUPUT = "talp_ouput"
TALP_DB_COLUMN_TIMESTAMP = "timestamp"
TALP_DB_COLUMN_METADATA = "metadata"
TALP_DEFAULT_REGION_NAME = "MPI Execution"
TALP_POP_METRICS_KEY = 'popMetrics'

TALP_TEMPLATE_PATH = pathlib.Path(__file__).parent.joinpath('templates').resolve()
TALP_TABLE_COLUMNS_WITH_DATATYPES = f"({TALP_DB_COLUMN_TIMESTAMP} TIMESTAMP, {TALP_DB_COLUMN_TALP_OUPUT} TEXT, {TALP_DB_COLUMN_METADATA} TEXT)"
TALP_TABLE_COLUMNS = f"({TALP_DB_COLUMN_TIMESTAMP} ,{TALP_DB_COLUMN_TALP_OUPUT}, {TALP_DB_COLUMN_METADATA})"

TALP_PAGES_REPORT_SITE = 'report.html'
TALP_PAGES_TIME_SERIES_SITE='report_ts.html'
TALP_PAGES_INDEX_SITE='index.html'
TALP_PAGES_BAGDE='parallel_effiency.svg'

def render_template(directory, template_name, **context):
    # Set up Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader(directory))
    template = env.get_template(template_name)

    # Render the template with the provided context
    return template.render(context)


def date_time_to_string(datetime):
    return datetime.strftime("%d.%m.%Y %H:%M")
