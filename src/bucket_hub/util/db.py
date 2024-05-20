import duckdb

"""

Created duckdb file via duckdb cli:
duckdb ~/code/bucket_hub/data/bsweger-flusight.db
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


def get_db_connection(db_file: str = "../../../data/bsweger-flusight.db"):
    con = duckdb.connect(db_file, read_only=True)
    return con
