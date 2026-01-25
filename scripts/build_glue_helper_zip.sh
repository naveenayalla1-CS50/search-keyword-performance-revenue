#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

# Zip only the python modules Glue needs at runtime.
# Adjust paths if your modules live elsewhere.
zip -r dist/glue-helper.zip \
  src/*.py src/**/*.py \
  -x "*__pycache__*" "*.pytest_cache*" "*.DS_Store*"
