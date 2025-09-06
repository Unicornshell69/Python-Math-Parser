from __future__ import annotations
from lexer.tokens import Token, TokenType
from lexer.lexer import tokenize
from .nodes import Expression, CalculatorMode
from .bindingPower import BindingPower
from .parsingFunctions import parseExpressionStatement



class Parser:
    def __init__(self):
        self.tokens:list[Token] = []
        self.position = 0
        self.mode:CalculatorMode = CalculatorMode.scientific

    def parse(self, sourcecode:str):
        self.position = 0
        self.tokens = tokenize(sourcecode)

        #print(self.tokens)

        return parseExpressionStatement(self)
    
    
    def current_token(self) -> Token:
        return self.tokens[self.position]
    
    def token_at_offset(self, offset:int) -> Token:
        return self.tokens[self.position + offset]
    

    def advance(self, offset = 1) -> Token:
        token = self.tokens[self.position]
        self.position += offset
        return token
    
    def has_token(self) -> bool:
        return self.position < len(self.tokens)


    def expect(self, expectedTypes:list[TokenType]|TokenType, ignoredTypes:list[TokenType]|TokenType = [], advance:bool = True) -> tuple[bool, Token]:

        ignored = list(ignoredTypes) if not isinstance(ignoredTypes,list) else ignoredTypes
        expected = list(expectedTypes) if not isinstance(expectedTypes, list) else expectedTypes

        expected_found = False

        i = 0
        while self.has_token():
            token = self.token_at_offset(i)

            if token.type not in ignored:
                if token.type in expected:
                    expected_found = True
                
                else:
                    raise Exception(f"Unexpected token found at position {self.position+i}: {token}")

                break
            i+=1

        token = self.tokens[i+self.position]
        if advance:
            self.advance(i+1)

        return (expected_found, token)

#Import after class init

#from .parsingFunctionMaps import get_led, get_nud, get_stmt