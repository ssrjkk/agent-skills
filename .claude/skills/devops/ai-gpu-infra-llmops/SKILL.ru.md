---
name: ai-gpu-infra-llmops
description: "Deploys and scales production AI/LLM and GPU infrastructure in Kubernetes using NVIDIA GPU Operator, DRA/MIG, vLLM tensor parallelism, KEDA scale-to-zero, Karpenter GPU nodes, Envoy AI Gateway, and LiteLLM. Use for self-hosted LLM serving and token cost governance."
category: devops
tags: [ai-infra, llmops, gpu, vllm, kubernetes, litellm, keda, karpenter]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: ai-gpu-infra-llmops
author: ssrjkk
---
# AI/GPU Infrastructure & LLMOps in Kubernetes (Сервинг LLM и GPU в K8s)

> Высокопроизводительный сервинг LLM через vLLM на GPU в Kubernetes, разделение карт MIG/DRA, автоскейлинг KEDA и шлюз LiteLLM.

## Быстрый старт
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

## Когда использовать
- Запуск локальных LLM (Qwen, Llama, DeepSeek, Mistral) на картах NVIDIA в Kubernetes через движок vLLM (PagedAttention, Continuous Batching)
- Аппаратная нарезка дорогих GPU A100/H100 через профили MIG, драйверы DRA или разделение времени Time-Slicing
- Масштабирование простаивающих GPU-подов в ноль через KEDA и быстрый заказ GPU-нод через Karpenter
- Единый шлюз LiteLLM / Envoy AI Gateway для учета токенов, бюджетов по командам, семантического кэша в Redis и фоллбэка в облачные API

## Лучшие практики
- Обязательно монтируйте emptyDir в RAM (medium: Memory, sizeLimit: 16Gi) в /dev/shm при tensor-parallel-size >= 2, иначе PyTorch NCCL упадет из-за лимита в 64 МБ.
- Кэшируйте веса моделей HuggingFace на постоянном томе PVC или локальном NVMe, чтобы при рестарте пода не качать по 60+ ГБ из сети.
- Включайте --enable-prefix-caching и --gpu-memory-utilization 0.92 в vLLM для переиспользования KV-кэша системных промптов.
- Применяйте аппаратный MIG в продакшене для жесткой изоляции видеопамяти, а Time-Slicing — только для тестовых и dev-стендов.
- Ставьте шлюз LiteLLM / Envoy AI Gateway перед всеми LLM для лимитирования токенов в минуту, контроля бюджетов и автопереключения при сбоях.
- Включайте семантический кэш в Redis/Valkey на уровне AI-шлюза, чтобы отдавать типовые ответы за 15 мс без нагрузки на GPU.

## Зависимости
```bash
# Install NVIDIA GPU Operator via Helm in Kubernetes
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
helm install gpu-operator nvidia/gpu-operator -n gpu-operator --create-namespace
```

## Примеры
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

## Пошаговое руководство
1. Установите NVIDIA GPU Operator в кластер и проверьте появление ресурсов nvidia.com/gpu в описании GPU-узлов.
2. Опишите Karpenter NodePool с фильтрацией по GPU-инстансам, толерациями nvidia.com/gpu и политикой консолидации.
3. Создайте том PVC для кэша весов /root/.cache/huggingface и том emptyDir в памяти (Memory) для /dev/shm.
4. Разверните Deployment с vLLM, указав --tensor-parallel-size, --max-model-len, --enable-prefix-caching и пробу готовности /health.
5. Настройте KEDA ScaledObject по метрике очереди запросов vllm:num_requests_waiting для автоскейлинга реплик.
6. Поднимите шлюз LiteLLM / Envoy AI Gateway с виртуальными ключами команд, лимитами бюджетов и семантическим кэшем в Redis.
7. Выведите на дашборд Grafana метрики TTFT (время первого токена), заполнение KV-cache и телеметрию карт DCGM Exporter.

## Валидация
1. Узлы кластера отображают доступные ресурсы nvidia.com/gpu в выводе kubectl describe node
2. Эндпоинт vLLM /v1/chat/completions отдает поток токенов и фиксирует попадания в prefix-cache
3. Шлюз LiteLLM контролирует квоты токенов и прозрачно переключает запросы на резервную модель при остановке пода vLLM
4. В Prometheus поступают метрики очереди vLLM и аппаратная телеметрия видеокарт из DCGM Exporter

## Устранение неполадок
- Ошибка PyTorch NCCL: unhandled system error при старте на нескольких GPU — примонтируйте emptyDir (medium: Memory, 16Gi) в /dev/shm.
- Под vLLM перезапускается во время загрузки тяжелых весов — добавьте startupProbe с запасом до 10 минут (failureThreshold: 60, periodSeconds: 10).
- Ошибка CUDA OutOfMemoryError при инициализации KV-кэша — уменьшите --max-model-len или перейдите на квантованные веса AWQ/FP8.
- GPU-под висит в статусе Pending — проверьте наличие toleration для ключа nvidia.com/gpu:NoSchedule в манифесте пода.
