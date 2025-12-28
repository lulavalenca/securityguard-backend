#!/bin/bash
# Run linting checks

echo "Running black..."
black app/

echo "Running flake8..."
flake8 app/ --max-line-length=100 --extend-ignore=E203,W503

echo "Running isort..."
isort app/

echo "Running mypy..."
mypy app/ --ignore-missing-imports

echo "✓ Linting complete!"
