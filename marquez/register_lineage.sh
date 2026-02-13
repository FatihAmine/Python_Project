#!/bin/bash

# 1. Create Namespace
echo "Creating Namespace..."
curl -X PUT http://localhost:5000/api/v1/namespaces/shopverse \
  -H "Content-Type: application/json" \
  -d '{
    "ownerName": "admin",
    "description": "E-commerce analytics pipeline"
  }'
echo ""

# 2. Create Source
echo "Creating Source..."
curl -X PUT http://localhost:5000/api/v1/sources/local_filesystem \
  -H "Content-Type: application/json" \
  -d '{
    "type": "POSTGRESQL", 
    "connectionUrl": "jdbc:postgresql://localhost:5432/marquez",
    "description": "Simulated local filesystem source"
  }'
echo ""

# 3. Create Input Dataset (Logs)
echo "Creating Input Dataset..."
curl -X PUT http://localhost:5000/api/v1/namespaces/shopverse/datasets/shopverse.logs \
  -H "Content-Type: application/json" \
  -d '{
    "type": "DB_TABLE",
    "physicalName": "shopverse.logs",
    "sourceName": "local_filesystem",
    "fields": [
      {"name": "timestamp", "type": "VARCHAR"},
      {"name": "event_type", "type": "VARCHAR"},
      {"name": "user_id", "type": "VARCHAR"}
    ],
    "description": "Raw JSON event logs from e-commerce site"
  }'
echo ""

# 4. Create Output Dataset (Analytics)
echo "Creating Output Dataset..."
curl -X PUT http://localhost:5000/api/v1/namespaces/shopverse/datasets/shopverse.analytics \
  -H "Content-Type: application/json" \
  -d '{
    "type": "DB_TABLE",
    "physicalName": "shopverse.analytics",
    "sourceName": "local_filesystem",
    "fields": [
      {"name": "event_type", "type": "VARCHAR"},
      {"name": "count", "type": "INTEGER"}
    ],
    "description": "Aggregated analytics data in CSV format"
  }'
echo ""

# 5. Create & Run Job (NiFi Association)
echo "Creating Job..."
curl -X PUT http://localhost:5000/api/v1/namespaces/shopverse/jobs/nifi_event_aggregation \
  -H "Content-Type: application/json" \
  -d '{
    "type": "BATCH",
    "inputs": [{"namespace": "shopverse", "name": "shopverse.logs"}],
    "outputs": [{"namespace": "shopverse", "name": "shopverse.analytics"}],
    "location": "https://github.com/shopverse/nifi-pipeline",
    "description": "NiFi Manual Pipeline: GetFile -> EvaluateJsonPath -> QueryRecord -> PutFile"
  }'
echo ""

# 6. Trigger a Run (simulated)
echo "Triggering simulated run..."
RUN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/namespaces/shopverse/jobs/nifi_event_aggregation/runs \
  -H "Content-Type: application/json" \
  -d '{}')
echo "Run Response: $RUN_RESPONSE"
RUN_ID=$(echo $RUN_RESPONSE | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
echo "Run ID: $RUN_ID"

if [ -n "$RUN_ID" ]; then
  echo "Completing run..."
  curl -X POST http://localhost:5000/api/v1/jobs/runs/$RUN_ID/complete
else
  echo "Run ID not found, skipping completion."
fi
echo ""
echo "Done!"
