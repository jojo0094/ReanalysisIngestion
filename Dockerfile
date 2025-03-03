# FROM timescale/timescaledb:latest-pg16
FROM timescale/timescaledb-ha:pg15.2-ts2.9.3-latest

USER root

WORKDIR /home/postgres

RUN apt-get update
RUN apt-get install -y wget

RUN apt-get install -y build-essential libreadline-dev libpam-dev postgresql-server-dev-15 libselinux1-dev libzstd-dev liblz4-dev libkrb5-dev zlib1g-dev python3 python3-pip libpq-dev clang llvm python3-dev
RUN wget https://github.com/ossc-db/pg_bulkload/releases/download/VERSION3_1_20/pg_bulkload-3.1.20.tar.gz
RUN tar xvf pg_bulkload-3.1.20.tar.gz
RUN cd pg_bulkload-3.1.20 && make && make install

# COPY pyproject.toml /home/postgres/pyproject.toml
# COPY uv.lock /home/postgres/uv.lock
COPY *.py /home/postgres/
COPY .env /home/postgres/.env
COPY entrypoint.sh /home/postgres/entrypoint.sh

RUN pip3 install uv
# RUN uv sync
RUN uv init
RUN uv venv
RUN uv python install 3.12
RUN uv add psycopg psycopg2-binary pandas xarray dask psycopg2 pyarrow dotenv sqlalchemy joblib tqdm netcdf4

ENV PATH="${PATH}:/home/postgres/pg_bulkload-3.1.20/bin"

# RUN ["chmod", "+x", "/home/postgres/entrypoint.sh"]
# RUN ["bash", "/home/postgres/entrypoint.sh"]
