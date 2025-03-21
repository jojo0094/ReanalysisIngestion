import argparse

from sqlalchemy import text

from utils import get_sqlalchemy_engine

def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a weather table in Postgres."
    )

    parser.add_argument(
        "--drop-table",
        action="store_true",
        default=False,
        help="Drop the table if it exists beforehand."
    )

    parser.add_argument(
        "--table-type",
        choices=["regular", "hyper"],
        help="Create a regular PostgreSQL table or a TimescaleDB hypertable.",
        required=True
    )

    parser.add_argument(
        "--unlogged",
        action="store_true",
        default=False,
        help="Make the table unlogged."
    )
    
    return parser.parse_args()


def main(args):
    engine = get_sqlalchemy_engine()

    with engine.connect() as conn:
        if args.drop_table:
            conn.execute(text("drop table if exists weather;"))
        
        unlogged = "unlogged" if args.unlogged else ""
        table_creation_query = f"""--sql
            create {unlogged} table if not exists weather (
                time timestamptz not null,
                location_id int,
                latitude float4,
                longitude float4,
                total_precipitation float4
            );
        """

        conn.execute(text(table_creation_query))

        if args.table_type == "hyper":
            conn.execute(text("select create_hypertable('weather', 'time');"))

        conn.commit()

if __name__ == "__main__":
    main(parse_args())
