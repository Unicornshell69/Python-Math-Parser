def Enum(cls):
    """Auto-increments class attributes for an enum. Supports manually setting element values.
    Set the default value of your attributes to None, or any non-int value, to allow them to be used."""
    enum_names = {}
    # Auto-Increment
    index = 0
    for name, val in vars(cls).items():
        if not name.startswith("__") and not callable(val):
            if isinstance(val, int) and index < val:
                index = val
            setattr(cls, name, index)
            enum_names[index] = name
            index += 1

    if issubclass(cls, enum):
        cls._enum_names = enum_names
    del enum_names

    return cls

_ = None

class enum:
    """Adds the `name` method if the @Enum decorator is used"""
    @classmethod
    def name(cls, value:int) -> str:
        if not hasattr(cls, "_enum_names"):
            raise Exception("The enum must use @Enum for the `name` method to be initialized")
        return cls._enum_names[value]