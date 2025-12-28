#!/bin/bash
# Run test suite

echo "Running tests..."
pytest app/tests -v --cov=app --cov-report=html

if [ $? -eq 0 ]; then
    echo "✓ All tests passed!"
    echo "Coverage report: htmlcov/index.html"
else
    echo "✗ Tests failed!"
    exit 1
fi
