# ECStremity

**ECStremity** is an Entity-Component library. It is a Python port of the JavaScript library [geotic](https://github.com/ddmills/geotic) by Dalton Mills.

- *entity* : a unique id and a collection of components
- *component* : a data container
- *query* : a way to gather collections of entities that match some criteria, for use in systems
- *event* : a message to an entity and its components

## Installation

```
pip install ecstremity
```

## Usage

To start using **ECStremity**, import the library and make some components.

```python
from ecstremity import (Engine, Component)

ecs = Engine()

class Position(Component):
    name: str = "POSITION"
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Velocity(Component):
    name: str = "VELOCITY"
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Frozen(Component):
    name: str = "FROZEN"
```

 All components must be registered with the engine. Component registration must use the class symbol (i.e. do not use the component name attribute).

```python
ecs.register_component(Position)
ecs.register_component(Velocity)
ecs.register_component(Frozen)
```

Instruct the engine to make a new entity, then add components to it.
Once a component is registered, it can be accessed using the class symbol or the name attribute. The name attribute is not case-sensitive.

```python
entity = ecs.create_entity()

entity.add(Position)
entity.add("Velocity")
```

The ecstremity library has no actual "system" class. Instead, instruct the engine to produce a query. For example, make a query that tracks all components that have both a `Position` and `Velocity` component, but not a `Frozen` component. A query can have any combination of the `all_of`, `any_of`, and `none_of` quantifiers.

```python
kinematics = ecs.create_query(
    all_of = ['POSITION', 'VELOCITY'],
    none_of = ['FROZEN']
    )
```

Loop over the result set to update the position for all entities in the query. The query will always reutrn an up-to-date list containing entities that match.

```python
def loop(dt):
    for entity in kinematics.result:
        entity['POSITION'].x += entity['VELOCITY'].x * dt
        entity['POSITION'].y += entity['VELOCITY'].y * dt
```
