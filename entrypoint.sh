#!/bin/bash
# wait_for_db_to_be_ready() {
#     while ! docker exec -it -u postgres "$CONTAINER_NAME" pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
# 	echo "Waiting for the database server to be ready...sleeping for 2 seconds."
#         sleep 2
#     done
# }
#

echo "Waiting for the database server to be ready...sleeping for 2 seconds."
sleep 5

source .env 

wait_for_db_to_be_ready() {
    while ! pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
        echo "Waiting for the database server to be ready...sleeping for 2 seconds."
        sleep 2
    done
}


# wait_for_db_to_be_ready



uv run python create_table.py \
--drop-table \
--table-type "regular" 


uv run python copy_data.py \
--method "psycopg3" \
--table-type "regular" \
--hours 8760 \
--workers 5 \
--benchmarks-file "benchmarks_copy.csv"
