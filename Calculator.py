#Calculator for the user
from MathParser import Parse, TokenType, NumberNode, OperatorNode

# Node Operations -------------------------------
# this is brainrot -v
def Add(a,b): return a+b
def Sub(a,b): return a-b
def Mul(a,b): return a*b
def Div(a,b): return a/b
def Pow(a,b): return pow(a,b)
#Used for the compute function, matched to the functions above
operations = {
    TokenType.Add: Add,
    TokenType.Sub: Sub,
    TokenType.Mul: Mul,
    TokenType.Div: Div,
    TokenType.Pow: Pow
}
#mathifier, this little fella takes the ast and does the maths
def Compute(node:NumberNode|OperatorNode) -> float|int:
    """Returns the calculation result of the parsed `ast` -> `(Compute(Parse(string)))`"""
    #Calculate Number Nodes
    if node.token_type == TokenType.Num:
        return node.value
    #Calculate Operator Nodes
    left_result = Compute(node.left)
    right_result = Compute(node.right)
    math_function = operations[node.token_type]
    return math_function(left_result, right_result)

# User Experience -------------------------------
def main():
    running = True
    print("       Python Math Parser\nWrite \"stop\" to end the program\n")
    while running:
        string = input("expression:\n> ").lower()
        if string == "stop":
            running = False
        else:
            ast = Parse(string)
            result = Compute(ast)
            #print(ast)
            print("= "+str(result))

    #end of program
    print("night night")
    exit()

if __name__ == "__main__":
    main()