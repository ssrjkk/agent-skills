---
name: ai-gpu-infra-llmops
description: "Deploys and scales production AI/LLM and GPU infrastructure in Kubernetes using NVIDIA GPU Operator, DRA/MIG, vLLM tensor parallelism, KEDA scale-to-zero, Karpenter GPU nodes, Envoy AI Gateway, and LiteLLM. Use for self-hosted LLM serving and token cost governance."
category: devops
tags: [ai-infra, llmops, gpu, vllm, kubernetes, litellm, keda, karpenter]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# AI/GPU Infrastructure & LLMOps in Kubernetes

> High-throughput vLLM GPU serving, MIG/DRA hardware partitioning, KEDA scale-to-zero, and LiteLLM/Envoy AI Gateway routing.

## Quick Start
```bash
# Deploy vLLM multi-GPU inference server and LiteLLM AI Gateway in Kubernetes
kubectl apply -f labs/nextgen_2027_pack/k8s-gpu-vllm-inference.yaml
kubectl apply -f labs/nextgen_2027_pack/envoy-ai-gateway-litellm.yaml
```

```yaml
# Shared memory /dev/shm volume required for multi-GPU PyTorch NCCL tensor parallelism
volumes:
  - name: dshm
    emptyDir:
      medium: Memory
      sizeLimit: 16Gi
```

## When to Use
- Running open-weights LLMs (Qwen, Llama, DeepSeek, Mistral) on NVIDIA GPUs in Kubernetes with vLLM continuous batching and PagedAttention
- Partitioning A100/H100 GPUs via Multi-Instance GPU (MIG), Dynamic Resource Allocation (DRA), or Time-Slicing
- Scaling idle GPU inference pods down to zero with KEDA and provisioning spot/on-demand GPU nodes with Karpenter
- Routing, rate-limiting by tokens, semantic caching, and setting per-team budgets across local vLLM and cloud APIs via LiteLLM or Envoy AI Gateway

## Best Practices
- Always mount an in-memory emptyDir (medium: Memory, sizeLimit: 16Gi) at /dev/shm when tensor-parallel-size >= 2 so NCCL never crashes on Linux's default 64MB shm.
- Store HuggingFace model weights on a persistent PVC or pre-baked node snapshot so pod restarts do not re-download 60GB+ weights over the network.
- Enable --enable-prefix-caching and tune --gpu-memory-utilization 0.92 in vLLM to maximize KV-cache throughput for system prompts.
- Use hardware MIG profiles in production for strict VRAM/compute isolation and Time-Slicing only in non-critical dev/staging clusters.
- Place LiteLLM or Envoy AI Gateway in front of all model endpoints to enforce token-per-minute limits, budget caps, and automatic cloud failover.
- Enable Redis semantic caching on the AI Gateway to serve repeated or near-identical prompts in <15ms at zero GPU compute cost.

## Dependencies
```bash
# Install NVIDIA GPU Operator via Helm in Kubernetes
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
helm install gpu-operator nvidia/gpu-operator -n gpu-operator --create-namespace
```

## Examples
```python
# Estimate vLLM VRAM requirement (GB) for FP16/BF16 vs AWQ/GPTQ 4-bit quantization with KV cache overhead
def estimate_vram_gb(params_b: float, bits: int = 16, kv_overhead: float = 1.25) -> float:
    bytes_per_param = bits / 8.0
    return round(params_b * bytes_per_param * kv_overhead, 2)

assert estimate_vram_gb(32, bits=16) == 80.0
assert estimate_vram_gb(32, bits=4) == 20.0
```

```yaml
# LiteLLM Gateway configuration with local vLLM primary, Claude fallback, and Redis semantic cache
model_list:
  - model_name: coding-assistant
    litellm_params:
      model: openai/Qwen/Qwen2.5-Coder-32B-Instruct
      api_base: http://vllm-inference-svc.ai-inference.svc:8000/v1
      api_key: internal-k8s-key
litellm_settings:
  fallbacks: [{"coding-assistant": ["claude-sonnet-fallback"]}]
  cache: true
  cache_params:
    type: redis-semantic
```

## Step-by-Step
1. Deploy NVIDIA GPU Operator in Kubernetes and verify nvidia.com/gpu allocatable resources on GPU worker nodes.
2. Configure Karpenter NodePool with node.kubernetes.io/instance-type GPU families and consolidation policies.
3. Create a PersistentVolumeClaim for /root/.cache/huggingface and an in-memory emptyDir volume for /dev/shm.
4. Deploy vLLM with --tensor-parallel-size, --max-model-len, --enable-prefix-caching, and readiness probes on /health.
5. Configure a KEDA ScaledObject watching vllm:num_requests_waiting in Prometheus to scale GPU replicas between 0/1 and N.
6. Deploy LiteLLM / Envoy AI Gateway with virtual keys, per-team max_budget limits, and Redis semantic caching.
7. Monitor time-to-first-token (TTFT), inter-token latency (ITL), KV-cache usage, and GPU DCGM temperature/power metrics in Grafana.

## Validation
1. kubectl get nodes -o json confirms allocatable nvidia.com/gpu capacity on GPU nodes
2. vLLM /v1/chat/completions responds with streaming tokens and prefix-cache hit rate > 0%
3. LiteLLM gateway enforces token rate limits and seamlessly fails over when primary vLLM pod is cordoned
4. Prometheus scrapes both vLLM queue metrics and NVIDIA DCGM GPU utilization metrics

## Troubleshooting
- PyTorch NCCL error: unhandled system error / shm exhausted — mount emptyDir with medium: Memory and sizeLimit: 16Gi at /dev/shm.
- vLLM pod killed by livenessProbe during weight loading — add a startupProbe allowing up to 10 minutes (failureThreshold: 60, periodSeconds: 10).
- CUDA OutOfMemoryError on startup — lower --max-model-len or use AWQ/FP8 quantized weights to leave headroom for the KV cache.
- GPU pod stuck in Pending — ensure spec.tolerations includes key: nvidia.com/gpu, operator: Exists, effect: NoSchedule.
