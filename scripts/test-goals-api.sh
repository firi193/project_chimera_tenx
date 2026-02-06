#!/usr/bin/env bash
# Test Goals API with curl (backend must be running on port 8000)
set -e
BASE="${BASE_URL:-http://localhost:8000}"
echo "=== Create goal ==="
CREATE=$(curl -s -X POST "$BASE/api/v1/goals" -H "Content-Type: application/json" -d '{"description": "My first goal"}')
echo "$CREATE" | jq . 2>/dev/null || echo "$CREATE"
GOAL_ID=$(echo "$CREATE" | jq -r '.id // empty')
if [ -z "$GOAL_ID" ]; then
  echo "No goal id in response; create may have failed."
  exit 1
fi
echo ""
echo "=== List goals ==="
curl -s "$BASE/api/v1/goals" | jq . 2>/dev/null || curl -s "$BASE/api/v1/goals"
echo ""
echo "=== Get goal $GOAL_ID ==="
curl -s "$BASE/api/v1/goals/$GOAL_ID" | jq . 2>/dev/null || curl -s "$BASE/api/v1/goals/$GOAL_ID"
