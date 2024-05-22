from cloudpathlib import S3Path, AnyPath
import duckdb
import structlog

logger = structlog.get_logger()

"""

Created duckdb file via duckdb cli:
duckdb ~/code/duck_hub/data/bsweger-flusight.db
#
# Need the httpfs plugin to read from s3
# INSTALL httpfs;
#
# disable http_keep_alive avoids IO error caused by httpfs leaving things open, which
# results in hitting the max number of open connections
SET http_keep_alive=false;

# filename=true adds a column to the table that points to the parquet file a row came from
# union_by_name=true accommodates different schemas in the parquet files (for example, the "location" schema
# in some files is set to integer--presumably because there is no "US", but in others it's a string)
CREATE TABLE model_output AS
SELECT * FROM read_parquet('s3://bsweger-flusight-forecast/model-output/*/*.parquet', filename=true, union_by_name=true);

"""

def create_hub_database(hub_bucket_name: str, db_path: str, db_name: str) -> str:
    db_file = AnyPath(db_path) / db_name

    if db_file.is_file():
        logger.warning('Database not created, file already exists', file=str(db_file))
        return

    hub_bucket = S3Path(f's3://{hub_bucket_name}')
    hub_model_output = hub_bucket / 'model-output'

    with duckdb.connect(str(db_file)) as con:
        con.sql('INSTALL httpfs;')
        con.sql('SET http_keep_alive=false;')
        con.sql(f"""
            CREATE TABLE model_output AS
            SELECT * FROM read_parquet('{str(hub_model_output)}/*/*.parquet', filename=true, union_by_name=true);
        """)
        con.table('model_output').show()
        logger.info('Created DuckDB database', db_file=str(db_file), num_rows=con.table('model_output').count('round_id').fetchall()[0][0])

    return str(db_file)


def get_db_connection(db_file: str = '../../../data/bsweger-flusight.db'):
    con = duckdb.connect(db_file, read_only=True)
    return con
