import time
from importlib import resources

import structlog
from rich import print

from bucket_hub.util.db import get_db_connection

logger = structlog.get_logger()

DATABASE_NAME = "bsweger-flusight.db"


def main():
    # janky way to get a path to the db file
    data_location = str(resources.files("bucket_hub").parent.parent / "data" / DATABASE_NAME)
    logger.info("connecting to DuckDB database", db_file=data_location)

    # con = get_db_connection(str(data_location))
    with get_db_connection(data_location) as con:
        sql = "SELECT model_id, count(*) AS total_submissions FROM model_output GROUP BY model_id;"

        print("Querying local, persistent DuckDB")
        start = time.process_time()
        mo_data = con.sql(sql)
        logger.info("executed DuckDB query", sql=sql, elapsed_time=time.process_time() - start)
        print(mo_data)

        print("DuckDB result as pandas dataframe: mo_data.to_db()\n")
        start = time.process_time()
        mo_data_df = mo_data.to_df()
        logger.info("converted DuckDB data to pandas", elapsed_time=time.process_time() - start)
        print(mo_data_df)

        print("DuckDb result as polars dataframe:  mo_data.pl()\n")
        start = time.process_time()
        mo_data_pl = mo_data.pl()
        logger.info("converted DuckDB data to polars", elapsed_time=time.process_time() - start)
        print(mo_data_pl)


if __name__ == "__main__":
    main()
