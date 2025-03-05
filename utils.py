import os
import subprocess

import dotenv
import sqlalchemy
import psycopg

dotenv.load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

def num_rows(hours):
    return hours * 1038240

def sqlalchemy_connection_string():
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

def get_sqlalchemy_engine():
    engine = sqlalchemy.create_engine(sqlalchemy_connection_string())
    return engine

def get_psycopg3_connection():
    connection_string = (
        f"host={POSTGRES_HOST} "
        f"port={POSTGRES_PORT} "
        f"dbname={POSTGRES_DB_NAME} "
        f"user={POSTGRES_USER} "
        f"password={POSTGRES_PASSWORD}"
    )
    return psycopg.connect(connection_string)

def get_nc_link() -> str:
    """Currently just one default link"""
    return "https://storage.googleapis.com/era5_reanalysis_nz_tp/total_precipitation_2000.nc"

def get_nc_links(start_year: int, end_year: int) -> list:
    """Get links for all the years in the range"""
    links = []
    for year in range(start_year, end_year + 1):
        link = f"https://storage.googleapis.com/era5_reanalysis_nz_tp/total_precipitation_{year}.nc"
        links.append(link)
    return links

