import sys
from stack import Stack
from tree import Tree
from parser_ import Parser
from lexical_analyser_ import LexicalAnalyser

def main():
    prog_file = sys.argv[1]
    # for prog_file in prog_file_Li:
    #     print("\n")
    
    # print("SCANNING AND SCREENING")
    LE = LexicalAnalyser(prog_file)
    tokens = LE.lexical_analyser()
    # for token in tokens:
    #     print(token[0], token[1])
    
    print("PARSING")
    P = Parser(tokens)
    # P.stripDel()
    P.E()
    Tree.print_AST()
    
    # standardizing the tree
    Tree.standardize_tree()


if __name__ == "__main__":
    main()