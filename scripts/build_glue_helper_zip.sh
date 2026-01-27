#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

ZIP="dist/glue-helper.zip"


# Collect python modules from src/ and flatten them into the zip root.
# This makes imports like: `from app import SearchKeywordPerformanceApp` work.
python_files=$(find src -type f -name "*.py" \
  ! -path "*/__pycache__/*" \
  ! -path "*/.pytest_cache/*")

if [[ -z "${python_files}" ]]; then
  echo "No .py files found under src/"
  exit 1
fi

rm -f "${ZIP}"

# -j flattens paths, placing files at the zip root
zip -j "${ZIP}" ${python_files}

echo "Created ${ZIP}"
unzip -l "${ZIP}" | head -n 50
