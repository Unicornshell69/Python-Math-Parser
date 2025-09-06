from lexer.lexer import tokenize
from parser.parser import Parser
from parser.nodes import ASTNode
from runtime.interpreter import evaluate
import json
from os import path
import sys
sys.set_int_max_str_digits(1000000000)


def store_ast(ast:ASTNode, dir:str =".\\ast.json"):
    with open(dir, "w") as file:
        json.dump(ast.to_dict(), file, indent=2)
    print(f"AST saved to \033[36m{path.abspath(dir).replace("\\","/")}\033[0m")



if __name__ == "__main__":
    parser = Parser()
    parser.type = float
    while 1:
        source = input(">")
        ast = parser.parse(source)
        result = evaluate(ast)
        #print(len(str(result)))
        print(f"={result}")
        store_ast(ast)
    #print(f"original: {source}")
    
