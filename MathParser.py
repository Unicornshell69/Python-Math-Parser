#Math parser by unicornshell
#thanks to darvass69 for the help :D
#October 2024 -> the mental illness has begun
#January 2025 -> fixing stuff up
from __future__ import annotations
import math

# Error calls
class EndTokenError(Exception):
    pass
class DoubleDecimalError(Exception):
    pass
class NotATokenError(Exception):
    pass
class TokenInWrongPlaceError(Exception):
    pass
class BannedTokenTypeFound(Exception):
    pass
class MissingParenthesisError(Exception):
    pass
err_style = "\""
Fix_Missing_Parentheses = True

# We have Enums at home --------------------------
class TokenType():
    Num = 0   #Number
    Add = 1   #Addition
    Sub = 2   #Subtraction
    Mul = 3   #Multiplication
    Div = 4   #Division
    Pow = 5   #Exponent
    Sqrt= 6   #Square root
    LPa = 7   #Left Parenthesis
    RPa = 8   #Right Parenthesis
    End = 9   #End of Calculations
    Func= 10  #TODO: Function
    Sep = 11  #Seperator
    Ban = 12  #Banned characters, get output but create an error
#Associated names for printing errors
TokenTypeNames = {0:"Number",1:"Add",2:"Subtract",3:"Multiply",4:"Divide",5:"Exponent",6:"Square root",7:"Left parenthesis",8:"Right parenthesis",9:"End",10:"Function",11:"Seperator",12:"Banned"}
class OperatorPriority():
    Default = 0
    Additive = 1
    Multiplicative = 2
    Prefix = 3
    Exponential = 4
    Function = 5
    Number = 6
# TODO #
# class FunctionType():
#     Root = 0
#     Log = 1
#     Ln = 2
#     Abs = 3
#     Round = 4

# Useful functions -------------------------------
def MatchSymbol(string,start,match:dict):
    """Searches the dictionary for a matching symbol. Works with any string length"""
    for symbol in match.keys():
        #single characters should have already been matched
        if len(symbol) != 1:
            char = string[start:start+len(symbol)]
            if char == symbol:
                return symbol
    if string[start] in match:
        return string[start]
    

# Dictionary maps --------------------------------
#Used for operation priority, really fucking important
OperatorPriorityMap = {
    TokenType.Add : OperatorPriority.Additive,
    TokenType.Sub : OperatorPriority.Additive,
    TokenType.Mul : OperatorPriority.Multiplicative,
    TokenType.Div : OperatorPriority.Multiplicative,
    TokenType.Pow : OperatorPriority.Exponential
    }
#Map of what operation is linked to characters
OperatorSymbolMap = {
    "+"   : TokenType.Add,
    "-"   : TokenType.Sub,
    "*"   : TokenType.Mul,
    "x"   : TokenType.Mul,
    "×"   : TokenType.Mul,
    "/"   : TokenType.Div,
    "÷"   : TokenType.Div,
    "^"   : TokenType.Pow,
    "**"  : TokenType.Pow,
    "("   : TokenType.LPa,
    ")"   : TokenType.RPa,
    "sqrt":TokenType.Sqrt,
    "√"   :TokenType.Sqrt,
    ","   : TokenType.Sep
    }
#You can use teeny tiny numbers as exponents
ExponentSymbolMap = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9"}
#Matches fraction characters to their float value
FractionSymbolMap = {"¼":0.25,"⅓":1/3,"⅖":0.4,"⅙":1/6,"½":0.5,"⅔":2/3,"⅗":3/5,"⅚":5/6,"¾":0.75,"⅕":0.2,"⅘":0.8,"⅐":1/7,"⅛":0.125,"⅞":7/8,"⅜":0.375,"⅑":1/9,"⅝":5/8,"⅒":0.1}
ConstantSymbolMap = {"pi":math.pi,"e":math.e}
# TODO #
#FunctionPriorityMap = {
#    FunctionType.root : OperatorPriority.Function,
#    FunctionType.log : OperatorPriority.Function
#    }
#Input characters that are ignored
IgnoreCharacters = (" ","\n","\r","\t")
DecimalSeperators = (".")       #I think this should work as a tuple, I haven't tested it though


# Custom Token class -----------------------------
# Token has a type (number, multiplication, etc) and a value (float/int if type=number, not important for any other type)
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    def  __repr__(self) -> str:
        return f"({self.token_type}, value={self.value})"

# Operator nodes are tokens with a left and right child node (these are also nodes, either NumberNodes or other Operators with children)
class OperatorNode(Token):
    def __init__(self, token_type, value,left:Token,right:Token):
        super().__init__(token_type, value)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Left: {self.left}\nOperator: {self.value}\nRight: {self.right}"
    
#NumberNodes are tokens with a fixed token_type, they exist for readability only
class NumberNode(Token):
    def __init__(self, value):
        super().__init__(TokenType.Num, value)
# TODO #
# class FunctionNode(Token):
    # def __init__(self, value,arguments:list):
        # super().__init__(TokenType.Func,value)
        # self.arguments = arguments
    # def __repr__(self):
        # return f"Function: {self.value}\nArguments: {self.arguments}"


# Parsing functions ------------------------------
# Split text into blocks (aka tokens), such as numbers, exponents, divisions, etc
def Tokenify(text:str):
    tokens = []
    #fix tabs & newlines
    #remove ignored characters
    ndx = 0
    while ndx < len(text):
        should_append = True
        char = text[ndx]
        ndx += 1

        #start by checking for ignore characters
        #if not, detect if we have a number
        #if not, try to match to an operator
        #if not an operator, die

        #ignore spaces and newlines and shit
        if char in IgnoreCharacters:
            should_append = False

        #create number tokens (combines all adjacent numbers into a float), allows starting a decimal number with .xx instead of 0.xx
        elif char.isdecimal() or char in DecimalSeperators:
            if char in DecimalSeperators:
                alreadyADot = True
                value = "0" + char
            else:
                alreadyADot = False
                value = char
                
            #keep scanning forward as long as we find numbers or a "." if there hasnt been one yet
            while ndx < len(text) and (text[ndx].isdecimal() or text[ndx] in DecimalSeperators): 
                if text[ndx] in DecimalSeperators:
                    if alreadyADot:
                        raise DoubleDecimalError(f"Error: Multiple decimal points were found in this number: {err_style}{value}{err_style}")#(f"Error creating float: Cannot have 2 decimal seperators in one number, you dumbass")
                    else:
                        alreadyADot = True
                        value += "."
                else:
                    value += text[ndx]
                ndx += 1
            token = NumberNode(value=float(value))

        #create operator tokens (as a Token, not an OperatorNode, because they don't have left and right elements yet)
        else:
            symbol = MatchSymbol(text,ndx-1,OperatorSymbolMap)
            #symbol is NoneType if MatchSymbol failed to find a match
            if symbol != None:
                token_type = OperatorSymbolMap[symbol]
                #raise an error for banned characters
                if token_type == TokenType.Ban:
                    raise BannedTokenTypeFound(f"Error: {err_style}{symbol}{err_style} is a banned character")
                else:
                    token = Token(token_type, value=symbol)
                    ndx += (len(symbol)-1)
            
            #small exponent numbers
            elif char in ExponentSymbolMap:
                value = ExponentSymbolMap[char]
                #start by creating a exponent token
                tokens.append(Token(TokenType.Pow,value=char))
                while ndx < len(text) and (text[ndx] in ExponentSymbolMap):
                    value += ExponentSymbolMap[text[ndx]]
                    ndx += 1
                #add the value represented by the small characters as a number token after the exponent
                token = NumberNode(value=int(value))
            
            #fractions become numbers
            elif char in FractionSymbolMap:
                token = NumberNode(value=FractionSymbolMap[char])
            
            else:
                symbol = MatchSymbol(text,ndx-1,ConstantSymbolMap)
                if symbol != None:
                    token = NumberNode(value=ConstantSymbolMap[symbol])
                    ndx += (len(symbol)-1)
            #tokenify couldnt find a matching operator token :(
                else: raise NotATokenError(f"Error: {err_style}{char}{err_style} is not a valid character")#(f"This bitch aint a token chief => {char} D:")

        if should_append:tokens.append(token)

    tokens.append(Token(TokenType.End,value="End"))
    return tokens

# Create big boy Node with a left and right node, which are also gonna be huge
def ParseBinOperator(tokens: list[Token], operator_priority: int):
    left_node = ParseUniOperator(tokens,operator_priority)

    while len(tokens) > 0:
        try: token_priority = OperatorPriorityMap[tokens[0].token_type]
        except: break

        if not (token_priority > operator_priority):
            break
        token = tokens.pop(0)
        left_node = OperatorNode(
            token.token_type,
            token.value,
            left_node,
            ParseBinOperator(tokens,token_priority)
        )
    return left_node

# Parse numbers, parentheses, negate signs, etc
def ParseUniOperator(tokens: list[Token], operator_priority):
    #Minus sign becomes -1*[Next Node] if it is here, because it doesnt have a parent operator
    if (OperatorPriority.Prefix > operator_priority):
        #negate sign
        if tokens[0].token_type == TokenType.Sub:
            tokens.pop(0)
            node = OperatorNode(
                TokenType.Mul,
                "negate",
                NumberNode(-1),
                ParseBinOperator(tokens,OperatorPriority.Prefix)
            )
            return node
        #double plus signs
        elif tokens[0].token_type == TokenType.Add:
            tokens.pop(0)
            node = ParseBinOperator(tokens,OperatorPriority.Prefix)
            return node
    
    #Handle square root as num ^ 0.5
    if (OperatorPriority.Function > operator_priority):
        if tokens[0].token_type == TokenType.Sqrt:
            tokens.pop(0)
            node = OperatorNode(
                TokenType.Pow,
                "sqrt",
                ParseBinOperator(tokens,OperatorPriority.Function),
                NumberNode(0.5)
                )
            return node

    #Restart ParseBinOperator if we enter parentheses
    if tokens[0].token_type == TokenType.LPa:
        tokens.pop(0)
        expression = ParseBinOperator(tokens,OperatorPriority.Default)

        if tokens[0].token_type == TokenType.RPa:
            tokens.pop(0)
            if tokens[0].token_type == TokenType.LPa:
                node = OperatorNode(
                    TokenType.Mul,
                    "Implicit Mul",
                    expression,
                    ParseBinOperator(tokens,OperatorPriority.Multiplicative)
                )
                return node
            #code will disregard missing parentheses 
            if not Fix_Missing_Parentheses : 
                return expression
            
        elif not Fix_Missing_Parentheses: 
            raise MissingParenthesisError(f"Error: Missing closed parenthesis before {err_style}{tokens[0].value}{err_style} [{TokenTypeNames[tokens[0].token_type]}]")
        
        return expression

    #Parse numbers
    if tokens[0].token_type == TokenType.Num:
        token = tokens.pop(0)

        #Add an implicit multiplication
        if tokens[0].token_type == TokenType.LPa:
            node = OperatorNode(
                TokenType.Mul,
                "Implicit Mul",
                token,
                ParseBinOperator(tokens,OperatorPriority.Multiplicative)
            )
            return node
        
        return token
    
    
    #If something went wrong
    raise TokenInWrongPlaceError(f"Error: Position of {err_style}{tokens[0].value}{err_style} [{TokenTypeNames[tokens[0].token_type]}] is invalid")#(f"This token aint supposed to be here chief => {tokens[0]} D:")
    #this is a fairly bad way of doing things, the parser is sorta dumb, it knows there is an error, but doesn't really know why
    #However, I am lazy.

# TODO #
# def ParseFunctionCall(tokens,operator_priority):
#     try: token_priority = FunctionPriorityMap[tokens[0].value]
#     except: raise Exception(f"not a function")
#     token = tokens.pop(0)
#     if tokens[0].token_type == TokenType.LPa:
#         token = tokens.pop(0)
#         argument = FunctionNode(
#             )
#     while len(tokens) > 0:
#         try: token_priority = FunctionPriorityMap[tokens[0].value]
#         except: break
#         if not (token_priority > operator_priority):
#             break
#         token = tokens.pop(0)


# Main function --------------------------------
def Parse(string):
    """Returns a parsed `ast` to be passed to the `Compute` function"""
    tokens = Tokenify(string)
    ast = ParseBinOperator(tokens,OperatorPriority.Default)
    if tokens[0].token_type == TokenType.End:
        tokens.pop(0)
    else:
        #Shit an error if no End Token is present
        raise EndTokenError(f"Error: {err_style}{tokens[0].value}{err_style} [{TokenTypeNames[tokens[0].token_type]}] should be {err_style}{TokenTypeNames[TokenType.End]}{err_style} instead")#(f"This token is supposed to be {TokenType.End}. It is {tokens[0].token_type} instead D:")
    return ast