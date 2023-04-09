#! /usr/bin/env bash
set -e

python /BookStore/bookstore/tests_pre_start.py

bash /BookStore/bookstore/scripts/test.sh "$@"