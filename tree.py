class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise Exception("Stack is empty")

    def is_empty(self):
        return len(self.stack) == 0

class Tree:
    # a stack containing nodes
    node_stack = Stack()

    def __init__(self, value, num_children):
        self.value = value
        self.num_children = num_children
        self.children = [None] * num_children
        self.build_tree(Tree.node_stack)

    def build_tree(self, node_stack):
        for i in range (self.num_children-1, -1,-1): #i = 5 4 3 2 1 0 for 6 children
            self.children[i] = node_stack.pop()
        node_stack.push(self)

def level_order_traversal(root):
    if root is None:
        return

    queue = []
    queue.append((root, 0))  # Add root node with level 0

    while len(queue) > 0:
        node, level = queue.pop(0)
        print("."*level, end="")
        print (node.value)
        # print(f"Level: {level}, Value: {node.value}")

        for child in node.children:
            if child is not None:
                queue.append((child, level + 1))

def preorder_traversal(root, level=0):
    if root is None:
        return

    print("." * level, root.value)

    for child in root.children:
        preorder_traversal(child, level + 1)  # Recursively traverse each child node with increased level


# Sample code to test the Tree class

# Create a tree with value 1 and 3 children
t1=Tree("f",0)
t2=Tree("x",0)
t3=Tree(3,0)
t4=Tree("func_form",3)
t5=Tree("p",0)
t6=Tree("f",0)
t7=Tree("3",0)
t8=Tree("gamma",2)
t9=Tree("gamma",2)
t10=Tree("let",2)



preorder_traversal(t10)
