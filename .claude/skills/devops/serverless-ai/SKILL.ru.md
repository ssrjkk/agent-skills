---
name: serverless-ai
description: "Serverless AI inference (Cloudflare Workers, Lambda)"
category: devops
tags: [serverless-ai, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: serverless-ai
---
# Serverless AI

> Запускайте AI-инференс на edge с serverless-платформами: Cloudflare Workers и AWS Lambda.

## Быстрый старт
```typescript
// Cloudflare Workers AI — edge-инференс
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { pathname } = new URL(request.url);

    if (pathname === "/generate") {
      const { prompt } = await request.json() as { prompt: string };

      const response = await env.AI.run("@cf/meta/llama-3.2-3b-instruct", {
        prompt: prompt,
        max_tokens: 500,
        temperature: 0.7
      });

      return Response.json(response);
    }

    // Текстовые эмбеддинги
    if (pathname === "/embed") {
      const { text } = await request.json() as { text: string | string[] };
      const embeddings = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
        text: Array.isArray(text) ? text : [text]
      });
      return Response.json(embeddings);
    }

    return new Response("Not found", { status: 404 });
  }
};
```

```python
# AWS Lambda с SageMaker
import boto3
import json
import os

sagemaker = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = os.environ["ENDPOINT_NAME"]

def lambda_handler(event, context):
    body = json.loads(event["body"])

    response = sagemaker.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps({
            "inputs": body["prompt"],
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        })
    )

    result = json.loads(response["Body"].read().decode())
    return {"statusCode": 200, "body": json.dumps({"response": result})}
```

## Ключевые концепции
Serverless AI меняет холодные старты на нулевые затраты в простое. Cloudflare Workers запускают инференс у пользователя (edge). Lambda с SageMaker даёт масштабируемый GPU-инференс. Лучше всего подходит для лёгких моделей и нагрузок по требованию.

## Когда использовать
- Лёгкий инференс (модели < 3B параметров)
- Переменная нагрузка с непредсказуемым трафиком
- Edge-приложения (требования к низкой задержке)
- Прототипы и недорогие деплои

## Пошаговое руководство
1. Выберите платформу: Workers AI для edge-инференса у пользователя, Lambda + SageMaker endpoint для более тяжёлых GPU-моделей или гибрид по маршрутам.
2. Проектируйте stateless-обработчики: логика модели и промптов в коде, состояние (эмбеддинги/поиск) во внешнем хранилище — KV, S3, БД.
3. Добавьте ограничения: Workers `wait`/`event.waitUntil`, Lambda `maxBatchSize`, строгие бюджеты памяти и таймаутов.
4. Боритесь с холодными стартами: прогревайте критичный путь (WarmPool / cron ping), держите payload небольшим.
5. Инструментируйте: логируйте задержку, токены, стоимость и ошибки; алармы на P95 выше бюджета.
6. Срезайте затраты на пиках: полагайтесь на автоскейлинг провайдера и кэш; A/B-тестируйте размер модели против задержки.

## Примеры
```typescript
// Workers AI с кэшем и lookup эмбеддингов
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const cache = caches.default;
    const url = new URL(request.url);
    const cached = await cache.match(request);
    if (cached) return cached;

    if (url.pathname === "/summarize") {
      const { text } = await request.json() as { text: string };
      const out = await env.AI.run("@cf/meta/llama-3.2-3b-instruct", {
        prompt: `Summarize in one sentence:\n${text}`,
        max_tokens: 120,
      });
      const json = Response.json(out);
      json.headers.set("Cache-Control", "max-age=300");
      await cache.put(request, json.clone());
      return json;
    }
    return Response.json({ ok: false, reason: "not found" }, { status: 404 });
  },
};
```
```bash
# Замер холодных стартов во времени
curl -w "@dns_time=%{time_starttransfer}\n" https://edge.example.com/summarize
# нагрузочный тест Lambda
hey -n 1000 -c 50 -m POST https://api-aws.example.com/generate
```

## Лучшие практики
- Низкий cold-start: модели меньше, warmers, минимум зависимостей.
- Рантаймы под CPU/GPU; батчинг где можно.
- Кэш весов моделей в слое или общем хранилище.
- Таймауты и память под ворклоад.
- Мониторинг invocations, длительности и cold-start rate.
- Для длинных запросов — выделенный эндпоинт.

## Устранение неполадок
- Высокие cold start: provisioned concurrency или warmer.
- Таймаут: разбейте работу или поднимите лимит функции.
- Ошибки памяти: правильно выделите под модель.
- Спайки стоимости: просмотрите паттерны invocations и кэш.

## Валидация
1. Функция деплоится и отвечает на запросы
2. Задержка холодного старта приемлема для кейса
3. Качество инференса соответствует ожиданиям для размера модели
4. Стоимость ниже always-on GPU-инстансов при переменном трафике
