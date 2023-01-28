#! /usr/bin/env bash
set -e
set -x

pytest --cov=schoolapi --cov-report=term-missing schoolapi/tests