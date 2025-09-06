from dataclasses import dataclass
from utils.enumClass import _, Enum, enum

@Enum
class TokenType(enum):
    Number = _
    Identifier = _     # log, ln, root, etc. Produce functions with identifier+openparent+expression+comma+expression+closeparen

    #~ Arithmetics Operators
    Add = _          #| +
    Subtract = _     #| -
    Multiply = _     #| *
    Divide = _       #| /
    Exponent = _     #| **
    Modulus = _      #| %
    Factorial = _    #| !
    SciNotation = _  #| exp, idk where it should go

    #~ Logical Operators
    And = _          #| AND / &
    Or = _           #| OR / |
    Xor = _          #| XOR
    Not = _          #| NOT / ~
    LShift = _       #| <
    RShift = _       #| >


    #~ Syntax
    OpenParen = _    #| (
    CloseParen = _   #| )
    Comma = _        #| ,
    Decimal = _      #| .
    AbsSign = _      #| |, may remove

    INVALID = _


#TokenTypeNames:tuple[str] = tuple([k for k,v in vars(TokenType).items() if not k.startswith("__")  and not callable(v)])

#I wanna make tokens only have a value if needed. Can't do that yet
class NoValueTokenType:...

@dataclass
class Token:
    type:TokenType
    value:str
    start:int

    @property
    def end(self):
        return self.start + len(self.value)

    def __repr__(self) -> str:
        return f"{TokenType.name(self.type)}({self.value})"



ArithmeticsMap = {
    "+":TokenType.Add,
    "-":TokenType.Subtract,
    "*":TokenType.Multiply,
    "/":TokenType.Divide,
    "%":TokenType.Modulus,
    "!":TokenType.Factorial,
    "exp":TokenType.SciNotation,
    #// "^":TokenType.Exponent,
    "**":TokenType.Exponent}

ArithemticKeys = ArithmeticsMap.keys()

SyntaxMap = {
    "(":TokenType.OpenParen,
    ")":TokenType.CloseParen,
    ",":TokenType.Comma,
    ".":TokenType.Decimal,
    "|":TokenType.AbsSign
}

SyntaxKeys = SyntaxMap.keys()

BitArithmeticsMap = {
    "AND":TokenType.And,
    "OR":TokenType.Or,
    "XOR":TokenType.Xor,
    "NOT":TokenType.Not,
    "<":TokenType.LShift,
    ">":TokenType.RShift
    }

BitArithmeticKeys = BitArithmeticsMap.keys()

#//FunctionIdentifierList = (
#//    "abs",
#//    "exp",
#//    "root",
#//    "sqrt",
#//    "log",
#//    "ln",
#//    "negate")

#//ConstantList = (
#//    "pi",
#//    "e"
#//)


WHITESPACES = (" ", "\t")
