import sys
# from stack import Stack
from tree import Tree
from parser_ import Parser
from lexical_analyser_ import LexicalAnalyser
from Cse_Machine import CSE_Machine

def main():
    prog_file = sys.argv[1]
    
    # print("SCANNING AND SCREENING")
    LE = LexicalAnalyser(prog_file)
    tokens = LE.lexical_analyser()
    # for token in tokens:
    #     print(token[0], token[1])
    
    # print("PARSING")
    P = Parser(tokens)
    # P.stripDel()
    P.E()
    AST = Tree.node_stack.top()
    Tree.print_AST(AST)

    with open("..\\Rpal-Interpreter\\AST_output.txt", "w") as file:
        file.write(Tree.ST_to_string(AST))

    # standardizing the tree
    ST = Tree.standardize_tree(AST)
    Tree.print_AST(ST)



    print("\n\n\n CSE Machine\n\n\n")

    machine = CSE_Machine()
    machine.run(ST)
    

if __name__ == "__main__":
    main()


# prog_file = sys.argv[1]
    
# # print("SCANNING AND SCREENING")
# LE = LexicalAnalyser(prog_file)
# tokens = LE.lexical_analyser()
# # for token in tokens:
# #     print(token[0], token[1])

# # print("PARSING")
# P = Parser(tokens)
# # P.stripDel()
# P.E()
# AST = Tree.node_stack.top()
# Tree.print_AST(AST)
# # write the output of print_AST to a file
# with open("..\\Rpal-Interpreter\\AST_output.txt", "w") as file:
#     file.write(Tree.ST_to_string(AST))
    

# # standardizing the tree
# ST = Tree.standardize_tree(AST)

# print("\n\n\nStandardized Tree\n\n\n")
# Tree.print_AST(ST)



# print("\n\n\nStarting the CSE Machine\n\n\n")


# controlStructures = []   
# count = 0

# generateControlStructure(ST,0) ############################

# builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]

# control = []
# stack = []
# environments = [EnvironmentNode(0, None)]
# currentEnvironment = 0

# control.append(environments[0].name)
# control += controlStructures[0]

# stack.append(environments[0].name)

# applyRules()

# print("Output of the above program is:")
# print(stack[0])