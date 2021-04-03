from __future__ import annotations


def build_references(allocator, uid):
    """Returns {component_name: slice or None, ...} for uid."""
    component_names = allocator.names
    get_slice = allocator.allocation_table.slices_from_uid
    slices = (s if s.start != s.stop else None for s in get_slice(uid))
    return dict(zip(component_names, slices))


class Accessor:
    """
    Accessors provide an object-oriented interface for a specific
    entity instance (uid) by providing an object with attributes
    that access the array slices allocated to that uid under
    the hood.
    """

    def __init__(self, uid: int) -> None:
        self._allocator = None
        self.uid = uid
        self._dirty = True
        self._active = True
        self._references = {}

    @property
    def dirty(self) -> bool:
        return self._dirty

    @property
    def references(self):
        return self._references

    def rebuild_references(self, build_ref=build_references):
        """Get up-to-date slices for all of the attributes."""
        self._references = {key: value for key, value in
                            build_ref(self._allocator, self.uid).items() if value is not None}
        self._dirty = False

    def __repr__(self):
        return "<Accessor for uid #%s>" % (self.uid,)


class AccessorFactory:

    def __init__(self, allocator):
        self.allocator = allocator

    def attribute_getter_factory(self, component_name):
        """Generate a getter for this component_name into the Component data array."""
        comp_dict = self.allocator.component_registry

        def getter(accessor, name=component_name, comp_dict=comp_dict):
            if accessor.dirty:
                accessor.rebuild_references()
            selector = accessor.references[name]
            return comp_dict[name][selector]
        return getter

    def attribute_setter_factory(self, component_name):
        """Generate a setter using this object's index to the domain arrays.

        `attr` is the domain's list of this attribute.
        """
        comp_dict = self.allocator.component_registry

        def setter(accessor, data, name=component_name, comp_dict=comp_dict):
            if accessor.dirty:
                accessor.rebuild_references()
            selector = accessor.references[name]
            comp_dict[name][selector] = data
        return setter

    def generate_accessor(self):
        """Return a DataAccessor class that can be instantiated with a
        uid to provide an object oriented interface with the data
        associated with the uid.
        """
        NewAccessor = type('DataAccessor', (Accessor,), {})
        allocator = self.allocator
        getter = self.attribute_getter_factory
        setter = self.attribute_setter_factory

        for name in allocator.names:
            print("Adding property: {}".format(name))
            setattr(NewAccessor, name, property(getter(name), setter(name)))
        NewAccessor._allocator = self.allocator
        return NewAccessor
