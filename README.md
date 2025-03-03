# ReanalysisIngestion
ETL pipe line for ERA5 reanalysis data

## Introduction

This repository contains the code for the ETL pipeline for the ERA5 reanalysis data. The pipeline is designed to download ERA5 Reanalysis and ingest it into a database. The pipeline intened to avoid hours of waiting to query a timeseries for a location. It makes sense the setup a postgres database with the data and query the database for the timeseries.

However, this is not to disregard other potential analytic alternative such as using duckdb to do file-based queries and analysis. I will write a benchmark for different ingestion methods as well as how it compares to the filebased approach. But this is for later.

The pipeline uses the following tools:
    - Docker
    - uv python package manager
    - gcp cloud storage (downloading using CDS API taking too long; therefore I have migrated the downloaded data to GCP bucket once and for all)
    - Postgres
    - PgAdmin (to do quick SQL query check or database connection check, and iterate the process)
    - Bash scripts

## Run steps
1. Clone the repository
2. Run the following command to do docker-compose setup.
```docker-compose up -d```
3. Run the following command to run the pipeline
```bash ./run.sh``` and you will see the ingestion process.

You can play around the number of workers in `entrypoint.sh` to see how it affects the ingestion process. I recommend to keep it to larger than 2 now as I can't seem to fix bugs about timer context manager (which is to be used for benchmarking later and to clean up dask client in case).
