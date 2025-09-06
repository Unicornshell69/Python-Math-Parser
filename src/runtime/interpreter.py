from parser.nodes import (
    Statement,
    ExpressionStatement, 
    Expression, 
    NumberExpression, 
    PrefixExpression, 
    BinaryExpression, 
    IdentifierExpression,
    IdentifierImplicitMulExpression,
    PostfixExpression,
    CallExpression,
    ASTNodeKind)
from lexer.tokens import Token, TokenType
#from .values import ValueKind, BinValue, FloatingValue, IntegerValue, Value
from math import gamma, factorial
from .natives import METHODS, CONSTANTS


class function:...

EVALFUNCTIONS:dict[ASTNodeKind, function] = {}

def TODO(node: Statement):
  print(f"This AST node type \"{ASTNodeKind.name(node.kind)}\" is under construction.")

def bind_evaluate(node:ASTNodeKind):
    def decorator(func):
        EVALFUNCTIONS[node] = func
        return func

    return decorator


def evaluate(node:Statement) -> float:
    eval_func = EVALFUNCTIONS.get(node.kind)
    if eval_func == None:
        raise Exception(f"The AST Node \"{ASTNodeKind.name(node.kind)}\" is not setup for interpretation (╯‵□′)╯︵┻━┻")

    return eval_func(node)


@bind_evaluate(ASTNodeKind.ExpressionStatement)
def eval(node:ExpressionStatement):
    return evaluate(node.expression)

@bind_evaluate(ASTNodeKind.FloatExpression)
def eval(node:NumberExpression):
    return node.value

@bind_evaluate(ASTNodeKind.PrefixExpression)
def eval(node:PrefixExpression):
    prefix = node.prefix.type
    if prefix == TokenType.Subtract:
        return - evaluate(node.right)
    
    elif prefix == TokenType.Not:
        return ~evaluate(node.right)
    
    TODO(node)

@bind_evaluate(ASTNodeKind.PostfixExpression)
def eval(node:PostfixExpression):
    postfix = node.postfix.type
    if postfix == TokenType.Factorial:
        #gamma is factorial for floats
        return gamma(evaluate(node.argument) + 1)
    
    TODO(node)


@bind_evaluate(ASTNodeKind.BinaryExpression)
def eval(node:BinaryExpression):
    return calculateBinary(evaluate(node.left),node.operator,evaluate(node.right))


# Use default python type errors. The parser will either create float or int NumberNodes
def calculateBinary(left:int|float, operator:Token, right:int|float):
    op = operator.type
    isint = (isinstance(left, int) and isinstance(right, int))

    if op == TokenType.Add:
        return left + right
    
    elif op == TokenType.Subtract:
        return left - right
    
    elif op == TokenType.Multiply:
        return left * right
    
    elif op == TokenType.Divide:
        if isint:
            #do intdiv for ints
            return left // right
        else:
            return left / right
    
    elif op == TokenType.Modulus:
        return left % right
    
    elif op == TokenType.SciNotation:
        return left*10**right
    
    elif op == TokenType.Exponent:
        return left**right
    
    #bitwise operations, cannot be done on floats
    elif isint:
        if op == TokenType.LShift:
            return left << right
        
        elif op == TokenType.RShift:
            return left >> right
        
        elif op == TokenType.And:
            return left & right
        
        elif op == TokenType.Or:
            return left | right
        
        elif op == TokenType.Xor:
            return left ^ right
        
        else:
            raise Exception(f"Cannot resolve {TokenType.name(op)} for {type(left)} and {type(right)}") 
            
    else:
        raise Exception(f"Cannot resolve {TokenType.name(op)} for {type(left)} and {type(right)}") 



@bind_evaluate(ASTNodeKind.CallExpression)
def eval(node:CallExpression):
    if node.caller.kind == ASTNodeKind.IdentifierExpression:
        #IdentifierExpression
        constant = CONSTANTS.get(node.caller.value)
        method = METHODS.get(node.caller.value)
        if constant == None:
            if method == None:
                raise Exception(f"Unknown identifier \"{node.caller.value}\"")
            else:
                return handleMethod(node)
        # else, do implicit mul
        



    # implicit mul
    if len(node.arguments) == 1:
        return evaluate(node.caller) * evaluate(node.arguments[0])
    
    else:
        raise Exception("Idfk")

# Should only happen for constants called by evaluate in CallExpression
# There are no "free" identifiers
@bind_evaluate(ASTNodeKind.IdentifierExpression)
def eval_Constant(node:IdentifierExpression):
    return CONSTANTS[node.value]

@bind_evaluate(ASTNodeKind.IdentifierImplicitMulExpression)
def eval(node:IdentifierImplicitMulExpression):
    return evaluate(node.left) * evaluate(node.identifier)

# If identifier is function name, call it and return
def handleMethod(node:CallExpression):
    method = METHODS[node.caller.value]
    return method(*[evaluate(arg) for arg in node.arguments])

