class EnvironmentNode(object):
    def __init__(self, number, parent):
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent = parent

    def addChild(self, node):
        self.children.append(node)
        node.variables.update(self.variables)

    def addVariable(self, key, value):
        self.variables[key] = value

class CSE_Machine:
    builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]

    def __init__(self):
        self.controlStructures = []
        self.count = 0
        self.control = []
        self.stack = []
        self.environments = [EnvironmentNode(0, None)]
        self.currentEnvironment = 0
    
    def run(self, ST):
        self.generateControlStructure(ST, 0)
        self.control.append(self.environments[0].name)
        self.control += self.controlStructures[0]
        self.stack.append(self.environments[0].name)
        self.applyRules()

        print("Output of the program is : ", self.stack[0])

    def generateControlStructure(self, root, i):
        while len(self.controlStructures) <= i:
            self.controlStructures.append([])

        if root.value == "lambda":
            self.count += 1
            leftChild = root.children[0]
            if leftChild.value == ",":
                temp = "lambda" + "_" + str(self.count) + "_"
                for child in leftChild.children:
                    temp += child.value[4:-1] + ","
                temp = temp[:-1]
                self.controlStructures[i].append(temp)
            else:
                temp = "lambda" + "_" + str(self.count) + "_" + leftChild.value[4:-1]
                self.controlStructures[i].append(temp)

            for child in root.children[1:]:
                self.generateControlStructure(child, self.count)

        elif root.value == "->":
            self.count += 1
            temp = "delta" + "_" + str(self.count)
            self.controlStructures[i].append(temp)
            self.generateControlStructure(root.children[1], self.count)
            self.count += 1
            temp = "delta" + "_" + str(self.count)
            self.controlStructures[i].append(temp)
            self.generateControlStructure(root.children[2], self.count)
            self.controlStructures[i].append("beta")
            self.generateControlStructure(root.children[0], i)

        elif root.value == "tau":
            n = len(root.children)
            temp = "tau" + "_" + str(n)
            self.controlStructures[i].append(temp)
            for child in root.children:
                self.generateControlStructure(child, i)

        else:
            self.controlStructures[i].append(root.value)
            for child in root.children:
                self.generateControlStructure(child, i)

    def lookup(self, name):
        if name.startswith("int", 1):
            return int(name[5:-1])
        elif name.startswith("str", 1):
            return name[5:-1].strip("'")
        elif name.startswith("id", 1):
            variable = name[4:-1]
            if variable in CSE_Machine.builtInFunctions:
                return variable
            else:
                value = self.environments[self.currentEnvironment].variables[variable]
                return value
        elif name.startswith("ystar", 1):
            return "ystar"
        elif name.startswith("nil", 1):
            return ()
        elif name.startswith("true", 1):
            return True
        elif name.startswith("false", 1):
            return False

    def applyRules(self):
        binop = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
        unop = ["neg", "not"]

        while len(self.control) > 0:
            symbol = self.control.pop()

            # Rule 1
            if symbol.startswith("<") and symbol.endswith(">"):
                self.stack.append(self.lookup(symbol))

            # Rule 2
            elif symbol.startswith("lambda"):
                self.stack.append(symbol + "_" + str(self.currentEnvironment))

            # Rule 4
            elif symbol == "gamma":
                stackSymbol_1 = self.stack.pop()
                stackSymbol_2 = self.stack.pop()

                if type(stackSymbol_1) == str and stackSymbol_1.startswith("lambda"):
                    self.currentEnvironment = len(self.environments)
                    lambdaData = stackSymbol_1.split("_")

                    parent = self.environments[int(lambdaData[3])]
                    child = EnvironmentNode(self.currentEnvironment, parent)
                    parent.addChild(child)
                    self.environments.append(child)

                    # Rule 11
                    variablesList = lambdaData[2].split(",")
                    if len(variablesList) > 1:
                        for i in range(len(variablesList)):
                            child.addVariable(variablesList[i], stackSymbol_2[i])
                    else:
                        child.addVariable(lambdaData[2], stackSymbol_2)

                    self.stack.append(child.name)
                    self.control.append(child.name)
                    self.control += self.controlStructures[int(lambdaData[1])]

                elif type(stackSymbol_1) == tuple:
                    self.stack.append(stackSymbol_1[stackSymbol_2 - 1])

                elif stackSymbol_1 == "ystar":
                    temp = "eta" + stackSymbol_2[6:]
                    self.stack.append(temp)
                #Rule 13
                elif type(stackSymbol_1) == str and stackSymbol_1.startswith("eta"):
                    temp = "lambda" + stackSymbol_1[3:]
                    self.control.append("gamma")
                    self.control.append("gamma")
                    self.stack.append(stackSymbol_2)
                    self.stack.append(stackSymbol_1)
                    self.stack.append(temp)

                elif stackSymbol_1 == "Order":
                    order = len(stackSymbol_2)
                    self.stack.append(order)

                elif stackSymbol_1 in ["Print", "print"]:
                    self.stack.append(stackSymbol_2)

                elif stackSymbol_1 == "Conc":
                    stackSymbol_3 = self.stack.pop()
                    self.control.pop()
                    temp = stackSymbol_2 + stackSymbol_3
                    self.stack.append(temp)

                elif stackSymbol_1 == "Stern":
                    self.stack.append(stackSymbol_2[1:])

                elif stackSymbol_1 == "Stem":
                    self.stack.append(stackSymbol_2[0])

                elif stackSymbol_1 == "Isinteger":
                    if type(stackSymbol_2) == int:
                        self.stack.append(True)
                    else:
                        self.stack.append(False)
                    # self.stack.append(isinstance(arg, int))

                elif stackSymbol_1 == "Istruthvalue":
                    if type(stackSymbol_2) == bool:
                        self.stack.append(True)
                    else:
                        self.stack.append(False)

                elif stackSymbol_1 == "Isstring":
                    if type(stackSymbol_2) == str:
                        self.stack.append(True)
                    else:
                        self.stack.append(False)

                elif stackSymbol_1 == "Istuple":
                    if type(stackSymbol_2) == tuple:
                        self.stack.append(True)
                    else:
                        self.stack.append(False)

                elif stackSymbol_1 == "Isfunction":
                    if stackSymbol_2 in CSE_Machine.builtInFunctions:
                        return True
                    else:
                        return False
            #Rule 5                        
            elif symbol.startswith("e_"):
                stackSymbol = self.stack.pop()
                self.stack.pop()
                if self.currentEnvironment != 0:
                    for element in reversed(self.stack):
                        if type(element) == str and element.startswith("e_"):
                            self.currentEnvironment = int(element[2:])
                            break
                self.stack.append(stackSymbol)

            #Rule 6
            elif(symbol in binop):
                rand_1 = self.stack.pop()
                rand_2 = self.stack.pop()
                if(symbol == "+"):
                    self.stack.append(rand_1+rand_2)
                elif(symbol == "-"):
                    self.stack.append(rand_1-rand_2)
                elif(symbol == "*"):
                    self.stack.append(rand_1*rand_2)
                elif(symbol == "/"):
                    self.stack.append(rand_1/rand_2)
                elif(symbol == "**"):
                    self.stack.append(rand_1**rand_2)
                elif(symbol == "gr"):
                    self.stack.append(rand_1 > rand_2)
                elif(symbol == "ge"):
                    self.stack.append(rand_1 >= rand_2)
                elif(symbol == "ls"):
                    self.stack.append(rand_1 < rand_2)
                elif(symbol == "le"):
                    self.stack.append(rand_1 <= rand_2)
                elif(symbol == "eq"):
                    self.stack.append(rand_1 == rand_2)
                elif(symbol == "ne"):
                    self.stack.append(rand_1 != rand_2)
                elif(symbol == "or"):
                    self.stack.append(rand_1 or rand_2)
                elif(symbol == "&"):
                    self.stack.append(rand_1 and rand_2)
                elif(symbol == "aug"):
                    if(type(rand_2) == tuple):
                        self.stack.append(rand_1 + rand_2)
                    else:
                        self.stack.append(rand_1+(rand_2,))

            #Rule 7
            elif(symbol in unop):
                rand = self.stack.pop()
                if(symbol == "not"):
                    self.stack.append(not rand)
                elif(symbol == "neg"):
                    self.stack.append(-rand)

            #Rule 8
            elif symbol == "beta":
                B = self.stack.pop()
                deltaElse = self.control.pop()
                deltaThen = self.control.pop()
                if B:
                    self.control += self.controlStructures[int(deltaThen.split('_')[1])]
                else:
                    self.control += self.controlStructures[int(deltaElse.split('_')[1])]

            #Rule 9
            elif symbol.startswith("tau_"):
                n = int(symbol.split("_")[1])
                tauList = [self.stack.pop() for _ in range(n)]
                self.stack.append(tuple(tauList))

            elif symbol == "ystar":
                self.stack.append(symbol)