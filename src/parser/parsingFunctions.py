from __future__ import annotations
#from .parsingFunctionMaps import nud, led
from lexer.tokens import Token, TokenType
from .nodes import (Statement,
                    ExpressionStatement, 
                    Expression, 
                    NumberExpression,
                    PrefixExpression, 
                    BinaryExpression, 
                    IdentifierExpression,
                    PostfixExpression,
                    IdentifierImplicitMulExpression,
                    CallExpression,
                    CalculatorMode)
from .bindingPower import BindingPower

# lazy ciruclar import fix (parser is not initalized)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .parser import Parser

from lexer.tokens import TokenType, Token
from .bindingPower import BindingPower
#from .parsingFunctions import parseBinaryExpression, parseNumberExpression

#typing
class function:...
STMT_MAP:dict[TokenType,function] = {}
NUD_MAP:dict[TokenType,tuple[function, BindingPower]] = {}
LED_MAP:dict[TokenType,tuple[function, BindingPower]] = {}

def get_led(token:Token) -> tuple[bool, function, int]:
    item = LED_MAP.get(token.type)
    if item == None:
        #& Return the highest binding power, so the missing LED Handler error isn't skipped in the parseExpression loop
        return False, None, BindingPower.primary
    return True, item[0], item[1]

def get_nud(token:Token) -> tuple[bool, function, int]:
    item = NUD_MAP.get(token.type)
    if item == None:
        return False, None, BindingPower.primary
    return True, item[0], item[1]

#! TODO
def get_stmt(token:Token) -> function:
    item = STMT_MAP.get(token.type)
    return item

# Adding handlers
def add_led(type:TokenType, bp:BindingPower, handler:function):
    LED_MAP[type] = (handler, bp)

def add_nud(type:TokenType, bp:BindingPower, handler:function):
    NUD_MAP[type] = (handler, bp)

def add_stmt(type:TokenType, handler:function):
    STMT_MAP[type] = handler



# ----------------------------- Parsing ----------------------------- #
#// def parseStatement(parser: Parser):
#//     stmt_handler = get_stmt(parser.current_token())
#//     if stmt_handler != None:
#//         return stmt_handler(parser)
#//     
#//     return parseExpressionStatement(parser)


def parseExpressionStatement(parser:Parser):
    expr = parseExpression(parser, BindingPower.default)
    
    return ExpressionStatement(expr)


def parseExpression(parser:Parser, bp:BindingPower) -> Expression:
    exists, nud_handler, nud_bp = get_nud(parser.current_token())
    
    if not exists:
        raise Exception(f"Expected NUD handler for token {TokenType.name(parser.current_token().type)}")

    left = nud_handler(parser)

    # There is no EOL token, so you need to stop when tokens are done
    while (parser.has_token() and (led := get_led(parser.current_token()))[2] > bp):
        exists, led_handler, led_bp = led
        if not exists:
            raise Exception(f"Expected LED handler for token {TokenType.name(parser.current_token().type)}")

        left = led_handler(parser, left, led_bp)
    
    return left

def parseGroupingExpression(parser:Parser) -> Expression:
    parser.expect([TokenType.OpenParen,])
    expression = parseExpression(parser, BindingPower.default)
    parser.expect([TokenType.CloseParen,])
    return expression

def parsePrefixExpression(parser:Parser) -> PrefixExpression:
    prefix = parser.advance() #assume we have a unary minus or NOT
    right = parseExpression(parser, BindingPower.default)

    return PrefixExpression(prefix, right)

def parsePostfixExpression(parser:Parser, left:Expression, bp:BindingPower) -> PostfixExpression:
    postfix = parser.advance() #assume we have a factorial

    return PostfixExpression(postfix, left)


def parseNumberExpression(parser:Parser) -> NumberExpression:
    # Convert [Number,Decimal,Number] to float
    num = int(parser.advance().value)

    #^ I may need to raise an error when a float is written in programmer mode
    #^ Currently it raises a LED handler error for the decimal
    
    if parser.mode == CalculatorMode.scientific:
        if parser.has_token() and parser.current_token().type == TokenType.Decimal:
            parser.advance() #& Eat decimal
            exists, token = parser.expect([TokenType.Number])
            num += int(token.value) / (10 ** len(token.value))
        # Convert to float for scientific (automatic if you have a fractional part)
        return NumberExpression(float(num))
    
    # Keep as integer for int/bin/hex/oct/etc.
    return NumberExpression(num)
        


def parseBinaryExpression(parser:Parser, left:Expression, bp:BindingPower):
    operator = parser.advance()
    right = parseExpression(parser,bp)

    return BinaryExpression(left, operator, right)


def parseGroupingExpression(parser:Parser) -> Expression:
    parser.expect([TokenType.OpenParen])
    expr = parseExpression(parser, BindingPower.default)
    parser.expect([TokenType.CloseParen])
    return expr

def parseCallExpression(parser:Parser, left:Expression|IdentifierExpression, bp:BindingPower) -> CallExpression:
    parser.expect([TokenType.OpenParen])

    first_arg = True
    args:list[Expression] = []
    while parser.current_token().type != TokenType.CloseParen:
        if not first_arg:
            parser.expect([TokenType.Comma])

        args.append(parseExpression(parser, BindingPower.default))

        first_arg = False

    parser.expect([TokenType.CloseParen])

    return CallExpression(left, args)

def parseIdentifierExpression(parser:Parser) -> IdentifierExpression:
    if parser.mode == CalculatorMode.programmer:
        token = parser.advance()
        #only allow up to hexadecimal. I will need to convert to number somehow
        if token.value not in ["A","B","C","D","E","F"]:
            raise Exception(f"Identifier {token.value} not allowed in programmer mode")
        
        IdentifierExpression(token.value)
    
    else:
        return IdentifierExpression(parser.advance().value)

#Identifier as led, used in something like "(3)pi(5)"
def parseIdentifierImplicitMul(parser:Parser, left:Expression, bp:BindingPower) -> IdentifierExpression:
    #parser.advance()
    return IdentifierImplicitMulExpression(parseExpression(parser, BindingPower.default), left)

#* For implict multiplication, check if a CallExpression isn't preceded by an identifier, and that there is only a single expression argument.
# I will also need to handle "constant" identifiers, which are replaced by numeric values.






# ------------------------------- Maps ------------------------------- #
#~ Binary Operators
add_led(TokenType.Add, BindingPower.additive, parseBinaryExpression)
add_led(TokenType.Subtract, BindingPower.additive, parseBinaryExpression)

add_led(TokenType.Multiply, BindingPower.multiplicative, parseBinaryExpression)
add_led(TokenType.Divide, BindingPower.multiplicative, parseBinaryExpression)
add_led(TokenType.Modulus, BindingPower.multiplicative, parseBinaryExpression)

add_led(TokenType.SciNotation, BindingPower.exponentiation, parseBinaryExpression)

add_led(TokenType.Exponent, BindingPower.exponentiation, parseBinaryExpression)

#~ Bit-wise Binary Operators
add_led(TokenType.And, BindingPower.bitwise_and, parseBinaryExpression)
add_led(TokenType.Or, BindingPower.bitwise_or, parseBinaryExpression)
add_led(TokenType.Xor, BindingPower.bitwise_xor, parseBinaryExpression)
add_led(TokenType.LShift, BindingPower.bitwise_shift, parseBinaryExpression)
add_led(TokenType.RShift, BindingPower.bitwise_shift, parseBinaryExpression)

#~ Prefix/Postfix
add_nud(TokenType.Subtract, BindingPower.prefix, parsePrefixExpression)
add_nud(TokenType.Not, BindingPower.prefix, parsePrefixExpression)
add_led(TokenType.Factorial, BindingPower.postfix, parsePostfixExpression)

#~ Number
add_nud(TokenType.Number, BindingPower.primary, parseNumberExpression)

#~ Parentheses
add_nud(TokenType.OpenParen, BindingPower.grouping, parseGroupingExpression)
add_led(TokenType.OpenParen, BindingPower.call, parseCallExpression)

#~ Identifier
add_nud(TokenType.Identifier, BindingPower.primary, parseIdentifierExpression)
add_led(TokenType.Identifier, BindingPower.primary, parseIdentifierImplicitMul)
