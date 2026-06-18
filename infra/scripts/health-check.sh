#!/bin/bash

# Health check script to verify all services are running

SERVICES=(
  "postgres:5432"
  "qdrant:6333"
  "ollama:11434"
  "backend:8000"
  "frontend:5173"
  "prometheus:9090"
  "grafana:3000"
  "loki:3100"
)

echo "Checking service health..."

for service in "${SERVICES[@]}"; do
  IFS=':' read -r host port <<< "$service"
  
  if nc -z "$host" "$port" 2>/dev/null; then
    echo "✓ $service is up"
  else
    echo "✗ $service is down"
  fi
done

echo "Health check complete!"
