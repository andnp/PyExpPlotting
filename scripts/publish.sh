#!/bin/bash
set -e

MYPYPATH=./typings mypy --ignore-missing-imports -p PyExpUtils

git config credential.helper "store --file=.git/credentials"
echo "https://${GH_TOKEN}:@github.com" > .git/credentials

git config user.email "andnpatterson@gmail.com"
git config user.name "github-action"

git fetch --all --tags

git checkout -f main

# bump the version
cz bump --no-verify --yes --check-consistency

# push to pypi repository
pdm build
python -m twine upload -u __token__ -p ${PYPI_TOKEN} --non-interactive dist/*

git push
git push --tags
