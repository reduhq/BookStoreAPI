#! /usr/bin/env bash
set -e
set -x

pytest --cov=bookstore --cov-report=term-missing bookstore/tests