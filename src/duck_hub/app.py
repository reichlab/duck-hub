import time
from importlib import resources

import duckdb
import structlog
from rich import print

from duck_hub.util.db import get_db_connection

logger = structlog.get_logger()

# janky way to get a path to the db file
DATABASE_PATH = resources.files('duck_hub').parent.parent / 'data'
DATABASE_NAME = 'cdcepi-flusight-forecast-hub.db'
DATABASE_FILE = str(DATABASE_PATH / DATABASE_NAME)


def dataframes(data_location: str):
    """Try DuckDB with various dataframes."""

    logger.info('connecting to DuckDB database', db_file=data_location)

    with get_db_connection(data_location) as con:
        sql = 'SELECT model_id, count(*) AS total_submissions FROM model_output GROUP BY model_id;'

        print('Querying local, persistent DuckDB')
        start = time.process_time()
        mo_data = con.sql(sql)
        logger.info('executed DuckDB query', sql=sql, elapsed_time=time.process_time() - start)
        print(mo_data)

        print('DuckDB result as pandas dataframe: mo_data.to_db()\n')
        start = time.process_time()
        mo_data_df = mo_data.to_df()
        logger.info('converted DuckDB data to pandas', elapsed_time=time.process_time() - start)
        print(mo_data_df)

        print('DuckDb result as polars dataframe:  mo_data.pl()\n')
        start = time.process_time()
        mo_data_pl = mo_data.pl()
        logger.info('converted DuckDB data to polars', elapsed_time=time.process_time() - start)
        print(mo_data_pl)


def ibis(data_location: str):
    """How can Ibis work with all this?"""

    import ibis  # why??????
    con = ibis.duckdb.connect(data_location, read_only=True)
    print(f"Tables: {con.list_tables()}")
    mo = con.table('model_output')
    print(mo)
    print(f"Move to pandas: {mo.head().to_pandas()}")
    # in the terminal: ibis.options.interactive = True
    # mo.filter(mo.output_type == "quantile")


def main():
    #dataframes(DATABASE_FILE)
    ibis(DATABASE_FILE)


if __name__ == '__main__':
    main()
