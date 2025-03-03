# wait_for_db_to_be_ready() {
#     while ! docker exec -it -u postgres "$container_name" pg_isready -h "$postgres_host" -u "$postgres_user"; do
# 	echo "Waiting for the database server to be ready...sleeping for 2 seconds."
#         sleep 2
#     done
# }
#
# wait_for_db_to_be_ready
#


uv run python create_table.py \
--drop-table \
--table-type "regular" 
uv run python copy_data.py \
--method "psycopg3" \
--table-type "regular"\
--hours 8760 \
--workers 3 \
--benchmarks-file "benchmarks_copy.csv"
