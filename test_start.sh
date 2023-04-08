#! /usr/bin/env bash
set -e

python /SchoolApi/schoolapi/tests_pre_start.py

bash /SchoolApi/schoolapi/scripts/test.sh "$@"