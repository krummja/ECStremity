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
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Frozen(Component):
    """Tag component denoting a frozen character."""
```

 All components must be registered with the engine. Component registration must use the class symbol (i.e. do not use the component name attribute).

```python
ecs.register_component(Position)
ecs.register_component(Velocity)
ecs.register_component(Frozen)
```

Instruct the engine to make a new entity, then add components to it.
Once a component is registered, it can be accessed using the class symbol or a string representing the class. The name attribute is not case-sensitive.

```python
entity = ecs.create_entity()

entity.add(Position)
entity.add("Velocity")
```

The ecstremity library has no actual "system" class. Instead, instruct the engine to produce a query. For example, make a query that tracks all components that have both a `Position` and `Velocity` component, but not a `Frozen` component. A query can have any combination of the `all_of`, `any_of`, and `none_of` quantifiers.

```python
kinematics = ecs.create_query(
    all_of = ['Position', 'Velocity'],
    none_of = ['Frozen']
    )
```

Loop over the result set to update the position for all entities in the query. The query will always reutrn an up-to-date list containing entities that match.

```python
def loop(dt):
    for entity in kinematics.result:
        entity['Position'].x += entity['Velocity'].x * dt
        entity['Position'].y += entity['Velocity'].y * dt
```


## Changelog

### v.1.0.1
Initial release

### v.1.0.2
- Changed how component names are handled. Previously creating a component required setting a class variable `name` 
  with a string in all-caps that is identical to the class name, e.g. if a component was created as `class Position`,
  the class required a variable `name = "POSITION"`. Now all components inherit from `componentmeta` which handles
  this automatically. All references to component names inside the engine also convert the name string to the required
  casing.

- Added the ability to make use of the `EntityEvent` system. Use `entity.fire_event('event_name', data)` where data can
  be any object (typically a dict) that you want to pass to an entity's components. The `'event_name'` should have a
  corresponding `on_event_name` method on one or more components of the entity, which will have the event passed to it.
  
- Added a prefab system. This is a work-in-progress addition, but essentially you can now define component structures
  that can be applied all at once to an entity, allowing for templating of entity types.
  
### v.1.0.3
- Miscellaneous fixes and performance updates.
- Fixed an issue with queries not updating their cache when components are added/removed from an entity.

### v.1.0.4
- Added an `EngineAdapter` class that allows for passing in a reference to the game client.
- Added entity cloning. Use `entity.clone()` to make a copy of an entity with all attached components.
- Added an `EventData` class to pass in as the data argument of `entity.fire_event`. This base class is meant to be
  extensible, but by default it has five optional parameters:
  - `instigator: Entity`   
    Used to pass reference to the entity that fired the event.
  - `target: Union[Tuple[int, int], Entity]`  
    Used to pass reference to an entity or position that can be used for various things, like forwarding an event or querying for data. 
  - `interactions: List[Dict[str, str]]`  
    Used to get back a list of interactions from a component. Typical format is `{'name': 'event_name', 'event': 'on_event_method'}`.
  - `callback: Callable[[Any], Any]`  
    A callback that can be executed inside a component.
  - `cost: float`  
    An event cost, for use with energy-based action systems.
- Added `EntityEvent.route` to trigger forwarding of an event to a target entity. For example, in my project game [Anathema](https://github.com/krummja/Anathema),
I use this to query a target entity for interactions, say when bumping into it:

```python
class Legs(Component):
  # ...
  def on_try_move(self, evt: EntityEvent) -> None:
      if self.area.is_blocked(*evt.data.target):
          if self.area.is_interactable(*evt.data.target):
              self.entity.fire_event('try_interact', evt.data)  
```

and then in a separate component:

```python
class Brain(Component):
    # ...
    def on_try_interact(self, evt: EntityEvent) -> None:
        evt.data.instigator = self.entity
        evt.data.interactions = []
        
        target: Entity = self.client.interaction_system.get(*evt.dat.target)
        routed_evt: EntityEvent = evt.route(
          new_event='get_interactions', 
          target=target
        )
        routed_evt.handle()
```

Finally, on a component attached to the target entity, I might have:

```python
class Container(Component):
    # ...
    def on_get_interactions(self, evt) -> None:
        if self._is_open:
            evt.data.interactions.append({
              "name": "Close",
              "event": "try_close_container"
            })
        # ...
```

Which requires a corresponding `Container.on_try_close_container`, and so forth.

### v.1.0.5
- Radically improved performance by switching to bitmasking for component registration and querying.

### v.1.0.6
- Implemented a prefab system.
