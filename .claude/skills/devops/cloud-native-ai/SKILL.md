---
name: cloud-native-ai
description: "Cloud-native AI deployment patterns"
category: devops
tags: [cloud-native, ai, kubernetes, inference, deployment]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Cloud-Native AI

> Deploy and scale AI workloads using cloud-native patterns with Kubernetes and containerization.

## Quick Start
```yaml
# model-serving.yaml — vLLM inference server
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args: ["--model", "mistralai/Mistral-7B-v0.1"]
        env:
        - name: HUGGING_FACE_HUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: hf-token
              key: token
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
            cpu: "8"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-server
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Pods
    pods:
      metric:
        name: vllm:gpu_cache_usage_perc
      target:
        type: AverageValue
        averageValue: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

```bash
# Model inference with batching
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-v0.1",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

## Key Concepts
Cloud-native AI uses containers, orchestration, service mesh, and GitOps for ML deployment. Key patterns: model serving with vLLM/TGI, batch inference with Kueue/Volcano, model registries, and A/B testing with traffic splitting.

## When to Use
- Production AI services requiring high availability
- Multi-model serving infrastructure
- CI/CD for ML models with canary deployments
- GPU cluster management and scheduling

## Step-by-Step
1. Containerize the model server: build an image with the inference engine (vLLM/TGI) and pinned model weights.
2. Deploy with Kubernetes: define a `Deployment` with GPU resource limits, env secrets, and `/health` readiness probe.
3. Expose the API: create a `Service` (ClusterIP) plus an `Ingress`/Gateway with TLS and routing to `/v1`.
4. Scale horizontally: attach an HPA on the GPU-cache metric (`vllm:gpu_cache_usage_perc`) with a stabilization window.
5. Roll out safely: use a rolling update with readiness checks for new model versions; route canary traffic by weight.
6. Run batch jobs: use Kueue/Volcano `Queue` + `Job` for offline inference, with PVC-based output artifacts.

## Examples
```yaml
# Gateway + Service exposing the model API
apiVersion: v1
kind: Service
metadata:
  name: vllm-server
spec:
  selector: { app: vllm }
  ports:
    - port: 8000
      targetPort: 8000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: model-ingress
spec:
  rules:
    - host: models.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service: { name: vllm-server, port: { number: 8000 } }
```
```bash
kubectl apply -f model-serving.yaml -f hpa.yaml -f svc-ingress.yaml
kubectl rollout status deployment/vllm-server
kubectl get hpa vllm-hpa
curl https://models.example.com/v1/chat/completions -d '{"model":"mistralai/Mistral-7B-v0.1","messages":[{"role":"user","content":"hi"}],"max_tokens":50}'
```

## Best Practices
- Run AI workloads in containers with pinned base images.
- Use GPU resource requests/limits on Kubernetes for inference.
- Cache models and embeddings to cut cold-start latency.
- Scale inference horizontally behind a load balancer.
- Monitor GPU utilization, latency, and error rates.
- Use a service mesh or gateway for traffic control.

## Troubleshooting
- GPU not allocated: check nodeSelector, resources, and driver.
- Cold start slow: preload models into shared memory or cache.
- OOM on inference: batch requests or right-size the container.
- Latency spikes: scale replicas and warm the model cache.

## Validation
1. Model deployment completes with health check passing
2. HPA scales based on GPU utilization
3. Rolling update deploys new model version without downtime
4. Batch inference jobs complete with correct results
