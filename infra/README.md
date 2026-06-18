# Infra README

## Quick build-up guide

### 1. Install WSL 2 on Windows
- Install Windows Subsystem for Linux (WSL 2) from Microsoft.
- From PowerShell as administrator:
  ```powershell
  wsl --install
  wsl --set-default-version 2
  ```
- Restart Windows if prompted.

### 2. Install Docker Rancher Desktop
- Install Rancher Desktop for Windows and choose the WSL 2 backend.
- Enable Kubernetes if you want a local Kubernetes cluster.
- Make sure `docker` and `kubectl` are available in your shell.

### 3. Install `kubectl`
- If not already installed, install `kubectl` on Windows or in WSL:
  ```powershell
  choco install kubernetes-cli
  ```
- Or inside WSL:
  ```bash
  sudo apt update
  sudo apt install -y kubectl
  ```

### 4. Verify tools
- Docker:
  ```bash
  docker version
  ```
- kubectl:
  ```bash
  kubectl version --client
  ```

## Docker Compose quick start

From the repository root:

```bash
docker compose -f infra/docker-compose/docker-compose.yaml up -d --remove-orphans
```

Stop the stack:

```bash
docker compose -f infra/docker-compose/docker-compose.yaml down -v --remove-orphans
```

See all the containers:

```bash
docker compose -f infra/docker-compose/docker-compose.yaml ps [-a]  
```

Access to the command line of a container:

```bash
docker exec -it <container-name> bash
```

Recreate images from dockerfiles:

```bash
docker compose build --no-cache <dockerfile-img>
```

Check logs of a container:

```bash
docker logs <container-name>
```

## Kubernetes quick start

From the repository root:

```bash
kubectl apply -k infra/k8s
```

Preview the applied resources without changing the cluster:

```bash
kubectl apply -k infra/k8s --dry-run=client
```

Inspect the resources:

```bash
kubectl get all -n default
kubectl get pvc -n default
```

## What services are in this infra

### 1. Backend
- **Purpose:** Main REST API service for the swarn application.
- **K8s Type:** `Deployment` (2 replicas)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** No persistent storage (stateless)
- **Key Features:**
  - Connects to PostgreSQL database
  - Communicates with Qdrant vector database
  - Integrates with Ollama for LLM inference
  - Includes HorizontalPodAutoscaler (2-5 replicas based on CPU)
  - Readiness and liveness probes for health checking
  - Init container waits for PostgreSQL availability

### 2. Frontend
- **Purpose:** Web UI served by Vite + React application.
- **K8s Type:** `Deployment` (2 replicas)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** No persistent storage (stateless)
- **Key Features:**
  - Serves static files on port 80
  - Includes HorizontalPodAutoscaler (2-5 replicas based on CPU)
  - Health checks for readiness and liveness

### 3. PostgreSQL
- **Purpose:** Relational database for application data and LangFuse tracing.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (10 Gi via PersistentVolumeClaim)
- **Key Features:**
  - Mounts `/var/lib/postgresql/data` for data persistence
  - Single instance (no high availability in this setup)
  - Alpine-based image for minimal footprint

### 4. Qdrant
- **Purpose:** Vector database for retrieval-augmented generation (RAG) and embeddings.
- **K8s Type:** `StatefulSet` (1 replica)
- **Service Type:** Headless Service (stable pod identity) + regular Service
- **Storage:** Persistent (1 Gi via volumeClaimTemplates)
- **Key Features:**
  - Exposes HTTP API on port 6333
  - Exposes gRPC API on port 6334
  - Stable network identity via headless service
  - Each StatefulSet replica gets its own PVC

### 5. Ollama
- **Purpose:** Local LLM inference service for running language models.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (30 Gi via PersistentVolumeClaim)
- **Key Features:**
  - High resource requirements (4 Gi memory request, 2 CPU)
  - Stores models in `/root/.ollama` directory
  - Extended liveness probe initialization (60s) for model loading time

### 6. Kafka
- **Purpose:** Event streaming platform for agents and asynchronous messaging.
- **K8s Type:** `StatefulSet` (1 replica)
- **Service Type:** Headless Service (stable pod identity) + regular Service
- **Storage:** Persistent (2 Gi via volumeClaimTemplates)
- **Key Features:**
  - Mounts `/var/lib/kafka` for log storage
  - Exposes port 9092 for broker communication
  - Headless service provides stable DNS names for each broker
  - In Docker Compose: uses `apache/kafka:latest` with persistent storage

### 7. Prometheus
- **Purpose:** Metrics collection and time-series database for monitoring.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (5 Gi via PersistentVolumeClaim)
- **Key Features:**
  - Scrapes metrics from services every 15 seconds
  - Stores time-series data in `/prometheus`
  - Configuration via ConfigMap for scrape targets
  - Web UI on port 9090

### 8. Grafana
- **Purpose:** Metrics visualization and dashboard creation.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (5 Gi via PersistentVolumeClaim)
- **Key Features:**
  - Web UI on port 3000
  - Admin credentials from secrets
  - Stores dashboards and user data in `/var/lib/grafana`
  - Integrates with Prometheus as data source

### 9. Loki
- **Purpose:** Centralized log aggregation and search system.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (10 Gi via PersistentVolumeClaim)
- **Key Features:**
  - Ingests logs on port 3100
  - Integrates with Grafana for log visualization
  - Stores log data in `/loki`
  - Lightweight alternative to ELK stack

### 10. LangFuse
- **Purpose:** LLM application tracing and analytics platform.
- **K8s Type:** `Deployment` (1 replica)
- **Service Type:** ClusterIP (internal cluster communication)
- **Storage:** Persistent (10 Gi via PersistentVolumeClaim)
- **Key Features:**
  - Web UI on port 3000
  - Uses PostgreSQL as backend database
  - Requires NextAuth for authentication
  - Init container waits for PostgreSQL availability
  - Traces LLM calls and provides analytics

## Deployment Type Reference

| Service | K8s Type | Reason | Scaling | Storage |
|---------|----------|--------|---------|---------|
| Backend | Deployment | Stateless API, easy horizontal scaling | HPA (2-5) | None |
| Frontend | Deployment | Stateless web server, easy horizontal scaling | HPA (2-5) | None |
| PostgreSQL | Deployment | Single database instance (no HA) | Manual | Persistent |
| Qdrant | StatefulSet | Requires stable identity and persistent state | Manual | Persistent |
| Ollama | Deployment | Single LLM instance with persistent models | Manual | Persistent |
| Kafka | StatefulSet | Broker needs stable hostname and state | Manual | Persistent |
| Prometheus | Deployment | Time-series database with single instance | Manual | Persistent |
| Grafana | Deployment | Dashboard server, stateless from app perspective | Manual | Persistent |
| Loki | Deployment | Log aggregator, single instance | Manual | Persistent |
| LangFuse | Deployment | Stateless app relying on PostgreSQL | Manual | Persistent |

**Key Takeaways:**
- **Deployment:** Used for stateless services or when the pod doesn't need a stable identity
- **StatefulSet:** Used for stateful applications that need stable network identities and persistent storage (Kafka, Qdrant)
- **HorizontalPodAutoscaler:** Only applied to stateless services (Backend, Frontend) for automatic scaling based on metrics

## How Kafka and Qdrant work

### Kafka internals (high level)
- Kafka is a distributed event streaming platform.
- Producers send messages to Kafka topics, and consumers read from those topics.
- Kafka stores messages durably on disk, using logs and partitions.
- In this infra, Kafka runs as a single broker with persistent storage.
- The headless service gives Kafka pods stable network names; the NodePort service allows local host access.

### Qdrant internals (high level)
- Qdrant is a vector database optimized for similarity search.
- It stores vector embeddings and metadata, and can search for nearest vectors quickly.
- Qdrant exposes an HTTP API on port 6333 and a gRPC API on port 6334.
- In this infra, Qdrant runs as a single stateful node with persistent storage.
- The headless service provides stable pod identity; the NodePort service allows local host access.

## Notes on Docker Compose vs Kubernetes

- Docker Compose uses named volumes, direct port mappings, and local healthchecks.
- Kubernetes uses `StatefulSet` and `volumeClaimTemplates` to give each replica stable storage.
- In Docker Compose, Kafka is run using `apache/kafka:latest` with `/var/lib/kafka` persistence.
- In Docker Compose, the services are easier to run locally.
- In Kubernetes, the stack is closer to production patterns for stateful services.

## Typical questions and answers

### Q: How can I execute the K8s manifests with kustomization?
A: Use `kubectl apply -k infra/k8s`. The `-k` flag tells `kubectl` to render the Kustomize overlay in the `infra/k8s` folder.

### Q: What does a headless Service mean?
A: A headless Service is a Kubernetes Service with `clusterIP: None`. It does not get a virtual cluster IP, and DNS returns the pod IPs directly. This is useful when each pod needs a stable identity, such as with a `StatefulSet`.

### Q: When should I use a headless Service vs a normal Service?
A: Use a normal Service when pods are interchangeable and you want load balancing. Use a headless Service when each pod is unique and clients need to address individual pods, such as Kafka brokers or stateful databases.

### Q: Do `pvc.yaml` files only define storage objects?
A: Yes. `pvc.yaml` files are just Kubernetes manifests for `PersistentVolumeClaim` objects. They are separate from `Deployment` or `StatefulSet` resources, and they are used to request storage from the cluster.

### Q: Why not use a standalone `pvc.yaml` with `StatefulSet`?
A: You can, but `StatefulSet` usually uses `volumeClaimTemplates` so each pod gets its own PVC. If you point multiple StatefulSet replicas at one PVC, they would share the same volume, which is usually wrong for stateful workloads.

### Q: Why were the Docker Compose specs aligned to the Kubernetes specs?
A: The Compose file was updated to reflect the same service behavior, persistence, and health-check intent. That makes the local development environment easier to understand alongside the Kubernetes architecture.

## Kubernetes Management Commands

### 1. Discovering Your Cluster

Check all available namespaces:
```bash
kubectl get namespaces
# or abbreviated
kubectl get ns
```

Check your current context namespace:
```bash
kubectl config view --minify -o jsonpath='{..namespace}'
# Returns nothing = using 'default' namespace
```

Check where all your pods are running:
```bash
kubectl get pods --all-namespaces | findstr /i "backend|frontend|postgres|qdrant|kafka|ollama|prometheus|grafana|loki|langfuse"
# or on macOS/Linux:
kubectl get pods --all-namespaces | grep -iE "(backend|frontend|postgres|qdrant|kafka|ollama|prometheus|grafana|loki|langfuse)"
```

View all StatefulSets, Deployments, and PVCs across namespaces:
```bash
kubectl get statefulset,deployment,pvc -A
# or filtered:
kubectl get statefulset,deployment,pvc -A -n swarn-ai
```

### 2. Scaling Services Up and Down

Scale stateful services to 0 replicas (stops the pods):
```bash
# Kafka (StatefulSet)
kubectl scale statefulset kafka --replicas=0 -n swarn-ai

# Qdrant (StatefulSet)
kubectl scale statefulset qdrant --replicas=0 -n swarn-ai

# Scale back up
kubectl scale statefulset kafka --replicas=1 -n swarn-ai
kubectl scale statefulset qdrant --replicas=1 -n swarn-ai
```

Scale Deployments:
```bash
# Backend Deployment
kubectl scale deployment backend --replicas=0 -n swarn-ai
kubectl scale deployment backend --replicas=2 -n swarn-ai

# PostgreSQL Deployment
kubectl scale deployment postgres --replicas=0 -n swarn-ai
kubectl scale deployment postgres --replicas=1 -n swarn-ai

# Ollama Deployment
kubectl scale deployment ollama --replicas=0 -n swarn-ai
kubectl scale deployment ollama --replicas=1 -n swarn-ai

# Prometheus, Grafana, Loki, Langfuse (similar pattern)
kubectl scale deployment prometheus --replicas=0 -n swarn-ai
kubectl scale deployment grafana --replicas=0 -n swarn-ai
kubectl scale deployment loki --replicas=0 -n swarn-ai
kubectl scale deployment langfuse --replicas=0 -n swarn-ai
```

### 3. Managing Persistent Volumes

List all PersistentVolumeClaims in your namespace:
```bash
kubectl get pvc -n swarn-ai
# Show labels to see which service owns each PVC
kubectl get pvc -n swarn-ai --show-labels
```

List all PersistentVolumes:
```bash
kubectl get pv
```

### 4. Deleting PersistentVolumeClaims

Delete PVCs for specific services using labels:
```bash
# Delete Kafka and Qdrant PVCs only
kubectl delete pvc -l "app in (kafka,qdrant)" -n swarn-ai

# Delete all PVCs in namespace (WARNING: This destroys all data!)
kubectl delete pvc --all -n swarn-ai
```

### 5. Viewing Logs and Status

Check pod status:
```bash
kubectl get pods -n swarn-ai
kubectl get pods -n swarn-ai -o wide
```

View logs from a specific pod:
```bash
kubectl logs <pod-name> -n swarn-ai
# Follow logs in real-time
kubectl logs <pod-name> -n swarn-ai -f
```

Describe a pod (shows events and status):
```bash
kubectl describe pod <pod-name> -n swarn-ai
```

### 6. Port Forwarding for Local Access

Forward ports to access services locally:
```bash
# Frontend (port 80 -> localhost:3000)
kubectl port-forward svc/frontend 3000:80 -n swarn-ai

# Backend API (port 8000 -> localhost:8000)
kubectl port-forward svc/backend 8000:8000 -n swarn-ai

# Qdrant (port 6333 -> localhost:6333)
kubectl port-forward svc/qdrant 6333:6333 -n swarn-ai

# Ollama (port 11434 -> localhost:11434)
kubectl port-forward svc/ollama 11434:11434 -n swarn-ai

# Prometheus (port 9090 -> localhost:9090)
kubectl port-forward svc/prometheus 9090:9090 -n swarn-ai

# Grafana (port 3000 -> localhost:3000)
kubectl port-forward svc/grafana 3000:3000 -n swarn-ai

# Loki (port 3100 -> localhost:3100)
kubectl port-forward svc/loki 3100:3100 -n swarn-ai

# LangFuse (port 3000 -> localhost:3000)
kubectl port-forward svc/langfuse 3000:3000 -n swarn-ai

# PostgreSQL (port 5432 -> localhost:5432)
kubectl port-forward svc/postgres 5432:5432 -n swarn-ai

# Kafka (port 9092 -> localhost:9092)
kubectl port-forward svc/kafka-service 9092:9092 -n swarn-ai
```

### 7. Clean Reset (Destroy Everything and Redeploy)

```bash
# Remove all resources in the namespace
kubectl delete all --all -n swarn-ai

# Delete all PVCs (destroys persisted data)
kubectl delete pvc --all -n swarn-ai

# Reapply all manifests
kubectl apply -k infra/k8s
```

### 8. Troubleshooting Common Issues

Pod is stuck in "Pending":
```bash
# Check why pod can't be scheduled
kubectl describe pod <pod-name> -n swarn-ai
# Usually due to: insufficient resources, no PVC available, or image pull issues
```

Pod is crashing ("CrashLoopBackOff"):
```bash
# Check logs to see what went wrong
kubectl logs <pod-name> -n swarn-ai --previous
# Shows the logs from the previous crash
```

Service not accessible:
```bash
# Check if service exists and has endpoints
kubectl get svc -n swarn-ai
kubectl get endpoints -n swarn-ai

# Check pod labels match service selector
kubectl get pods -n swarn-ai --show-labels
kubectl get svc <service-name> -n swarn-ai -o yaml | grep selector
```

## How to study this infra

- Start with Docker Compose for local experimentation.
- Use Kubernetes when you want to learn stateful deployment patterns, headless services, and persistent volumes.
- Compare `docker-compose/docker-compose.yaml` with `infra/k8s/*.yaml` to see how the same services map across both deployment models.
