from utils.enumClass import Enum, enum, _


# The code below is currently unused
@Enum
class ValueKind(enum):
    floatingPoint = _
    integer = _
    binary = _

class Value:
    def __init__(self, kind:ValueKind):
        self.kind = kind

    def __repr__(self):
        return f"Value {ValueKind.name(self.kind)}"
    
class BinValue(Value):
    def __init__(self, value:int):
        super().__init__(ValueKind.binary)
        self.value = value

    def __repr__(self):
        return f"Value {ValueKind.name(self.kind)}\n{self.value}"
    
class FloatingValue(Value):
    def __init__(self, value:float):
        super().__init__(ValueKind.floatingPoint)
        self.value = value

    def __repr__(self):
        return f"Value {ValueKind.name(self.kind)}\n{self.value}"
    
class IntegerValue(Value):
    def __init__(self, value:int):
        super().__init__(ValueKind.integer)
        self.value = value