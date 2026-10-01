---
name: unity-ecs
description: "Создание масштабируемых игр на Unity с Entity Component System (ECS): системы, запросы, джобы, Burst-компиляция и паттерны DOTS. Для высокопроизводительных игр на Unity."
category: gamedev
tags: [unity, ecs, dots, jobs, burst, game-dev, performance, csharp]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Unity ECS

> Создание высокопроизводительных игр на Unity с Entity Component System и DOTS.

## Быстрый старт

```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

// Определение компонента
public struct Health : IComponentData
{
    public float Current;
    public float Max;
}

// Определение системы
public partial class DamageSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float dt = SystemAPI.Time.DeltaTime;

        foreach (var (health, transform) in
            SystemAPI.Query<RefRW<Health>, RefRO<LocalTransform>>())
        {
            if (health.ValueRO.Current <= 0)
                continue;

            // Пример: регенерация здоровья со временем
            health.ValueRW.Current = math.min(
                health.ValueRO.Current + dt * 5f,
                health.ValueRO.Max
            );
        }
    }
}
```

## Когда использовать

- Создание игр с тысячами однотипных сущностей (пули, частицы, NPC)
- Когда производительности MonoBehaviour недостаточно
- Необходимость data-oriented дизайна и cache-friendly кода
- Масштабные симуляции или стратегические игры

## Пошагово

### 1. Проектирование компонентов (данные)

Держите компоненты маленькими и сфокусированными:

```csharp
public struct MovementSpeed : IComponentData { public float Value; }
public struct TargetPosition : IComponentData { public float3 Value; }
public struct DamageOnContact : IComponentData { public float Amount; }
```

### 2. Создание систем (логика)

Системы работают с сущностями, имеющими определённые комбинации компонентов:

```csharp
public partial class MovementSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float dt = SystemAPI.Time.DeltaTime;

        foreach (var (transform, speed) in
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<MovementSpeed>>())
        {
            var pos = transform.ValueRO.Position;
            pos.z += speed.ValueRO.Value * dt;
            transform.ValueRW.Position = pos;
        }
    }
}
```

### 3. Использование Jobs для параллелизма

```csharp
[BurstCompile]
public partial struct CalculateDamageJob : IJobEntity
{
    public float DeltaTime;

    void Execute(ref Health health, in DamageOverTime dot)
    {
        health.Current -= dot.DamagePerSecond * DeltaTime;
        health.Current = math.max(0, health.Current);
    }
}

public partial class DamageOverTimeSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var job = new CalculateDamageJob
        {
            DeltaTime = SystemAPI.Time.DeltaTime
        };
        job.ScheduleParallel();
    }
}
```

### 4. Запросы сущностей

```csharp
partial class TargetingSystem : SystemBase
{
    private EntityQuery _enemyQuery;

    protected override void OnCreate()
    {
        _enemyQuery = new EntityQueryBuilder(Allocator.Temp)
            .WithAll<Health, EnemyTag>()
            .WithNone<DeadTag>()
            .Build(this);
    }

    protected override void OnUpdate()
    {
        var enemies = _enemyQuery.ToEntityArray(Allocator.Temp);
        // Обработка врагов...
    }
}
```

### 5. Общие компоненты (рендеринг)

```csharp
public struct SpriteRenderer : ISharedComponentData
{
    public Texture2D Texture;
    public Material Material;
}

// Сущности с одинаковыми общими компонентами группируются вместе
```

## Лучшие практики

- **Держите компоненты маленькими** — единственная ответственность
- **Избегайте управляемых ссылок** в компонентах (используйте ссылки Entity)
- **Используйте Burst** для математически тяжёлых jobs
- **Группируйте сущности** по общим компонентам для рендеринга
- **Профилируйте с Unity Profiler** — измеряйте перед оптимизацией

## Типичные ошибки

- Забыли пометить job атрибутом `[BurstCompile]`
- Использование `foreach` вместо `IJobEntity` для больших наборов данных
- Создание слишком большого количества систем — группируйте связанную логику
- Не освобождают NativeArrays и другие нативные контейнеры

## Примеры

### Создание сущностей

```csharp
public partial class SpawnerSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var ecb = new EntityCommandBuffer(Allocator.TempJob);

        foreach (var (spawner, transform) in
            SystemAPI.Query<RefRO<Spawner>, RefRO<LocalTransform>>())
        {
            if (spawner.ValueRO.CanSpawn)
            {
                var entity = ecb.Instantiate(spawner.ValueRO.Prefab);
                ecb.SetComponent(entity, new LocalTransform
                {
                    Position = transform.ValueRO.Position
                });
            }
        }

        ecb.Playback(SystemAPI.GetSingleton<EntityManager>());
        ecb.Dispose();
    }
}
```

### Здоровье и смерть

```csharp
public partial class DeathSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var ecb = new EntityCommandBuffer(Allocator.TempJob);

        foreach (var (health, entity) in
            SystemAPI.Query<RefRO<Health>>().WithEntityAccess())
        {
            if (health.ValueRO.Current <= 0)
            {
                ecb.AddComponent<DeadTag>(entity);
                ecb.RemoveComponent<Health>(entity);
            }
        }

        ecb.Playback(SystemAPI.GetSingleton<EntityManager>());
        ecb.Dispose();
    }
}
```

## Валидация

```csharp
[Test]
public void MovementSystem_UpdatesPosition()
{
    using var world = new World("Test");
    var system = world.GetOrCreateSystemManaged<MovementSystem>();

    var entity = world.EntityManager.CreateEntity();
    world.EntityManager.AddComponentData(entity, new LocalTransform
    {
        Position = new float3(0, 0, 0)
    });
    world.EntityManager.AddComponentData(entity, new MovementSpeed { Value = 10f });

    system.Update();

    var transform = world.EntityManager.GetComponentData<LocalTransform>(entity);
    Assert.Greater(transform.Position.z, 0);
}
```
