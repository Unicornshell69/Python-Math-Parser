from lexer.tokens import Token, TokenType
from utils.enumClass import Enum, enum, _


# Used to decide whether to parse all numbers as floats or ints
class CalculatorMode:
    programmer = 0
    scientific = 1

@Enum
class ASTNodeKind(enum):
    ExpressionStatement = _
    BinaryExpression = _
    PrefixExpression = _
    PostfixExpression = _
    NumberExpression = _
    IdentifierExpression = _
    IdentifierImplicitMulExpression = _
    CallExpression = _

class ASTNode:
    """Parent object to statements and expressions"""
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if key == "kind":
                result[key] = ASTNodeKind.name(value)
            else:
                result[key] = self._convert(value)
        return result

    def _convert(self, value):
        #recursive convert
        if isinstance(value, ASTNode):
            return value.to_dict()
        #recursive convert in lists (for call args)
        elif isinstance(value, list):
            return [self._convert(v) for v in value]
        # Returns the string for tokens. The only printed token is for binary operators and prefix
        elif isinstance(value, Token):
            return str(value.value)
        else:
            return value

class Statement(ASTNode):
    def __init__(self, kind:ASTNodeKind):
        self.kind = kind

class Expression(ASTNode):
    def __init__(self, kind:ASTNodeKind):
        self.kind = kind

# Statements
class ExpressionStatement(Statement):
    def __init__(self, expression:Expression):
        super().__init__(ASTNodeKind.ExpressionStatement)
        self.expression = expression

    def __repr__(self) -> str:
        return f"Expression: {self.expression}"

# Expressions
class BinaryExpression(Expression):
    def __init__(self, left:Expression, operator:Token, right:Expression):
        super().__init__(ASTNodeKind.BinaryExpression)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f"Left: {self.left}\nOperator: {TokenType.name(self.operator.type)}\nRight: {self.right}"

class PrefixExpression(Expression):
    def __init__(self, prefix:Token, right:Expression):
        super().__init__(ASTNodeKind.PrefixExpression)
        self.prefix = prefix
        self.right = right

    def __repr__(self) -> str:
        return f"Prefix: {self.prefix}\nRight: {self.right}"

class PostfixExpression(Expression):
    def __init__(self, postfix:Token, argument:Expression):
        super().__init__(ASTNodeKind.PostfixExpression)
        self.postfix = postfix
        self.argument = argument

    def __repr__(self) -> str:
        return f"Postfix: {self.postfix}\nLeft: {self.argument}"

#? The "Binary" type allows for bitshifts and bitwise expressions, used for programmer mode. All
#? This means all Number nodes need to either be floats, or ints
class NumberExpression(Expression):
    def __init__(self, value:float|int):
        super().__init__(ASTNodeKind.NumberExpression)
        self.value = value

    def __repr__(self) -> str:
        return f"Value: {self.value}"
    
# class ConstantExpression(NumberExpression):
#     def __init__(self, value:float):
#         super().__init__(value)

class IdentifierExpression(Expression):
    """For function calls or constants"""
    def __init__(self, value:str):
        super().__init__(ASTNodeKind.IdentifierExpression)
        self.value = value

    def __repr__(self) -> str:
        return f"Identifier: {self.value}"

class IdentifierImplicitMulExpression(Expression):
    """For function calls or constants"""
    def __init__(self, identifier:IdentifierExpression, left:Expression):
        super().__init__(ASTNodeKind.IdentifierImplicitMulExpression)
        self.identifier = identifier
        self.left = left

    def __repr__(self) -> str:
        return f"Identifier: {self.value}"
    
class CallExpression(Expression):
    def __init__(self, caller:Expression, arguments:list[Expression]):
        super().__init__(ASTNodeKind.CallExpression)
        self.caller = caller
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"Caller: {self.caller}\nArgs: {self.arguments}"