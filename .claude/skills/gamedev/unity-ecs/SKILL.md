---
name: unity-ecs
description: "Build scalable Unity games with Entity Component System (ECS): systems, queries, jobs, burst compilation, and DOTS patterns. Use for high-performance Unity."
category: gamedev
tags: [unity, ecs, dots, jobs, burst, game-dev, performance, csharp]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Unity ECS

> Building high-performance Unity games with Entity Component System and DOTS.

## Quick Start

```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

// Define a component
public struct Health : IComponentData
{
    public float Current;
    public float Max;
}

// Define a system
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

            // Example: regenerate health over time
            health.ValueRW.Current = math.min(
                health.ValueRO.Current + dt * 5f,
                health.ValueRO.Max
            );
        }
    }
}
```

## When to Use

- Building games with thousands of similar entities (bullets, particles, NPCs)
- When MonoBehaviour performance is not enough
- Need for data-oriented design and cache-friendly code
- Large-scale simulations or strategy games

## Step-by-Step

### 1. Design Components (Data)

Keep components small and focused:

```csharp
public struct MovementSpeed : IComponentData { public float Value; }
public struct TargetPosition : IComponentData { public float3 Value; }
public struct DamageOnContact : IComponentData { public float Amount; }
```

### 2. Create Systems (Logic)

Systems operate on entities with specific component combinations:

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

### 3. Use Jobs for Parallelism

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

### 4. Entity Queries

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
        // Process enemies...
    }
}
```

### 5. Shared Components (Rendering)

```csharp
public struct SpriteRenderer : ISharedComponentData
{
    public Texture2D Texture;
    public Material Material;
}

// Entities with same shared component are grouped together
```

## Best Practices

- **Keep components small** — single responsibility
- **Avoid managed references** in components (use Entity references)
- **Use Burst** for math-heavy jobs
- **Batch entities** by shared components for rendering
- **Profile with Unity Profiler** — measure before optimizing

## Common Pitfalls

- Forgetting to mark jobs with `[BurstCompile]`
- Using `foreach` instead of `IJobEntity` for large datasets
- Creating too many systems — group related logic
- Not disposing NativeArrays and other native containers

## Examples

### Spawning Entities

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

### Health and Death

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

## Validation

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
