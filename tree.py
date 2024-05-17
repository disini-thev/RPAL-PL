from stack import Stack
import sys

class Tree:
    # a stack containing nodes
    node_stack = Stack()

    def __init__(self, value, num_children):
        self.value = value
        self.num_children = num_children
        self.children = [None] * num_children
        # print("\nTREE BUILT\n", value, num_children)
        self.build_tree()

    def build_tree(self):
        for i in range (self.num_children-1, -1,-1): #i = 5 4 3 2 1 0 for 6 children
            if Tree.node_stack.is_empty():
                print("Can't ")
            self.children[i] = Tree.node_stack.pop()
        Tree.node_stack.push(self)

   
    def print_AST(root, level=0):
        # preorder_traversal_AST(root)
        if root is None:
            return

        print("." * level + root.value)

        for child in root.children:
            Tree.print_AST(child, level + 1)  # Recursively traverse each child node with increased level

    
    def ST_to_string(root, level=0):
        # preorder_traversal_AST(root)
        if root is None:
            return ""
        # print(root.value)

        result = "." * level + root.value + "\n"

        for child in root.children:
            result += Tree.ST_to_string(child, level + 1)
        return result

    
    # pre order traversalto print the ST
    """
    def print_ST(root):
        if root is None:
            return

        print(root.value, end="\t")

        for child in root.children:
            Tree.print_ST(child)  # Recursively traverse each child node
    """
    
    def level_order_traversal(root):
        if root is None:
            return

        queue = []
        queue.append((root, 0))  # Add root node with level 0

        while len(queue) > 0:
            node, level = queue.pop(0)
            print("."*level, end=" ")
            print (node.value)

            for child in node.children:
                if child is not None:
                    queue.append((child, level + 1))


    def standardize_tree(root):
        if root is None:
            return
        # print("Current root ", root.value)
        for i in range (root.num_children):
                root.children[i] = Tree.standardize_tree(root.children[i])
            # ensured the standardized structure of the children nodes

        if root.value == "let":
            # print("Standardizing let")
            root.value = "gamma"
            if root.children[0].value != "=":
                print("Error: Expected '=' in let")
                sys.exit()
            #else
            root.children[0].value = "lambda"
            root.children[0].children[1], root.children[1] = root.children[1], root.children[0].children[1] #exchange the children 
            return root
        
        if root.value == "where":
            # print("Standardizing where")
            root.value = "gamma"
            root.children[0], root.children[1] = root.children[1], root.children[0]
            # if root.children[0].value != "=":
            #     print("Error: Expected '=' in let")
            #     sys.exit()
            #else
            root.children[0].value = "lambda"
            root.children[0].children[1], root.children[1] = root.children[1], root.children[0].children[1] #exchange the children 
            return root

        if root.value == "fcn_form": # P V+ E 
            # print("Standardizing fcn_form")
            #restructuring : push all the children to the stack
            for child in root.children: 
                Tree.node_stack.push(child)
            num_lambda = root.num_children - 2 # number of newly introduced lamba nodes
            for i in range(num_lambda):
                Tree("lambda", 2)
            Tree("=",2) # check if the root is changed or just a temporary root created
            root = Tree.node_stack.pop()
            return root
        
        """
        # if root.value in ["tau", ",", "->","or","&","not","gr","ge","ls","le","eq","ne","+", "-", "neg", "*", "/","**","="]:
        #     # do not standardize these nodes, keep them as they are
        #     return

        # if root.value in ["true", "false", "nil", "dummy"]:
        #     # no children to standardize
        #     return
        
        # check what to do with id int str
        #################################################
        """
        
        if root.value == "lambda": # V++ E 
            # print("Standardizing lambda")
            #restructuring : push all the children to the stack
            for child in root.children: 
                Tree.node_stack.push(child)
            num_lambda = root.num_children - 2 # number of newly introduced lamba nodes
            for i in range(num_lambda):
                Tree("lambda", 2)
            Tree("lambda",2) # check if the root is changed or just a temporary root created
            root = Tree.node_stack.pop() 
            return root

        if root.value == "within":
            # print("Standardizing within")
            # after standardizing the child nodes
            """ within
                /     \
                =      =
              /  \    /  \  
             x1  E1  x2  E2 
            """
            Tree.node_stack.push(root.children[1].children[0]) # x2   #stack x2
            Tree.node_stack.push(root.children[0].children[0]) # x1   #stack x1 x2
            Tree.node_stack.push(root.children[1].children[1]) # E2   #stack E2 x1 x2
            Tree("lambda", 2)                                # stack lambda x2
            Tree.node_stack.push(root.children[0].children[1]) # E1   #stack E1 lambda x2
            Tree("gamma", 2)                                 # stack gamma x2
            Tree("=", 2)                              # stack =
            root = Tree.node_stack.pop()                            # empty stack
            return root

        if root.value == "@":
            # print("Standardizing @")
            # after standardizing the child nodes
            """    @
                /  |  \
               E1  N   E2
            """
            Tree.node_stack.push(root.children[1]) # N    #stack N
            Tree.node_stack.push(root.children[0]) # E1   #stack E1 N
            Tree("gamma", 2)                              # stack gamma 
            Tree.node_stack.push(root.children[2]) # E2   #stack E2 gamma
            Tree("gamma", 2)                       # stack gamma          
            root = Tree.node_stack.pop()                         # empty stack
            return root

        if root.value == "and":
            # print("Standardizing and")
            # after standardizing the child nodes
            """ and
                /   \
               =     =
              / \   / \
             x1 E1 x2 E2
            """
            root.children[0].children[1], root.children[1].children[0]= root.children[1].children[0], root.children[0].children[1] #exchange the children
            root.value = "="
            root.children[0].value = ","
            root.children[1].value = "tau"
            return root
        
        if root.value == "rec":
            # print("Standardizing rec")
            # after standardizing the child nodes
            """ rec
                |
                =
               / \
              x  E
            """
            Tree.node_stack.push(root.children[0].children[0])       # x    # stack x
            Tree("ystar", 0)                                         # stack ystar
            Tree.node_stack.push(root.children[0].children[0]) # x   # stack x Ystar x
            Tree.node_stack.push(root.children[0].children[1]) # E   # stack E x Ystar x
            Tree("lambda", 2)                                        # stack lambda Ystar x
            Tree("gamma", 2)                                         # stack gamma x
            Tree("=", 2)                                             # stack =
            root = Tree.node_stack.pop()                             # empty stack
            return root
        return root

    
        

    


    