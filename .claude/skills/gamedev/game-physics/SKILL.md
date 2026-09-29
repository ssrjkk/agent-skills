---
name: game-physics
description: "Implement 2D/3D game physics: rigid bodies, collisions, constraints, raycasting, and performance optimization. Use for realistic game mechanics."
category: gamedev
tags: [physics, game-dev, rigid-body, collision, raycast, simulation, 2d, 3d]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Game Physics

> Building realistic game physics with collision detection, rigid bodies, and constraints.

## Quick Start

```python
# Basic rigid body setup (example with common physics engine pattern)
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

## When to Use

- Building platformers, shooters, or physics-based puzzles
- Implementing vehicle simulation or character controllers
- When you need realistic object interactions
- Optimizing physics for mobile or VR performance

## Step-by-Step

### 1. Choose Your Physics Scope

Determine what level of physics your game needs:

- **Arcade**: Simple AABB collisions, basic gravity
- **Casual**: Circle/sphere collisions, friction, bounce
- **Realistic**: Full rigid body dynamics, constraints, joints

### 2. Collision Detection

Implement broad phase then narrow phase:

```python
def broad_phase_aabb(obj_a, obj_b):
    """Quick rejection using bounding boxes."""
    return not (
        obj_a.max_x < obj_b.min_x or obj_a.min_x > obj_b.max_x or
        obj_a.max_y < obj_b.min_y or obj_a.min_y > obj_b.max_y
    )

def narrow_phase_circle(c1, c2):
    """Precise circle-circle collision."""
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance < (c1.radius + c2.radius)
```

### 3. Collision Response

Handle what happens after collision:

```python
def resolve_collision(body_a, body_b, normal, depth):
    """Simple elastic collision response."""
    relative_velocity = tuple(b - a for a, b in zip(body_a.velocity, body_b.velocity))
    velocity_along_normal = sum(r * n for r, n in zip(relative_velocity, normal))

    if velocity_along_normal > 0:
        return  # Objects separating

    restitution = 0.5  # Bounciness
    impulse = -(1 + restitution) * velocity_along_normal
    impulse /= (1 / body_a.mass + 1 / body_b.mass)

    impulse_vector = tuple(impulse * n for n in normal)
    body_a.velocity = tuple(v - impulse / body_a.mass for v in impulse_vector)
    body_b.velocity = tuple(v + impulse / body_b.mass for v in impulse_vector)
```

### 4. Constraints and Joints

```python
class DistanceConstraint:
    """Keep two bodies at fixed distance."""
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

### 5. Raycasting

```python
def raycast(origin, direction, objects, max_distance):
    """Find first object hit by ray."""
    closest_hit = None
    closest_distance = max_distance

    for obj in objects:
        hit, distance = obj.ray_intersection(origin, direction)
        if hit and distance < closest_distance:
            closest_distance = distance
            closest_hit = obj

    return closest_hit, closest_distance
```

## Best Practices

- **Use spatial partitioning** (quadtree, octree) for broad phase
- **Fixed timestep** for deterministic physics (important for multiplayer)
- **Sleeping bodies** — disable physics for stationary objects
- **Continuous collision detection** for fast-moving objects
- **Separate physics and rendering** — run physics at fixed rate

## Common Pitfalls

- Tunneling (fast objects passing through walls) — use CCD or smaller timesteps
- Floating point errors accumulating — use position correction
- Too many collision checks — optimize with spatial structures
- Variable timestep causing instability — use fixed timestep with interpolation

## Examples

### Platformer Character Controller

```python
class CharacterController:
    def __init__(self):
        self.grounded = False
        self.jump_force = 10
        self.move_speed = 5
        self.gravity = -20

    def update(self, input, dt):
        # Horizontal movement
        self.velocity.x = input.horizontal * self.move_speed

        # Jump
        if input.jump and self.grounded:
            self.velocity.y = self.jump_force
            self.grounded = False

        # Gravity
        self.velocity.y += self.gravity * dt
```

### Vehicle Physics

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

## Validation

```python
# Test your physics implementation
def test_collision_detection():
    body_a = RigidBody(1, (0, 0), (0, 0))
    body_b = RigidBody(1, (1, 0), (0, 0))
    assert detect_collision(body_a, body_b, radius=0.6)

def test_gravity():
    body = RigidBody(1, (0, 10), (0, 0))
    body.apply_force((0, -9.8))
    body.update(1.0)
    assert body.velocity[1] < 0  # Falling
```
