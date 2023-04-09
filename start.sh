#! /usr/bin/env bash

# Let the DB start
python3 ./bookstore/backend_pre_start.py

# Run the migrations
alembic upgrade head

# Create initial data in DB
python3 ./bookstore/initial_data.py

# Run the api
exec uvicorn bookstore.main:app --reload --host 0.0.0.0 --port 8000