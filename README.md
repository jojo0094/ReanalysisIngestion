# ReanalysisIngestion
ETL pipe line for ERA5 reanalysis data


![AI generated image](./data/images/aigenerated.png)

<sub><sup>⚠️ AI-Generated Content Warning: This image was generated using AI and may not be 100% accurate or representative of real-world systems.</sup></sub>

## Introduction

This repository contains the code for the ETL pipeline for the ERA5 reanalysis data. The pipeline is designed to download ERA5 Reanalysis dataset and ingest it into a database. The pipeline intended to avoid hours of waiting to query a timeseries for a location. It makes sense to set up a postgres database with the data first and query the database for the timeseries.

However, this is not to disregard other potential analytic alternative such as using duckdb to do file-based queries and analysis. I will write a benchmark for different ingestion methods as well as how it compares to the filebased approach. But this is for later.

The pipeline uses the following tools:

- **Docker**
- **uv** (Python package manager)
- **Google Cloud Storage** (CDS API downloads were too slow, so data was migrated to a GCP bucket temporarily). If, however, you want to download yourself, use `download.py` (check out cds copernicus  site for api setup)
- **PostgreSQL**
- **pgAdmin** (for quick SQL queries and connection checks)
- **Bash scripts**


## Run steps
1. Clone the repository
2. Run the following command to do docker-compose setup.
```docker-compose up -d```
3. Run the following command to run the pipeline
```bash ./run.sh``` and you will see the ingestion process.

You can play around the number of workers in `entrypoint.sh` to see how it affects the ingestion speed. I recommend to keep it to larger than 1 now as I can't seem to fix bugs about timer context manager (which is to be used for benchmarking later and to clean up dask client resource in case).

![Gif](./data/images/reanalysis.gif)
