from .tokens import Token, TokenType, WHITESPACES
from .tokens import ArithemticKeys, ArithmeticsMap, SyntaxMap, SyntaxKeys, BitArithmeticKeys, BitArithmeticsMap
import re



def tokenize(source:str) -> list[Token]:
    data = TokenizerData(source)
    while not data.isEmpty():
        start = data.position

        if data.peek() in WHITESPACES:
            data.step()
        #~ Number
        #? The decimal part is combined in parseNumberExpression
        elif data.peek().isdigit():
            number = data.slice()
            while not data.isEmpty() and data.peek().isdigit():
                number += data.slice()
            data.addToken(TokenType.Number, number, start)
            

        #~ Parentheses, commas, etc
        elif data.match(*SyntaxKeys):
            matched = data.matched_symbol(*SyntaxKeys)
            data.addToken(SyntaxMap[matched], data.slice(len(matched)), start)

        #~ Add, subtract, etc
        elif data.match(*ArithemticKeys):
            matched = data.matched_symbol(*ArithemticKeys)
            data.addToken(ArithmeticsMap[matched], data.slice(len(matched)), start)

        #~ Bitshift, and, or, etc
        elif data.match(*BitArithmeticKeys):
            matched = data.matched_symbol(*BitArithmeticKeys)
            data.addToken(BitArithmeticsMap[matched], data.slice(len(matched)), start)

        #~ Identifiers (later functions)
        elif data.peek().isalnum():
            ident = ""
            while not data.isEmpty() and data.peek().isalnum():
                ident += data.slice()
            
            data.addToken(TokenType.Identifier, ident, start)

        #~ Unrecognized character handling
        else:
            #print and move forward
            val = data.slice()
            data.addToken(TokenType.INVALID, val, start)
            print(f"\033[91m\033[01m[ERROR]\033[0m Unrecognized character for tokenizing [\033[33m{val}\033[0m]")

    
    #// data.tokens.append(Token(TokenType.EOL,""))
    return data.tokens




class TokenizerData:
    def __init__(self, source:str):
        self.src:str = source
        self.tokens:list[Token] = []
        self.initial_length = len(self.src)


    def step(self, n = 1) -> None:
        """Cuts n characters from the source"""
        self.src = self.src[n:]

    def slice(self, n = 1) -> str:
        """Cuts n characters from the source and returns the cut characters"""
        chars = self.src[0:n]
        self.src = self.src[n:]
        return chars
    
    def peek(self) -> str:
        return self.src[0]

    def isEmpty(self) -> bool:
        return self.length == 0
    
    def addToken(self, type:TokenType, value, start:int):
        self.tokens.append(Token(type, value, start))

    def compare_string(self, string:str) -> bool:
        if len(string) > self.length:
            return False
        
        for i in range(len(string)):
            if self.src[i] != string[i]:
                return False
            
        return True

    def match(self, *symbols:str) -> bool:
        "Returns true if the source contains one of the symbols, else false"
        return any(self.compare_string(symbol) for symbol in symbols)
    
    def matched_symbol(self, *symbols:str) -> str|None:
        "Returns the longest matched symbol. To avoid a None return, first check with match()"
        matches = [s for s in symbols if self.compare_string(s)]
        return max(matches, key=len) if matches else None

    @property
    def length(self) -> int:
        return len(self.src)
    
    @property
    def position(self) -> int:
        return self.initial_length - self.length
    

