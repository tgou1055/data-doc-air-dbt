# the Stable airflow version is 2.2.0, 2.3.2
FROM apache/airflow:2.9.2
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy dbt profile, modify profiles.yml location later
# COPY profiles.yml /root/.dbt/profiles.yml

# FROM ghcr.io/dbt-labs/dbt-snowflake:1.0.latest

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get install -y nano && rm -rf /var/lib/apt/lists/*

USER airflow
# Upgrade pip, setuptools, and wheel
#RUN pip install --upgrade pip setuptools wheel
RUN pip install --upgrade pip

# Install dbt
RUN pip install dbt-core==1.8.7
RUN pip install dbt-snowflake==1.8.3
