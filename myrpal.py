import sys
import argparse
from tree import Tree
from parser_ import Parser
from lexical_analyser_ import LexicalAnalyser
from Cse_Machine import CSE_Machine

def main():
    parser = argparse.ArgumentParser(description='RPAL Interpreter')
    parser.add_argument('prog_file', type=str, help='the RPAL program file')
    parser.add_argument('-ast', action='store_true', help='print the abstract syntax tree and exit')
    
    args = parser.parse_args()
    prog_file = args.prog_file
    
    # Scanning and screening
    LE = LexicalAnalyser(prog_file)
    tokens = LE.lexical_analyser()
    
    # Parsing
    P = Parser(tokens)
    P.E()
    AST = Tree.node_stack.top()
    
    if args.ast:
        print("Abstract Syntax Tree")
        Tree.print_AST(AST)
        return

    # Standardizing the tree
    ST = Tree.standardize_tree(AST)
    
    # Running the CSE Machine
    machine = CSE_Machine()
    machine.run(ST)

if __name__ == "__main__":
    main()
