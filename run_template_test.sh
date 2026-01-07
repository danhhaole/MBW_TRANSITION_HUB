#!/bin/bash

# Script to run Flow Template tests

echo "🧪 Running Flow Template Unit Tests..."
echo "========================================"

cd /home/mbw2025/cloude-app

# Run the specific test
bench --site mira.localhost run-tests \
  --app mbw_transition_hub \
  --doctype "Mira Flow Template"

echo ""
echo "========================================"
echo "✅ Test completed!"
