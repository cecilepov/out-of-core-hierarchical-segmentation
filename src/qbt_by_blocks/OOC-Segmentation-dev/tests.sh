#!/usr/bin/env bash

for filename in Tests/*.py; do
    pytest -v ${filename}
done
