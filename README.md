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

# Define some simple components to start with.
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

# All components must be registered with the engine.
# Component registration must use the class symbol (i.e. do not use the component name attribute).
ecs.register_component(Position)
ecs.register_component(Velocity)
ecs.register_component(Frozen)

# Tell the engine to make an entity.
# You can call `entity.uid` to get the entity's unique ID.
entity = ecs.create_entity()

# Add components to the entity.
# Once a component is registered, it can be accessed using the class symbol, but the name
# attribute can also be used. The component name is not case-sensitive.
entity.add(Position)
entity.add("Velocity")
entity.add("FROZEN")

# Create a query that tracks all components that have both a `Position` and `Velocity`
# component, but not a a `Frozen` component. A query can have any combination of the
# `all_of`, `any_of`, and `none_of` quantifiers.
kinematics = ecs.create_query(
    all_of = ['POSITION', 'VELOCITY'],
    none_of = ['FROZEN']
    )

def loop(dt):
    # Loop over the result set to update the position for all entities in the query.
    # The query will always return an up-to-date list containing entities that match.
    for entity in kinematics.result:
        entity['POSITION'].x += entity['VELOCITY'].x * dt
        entity['POSITION'].y += entity['VELOCITY'].y * dt
```
