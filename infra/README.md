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
cd "infra/docker-compose"
docker compose up -d
```

Stop the stack:

```bash
docker compose down
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

### Kafka
- Provides an event bus for agents and asynchronous messaging.
- Deployed as a `StatefulSet` in Kubernetes to preserve storage and identity.
- Uses `volumeClaimTemplates` in Kubernetes for persistent storage.
- Exposed by a headless Service and a NodePort Service for local access.
- In Docker Compose, Kafka uses `apache/kafka:latest` and mounts `/var/lib/kafka` for persistent data.

### Qdrant
- Provides a vector database for retrieval-augmented generation (RAG) and embeddings.
- Deployed as a `StatefulSet` in Kubernetes for stable storage and pod identity.
- Uses `volumeClaimTemplates` for persistent storage.
- Exposed by a headless Service and a NodePort Service for local access.

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

## How to study this infra

- Start with Docker Compose for local experimentation.
- Use Kubernetes when you want to learn stateful deployment patterns, headless services, and persistent volumes.
- Compare `docker-compose/docker-compose.yaml` with `infra/k8s/*.yaml` to see how the same services map across both deployment models.
