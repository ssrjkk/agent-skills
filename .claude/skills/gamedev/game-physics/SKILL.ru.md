---
name: game-physics
description: "Реализация 2D/3D игровой физики: твёрдые тела, столкновения, ограничения, рейкастинг и оптимизация производительности. Для реалистичной игровой механики."
category: gamedev
tags: [physics, game-dev, rigid-body, collision, raycast, simulation, 2d, 3d]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Физика в играх

> Создание реалистичной игровой физики с обнаружением столкновений, твёрдыми телами и ограничениями.

## Быстрый старт

```python
# Базовая настройка твёрдого тела (паттерн для типичного физического движка)
class RigidBody:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = (0, 0, 0)

    def apply_force(self, force):
        self.acceleration = tuple(f / self.mass for f in force)

    def update(self, dt):
        self.velocity = tuple(v + a * dt for v, a in zip(self.velocity, self.acceleration))
        self.position = tuple(p + v * dt for p, v in zip(self.position, self.velocity))
```

## Когда использовать

- Создание платформеров, шутеров или головоломок с физикой
- Реализация симуляции транспорта или контроллеров персонажей
- Когда нужно реалистичное взаимодействие объектов
- Оптимизация физики для мобильных или VR

## Пошагово

### 1. Определите масштаб физики

Определите, какой уровень физики нужен вашей игре:

- **Аркадная**: простые AABB столкновения, базовая гравитация
- **Казуальная**: круговые/сферические столкновения, трение, отскок
- **Реалистичная**: полная динамика твёрдых тел, ограничения, суставы

### 2. Обнаружение столкновений

Реализуйте широкую фазу, затем узкую:

```python
def broad_phase_aabb(obj_a, obj_b):
    """Быстрое отсечение по ограничивающим коробкам."""
    return not (
        obj_a.max_x < obj_b.min_x or obj_a.min_x > obj_b.max_x or
        obj_a.max_y < obj_b.min_y or obj_a.min_y > obj_b.max_y
    )

def narrow_phase_circle(c1, c2):
    """Точное столкновение круг-круг."""
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance < (c1.radius + c2.radius)
```

### 3. Реакция на столкновение

Обработка того, что происходит после столкновения:

```python
def resolve_collision(body_a, body_b, normal, depth):
    """Простая упругая реакция на столкновение."""
    relative_velocity = tuple(b - a for a, b in zip(body_a.velocity, body_b.velocity))
    velocity_along_normal = sum(r * n for r, n in zip(relative_velocity, normal))

    if velocity_along_normal > 0:
        return  # Объекты разделяются

    restitution = 0.5  # Упругость
    impulse = -(1 + restitution) * velocity_along_normal
    impulse /= (1 / body_a.mass + 1 / body_b.mass)

    impulse_vector = tuple(impulse * n for n in normal)
    body_a.velocity = tuple(v - impulse / body_a.mass for v in impulse_vector)
    body_b.velocity = tuple(v + impulse / body_b.mass for v in impulse_vector)
```

### 4. Ограничения и суставы

```python
class DistanceConstraint:
    """Поддержание фиксированного расстояния между двумя телами."""
    def __init__(self, body_a, body_b, distance):
        self.body_a = body_a
        self.body_b = body_b
        self.distance = distance

    def solve(self):
        dx = self.body_b.position[0] - self.body_a.position[0]
        dy = self.body_b.position[1] - self.body_a.position[1]
        current_dist = (dx * dx + dy * dy) ** 0.5
        error = current_dist - self.distance

        if current_dist == 0:
            return

        normal = (dx / current_dist, dy / current_dist)
        correction = error / 2

        self.body_a.position = (
            self.body_a.position[0] + normal[0] * correction,
            self.body_a.position[1] + normal[1] * correction
        )
        self.body_b.position = (
            self.body_b.position[0] - normal[0] * correction,
            self.body_b.position[1] - normal[1] * correction
        )
```

### 5. Рейкастинг

```python
def raycast(origin, direction, objects, max_distance):
    """Поиск первого объекта, пересечённого лучом."""
    closest_hit = None
    closest_distance = max_distance

    for obj in objects:
        hit, distance = obj.ray_intersection(origin, direction)
        if hit and distance < closest_distance:
            closest_distance = distance
            closest_hit = obj

    return closest_hit, closest_distance
```

## Лучшие практики

- **Используйте пространственное разбиение** (quadtree, octree) для широкой фазы
- **Фиксированный шаг времени** для детерминированной физики (важно для мультиплеера)
- **Спящие тела** — отключайте физику для неподвижных объектов
- **Непрерывное обнаружение столкновений** для быстро движущихся объектов
- **Разделяйте физику и рендеринг** — запускайте физику с фиксированной частотой

## Типичные ошибки

- Туннелирование (быстрые объекты проходят сквозь стены) — используйте CCD или меньший шаг времени
- Накопление ошибок плавающей точки — используйте коррекцию позиции
- Слишком много проверок столкновений — оптимизируйте пространственными структурами
- Переменный шаг времени вызывает нестабильность — используйте фиксированный шаг с интерполяцией

## Примеры

### Контроллер персонажа для платформера

```python
class CharacterController:
    def __init__(self):
        self.grounded = False
        self.jump_force = 10
        self.move_speed = 5
        self.gravity = -20

    def update(self, input, dt):
        # Горизонтальное движение
        self.velocity.x = input.horizontal * self.move_speed

        # Прыжок
        if input.jump and self.grounded:
            self.velocity.y = self.jump_force
            self.grounded = False

        # Гравитация
        self.velocity.y += self.gravity * dt
```

### Физика транспорта

```python
class Vehicle:
    def apply_engine_force(self, throttle):
        force = throttle * self.engine_power
        self.apply_force_to_rear_wheels(force)

    def apply_brakes(self, brake_force):
        self.apply_friction_to_all_wheels(brake_force)

    def steer(self, angle):
        self.front_wheel_angle = angle
```

## Валидация

```python
# Тестирование реализации физики
def test_collision_detection():
    body_a = RigidBody(1, (0, 0), (0, 0))
    body_b = RigidBody(1, (1, 0), (0, 0))
    assert detect_collision(body_a, body_b, radius=0.6)

def test_gravity():
    body = RigidBody(1, (0, 10), (0, 0))
    body.apply_force((0, -9.8))
    body.update(1.0)
    assert body.velocity[1] < 0  # Падает
```
