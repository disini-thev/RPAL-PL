import sys
from tree import Tree
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.next_token = self.tokens[0] # initializing the first token as 0th

    # def stripDel(self):

    #     while self.pos < (len(self.tokens) -1) and  ((self.tokens[self.pos])[1] == "DELETE" or (self.tokens[self.pos])[1] == "COMMENT"):
    #         self.pos+=1
    #         self.next_token = self.tokens[self.pos]

    def read(self, expected_token):
        # print("Reading ", expected_token)
        # self.stripDel()

        if self.next_token[0] != expected_token:
            print(f"Error: Expected {expected_token} but got {self.next_token[0]}")
            sys.exit()
        self.pos+=1
        if self.pos < len(self.tokens):
            self.next_token = self.tokens[self.pos]
        
        # print(self.next_token)

        # self.stripDel()

        # print("Next Token", self.next_token)
        
    def E(self):
        """E->'let' D 'in' E    => 'let'
            -> 'fn'  Vb+ '.' E  => 'lambda'
            ->  Ew;
        """
        # print("parsing in E", self.next_token)
        if self.next_token[0] == "let":
            self.read("let")
            self.D()
            self.read("in")
            self.E()
            Tree("let", 2)   #decide the number of children 3
        elif self.next_token[0] == "fn":
            self.read("fn")
            n = 0
            self.Vb()
            n += 1
            while self.next_token[1] == "IDENTIFIER" or self.next_token[1] == "(": # first set of Vb ->[ IDENTIFIER , '(' ]
                self.Vb()
                n += 1
            self.read(".")
            self.E()
            Tree("lambda", n+1 )  #decide the number of children 4
        else:
            self.Ew()
        # print("Returning from E")

    def Ew(self):
        """ Ew-> T 'where' Dr    => 'where'
                -> T;
        """
        # print("parsing in Ew", self.next_token)
        self.T()
        if self.next_token[0] == "where":
            self.read("where")
            self.Dr()
            Tree("where", 2)  #decide the number of children 5
        # print("Returning from Ew")
    
    def T(self):
        """ 
        T   -> Ta (','  Ta)+    => 'tau'
            -> Ta;
        -------------------------------
        T -> Ta (',' Ta)*
        """
        # print("parsing in T", self.next_token)
        self.Ta()
        if self.next_token[0] == ",":
            n=0
            while self.next_token[0] == ",":
                self.read(",")
                self.Ta()
                n+=1
            Tree("tau", n+1) #decide the number of children 6
        # print("Returning from T")

    def Ta(self):
        """ 
        Ta  -> Ta 'aug' Tc    => 'aug'
            -> Tc;
        -------------------------------
        Ta -> Tc ('aug' Tc)*
        
        """
        # print("parsing in Ta", self.next_token)
        self.Tc()
        while self.next_token[0] == "aug":
            self.read("aug")
            self.Tc()
            Tree("aug", 2)  #decide the number of children 7
        # print("Returning from Ta")

    def Tc(self):
        """
        Tc  -> B '->' Tc '|' Tc   => '->'
            -> B;
        --------------------------------
        Tc -> B (   |  '->' Tc '|' Tc)
        """
        # print("parsing in Tc", self.next_token)
        self.B()
        if self.next_token[0] == "->":
            self.read("->")
            self.Tc()
            self.read("|")
            self.Tc()
            Tree("->", 3)
        # print("Returning from Tc")

    def B(self):
        """
        B   -> B 'or' Bt    => 'or'
            -> Bt;
        --------------------------------
        B -> Bt ('or' Bt)*
        """
        # print("parsing in B", self.next_token)
        self.Bt()
        while self.next_token[0] == "or":
            self.read("or")
            self.Bt()
            Tree("or", 2)  #decide the number of children 9
        # print("Returning from B")

    def Bt(self):
        """
        Bt  -> Bt '&' Bs    => '&'
            -> Bs;
        --------------------------------
        Bt -> Bs ('&' Bs)*
        """
        # print("parsing in Bt", self.next_token)
        self.Bs()
        while self.next_token[0] == "&":
            self.read("&")
            self.Bs()
            Tree("&", 2)
        # print("Returning from Bt")

    def Bs(self):
        """
        Bs  -> 'not' Bp    => 'not'
            -> Bp;
        """
        # print("parsing in Bs", self.next_token)
        if self.next_token[0] == "not":
            self.read("not")
            self.Bp()
            Tree("not", 1)
        else:
            self.Bp()
        # print("Returning from Bs")

    def Bp(self):
        """
        Bp  -> A ('gr' | '>' ) A    => 'gr'
            -> A ('ge' | '>=' ) A   => 'ge'
            -> A ('ls' | '<' ) A    => 'ls'
            -> A ('le' | '<=' ) A   => 'le'
            -> A 'eq' A             => 'eq'
            -> A 'ne' A             => 'ne'
            -> A;
        """
        # print("parsing in Bp", self.next_token)
        self.A()
        if self.next_token[0] == "gr" or self.next_token[0] == ">":
            self.read(self.next_token[0])
            self.A()
            Tree("gr", 2)
        elif self.next_token[0] == "ge" or self.next_token[0] == ">=":
            self.read(self.next_token[0])
            self.A()
            Tree("ge", 2)
        elif self.next_token[0] == "ls" or self.next_token[0] == "<":
            self.read(self.next_token[0])
            self.A()
            Tree("ls", 2)
        elif self.next_token[0] == "le" or self.next_token[0] == "<=":
            self.read(self.next_token[0])
            self.A()
            Tree("le", 2)
        elif self.next_token[0] == "eq":
            self.read("eq")
            self.A()
            Tree("eq", 2)
        elif self.next_token[0] == "ne":
            self.read("ne")
            self.A()
            Tree("ne", 2)
        # other values should not be passed from this
        # print("Returning from Bp")

    def A(self):
        """
        A   -> A '+' At    => '+'
            -> A '-' At    => '-'
            ->   '+' At
            ->   '-' At    => 'neg'
            -> At;
        --------------------------------
        A -> ( '+' At | '-' At | At ) ( '+' At | '-' At)*
        """
        # print("parsing in A", self.next_token)
        if self.next_token[0]=="+":
            self.read("+")
            self.At()
        elif self.next_token[0]=="-":
            self.read("-")
            self.At()
            Tree("neg", 1)
        else:
            self.At()
        while self.next_token[0] == "+" or self.next_token[0] == "-":
            if self.next_token[0]=="+":
                self.read("+")
                self.At()
                Tree("+", 2)
            elif self.next_token[0]=="-":
                self.read("-")
                self.At()
                Tree("-", 2)
        # print("Returning from A")

    def At(self):
        """
        At  -> At '*' Af    => '*'
            -> At '/' Af    => '/'
            -> Af;
        --------------------------------
        At -> Af (* Af | / Af)*
        """
        # print("parsing in At", self.next_token)
        self.Af()
        while self.next_token[0] == "*" or self.next_token[0] == "/":
            if self.next_token[0]=="*":
                self.read("*")
                self.Af()
                Tree("*", 2)
            elif self.next_token[0]=="/":
                self.read("/")
                self.Af()
                Tree("/", 2)
        # print("Returning from At")

    def Af(self):
        """
        Af  -> Ap '**' Af    => '**'
            -> Ap;
        ------------------------
        Af -> Ap (    | ** Af)
        """
        # print("parsing in Af", self.next_token)
        self.Ap()
        if self.next_token[0] == "**":
            self.read("**")
            self.Af()
            Tree("**", 2)
        # print("Returning from Af")
        
    def Ap(self):
        """
        Ap  -> Ap '@' <identifier> R    => '@'
            -> R;
        ---------------------------------
        Ap -> R ( @ identifier R)*
            
        """
        # print("parsing in Ap", self.next_token)
        self.R()
        while self.next_token[0] == "@":
            self.read("@")
            # check if the next token is an identifier
            if self.next_token[1] == "IDENTIFIER":
                Tree(self.next_token[0], 0)
                self.read(self.next_token[0])
                self.R()
                Tree("@", 3) #fixed the number of children, check again
            else:
                print(f"Error: Expected an identifier but got {self.next_token[0]}")
                sys.exit()
            
        # print("Returning from Ap")        

    def R(self):
        """
        R   -> R Rn    => 'gamma'
            -> Rn;
        -------------
        R -> Rn+
        """
        # print("parsing in R", self.next_token)
        self.Rn()
        while self.next_token[1] in ["IDENTIFIER", "INTEGER", "STRING"] or self.next_token[0] in ["true", "false","nil", "(", "dummy"]: # check if the next token is in the first set of Rn
            self.Rn()
            Tree("gamma", 2)
        # print("Returning from R")

    def Rn(self):
        """
        Rn  -> <Identifier>
            -> <Integer>
            -> <String>
            -> 'true'       => 'true'
            -> 'false'      => 'false'
            -> 'nil'        => 'nil'
            -> '(' E ')'
            -> 'dummy'      => 'dummy';
        """
        # print("parsing in Rn", self.next_token)
        if self.next_token[0] == "true":
            self.read("true")
            Tree("true", 0)
        elif self.next_token[0] == "false":
            self.read("false")
            Tree("false", 0)
        elif self.next_token[0] == "nil":
            self.read("nil")
            Tree("nil", 0)
        elif self.next_token[0] == "dummy":
            self.read("dummy")
            Tree("dummy", 0)
        elif self.next_token[0] == "(":
            self.read("(")
            self.E()
            self.read(")")
        # for other Identifier tokens
        elif self.next_token[1] == "IDENTIFIER":
            val = self.next_token[0]
            self.read(self.next_token[0])
            Tree("id :"+ val, 0)
        elif self.next_token[1] == "INTEGER":
            val = self.next_token[0]
            self.read(self.next_token[0])
            Tree("int :"+ val, 0)
        elif self.next_token[1] == "STRING":
            val = self.next_token[0]
            self.read(self.next_token[0])
            Tree("str :"+ val, 0)
        else:
            print(f"Error: Expected an identifier, integer, string, 'true', 'false', 'nil', '(', or 'dummy' but got {self.next_token[0]}")
            sys.exit()
        # print("Returning from Rn")

    def D(self):
        """
        D   -> Da 'within' D    => 'within'
            -> Da;
        """
        # print("parsing in D", self.next_token)
        self.Da()
        if self.next_token[0] == "within":
            self.read("within")
            self.D()
            Tree("within", 2)
        # print("Returning from D")

    def Da(self):
        """
        Da  -> Dr ('and' Da)+    => 'and'
            -> Dr;
        """
        # print("parsing in Da", self.next_token)
        self.Dr()
        n=0
        while self.next_token[0] == "and":
            self.read("and")
            self.Dr()
            n+=1
        if n>0:  # check if there are more than one 'and' in the input
            Tree("and", n+1)
        # print("Returning from Da")

    def Dr(self):
        """
        Dr  -> 'rec' Db    => 'rec'
            -> Db;
        """
        # print("parsing in Dr", self.next_token)
        if self.next_token[0] == "rec":
            self.read("rec")
            self.Db()
            Tree("rec", 1)
        else:
            self.Db()
        # print("Returning from Dr")

    def Db(self):
        """
        Db  -> Vl '=' E    => '='  first set of vl is <identifier>
            -> <identifier> Vb+ '=' E    => 'fcn_form';
            -> '(' D ')';
        """
        # print("parsing in Db", self.next_token)
        if self.next_token[0] == "(":
            self.read("(")
            self.D()
            self.read(")")


        elif self.next_token[1] == "IDENTIFIER":
            val = self.next_token[0]
            self.read(self.next_token[0])
            Tree(val,0)
            # print(self.next_token)

            if self.next_token[0]=="," or self.next_token[0] == "=":  #checking if this should go through vl
                self.Vl()
                self.read("=")
                self.E()
                Tree("=", 2)
            
            else: # going through Vb path
                n=0
                self.Vb()
                n+=1
                # print("Next ",self.next_token)
                while self.next_token[1] == "IDENTIFIER" or self.next_token[1] == "(":  # check if the next token is in the first set of Vb
                    #fixed the extra reading of the token
                    self.Vb()
                    n+=1
                self.read("=")
                self.E()
                Tree("fcn_form", n+2)
        # else:
        #     self.Vl()
            
        # print("Returning from Db")

    def Vb(self): 
        """
        Vb -> <identifier>
            -> '(' Vl ')'
            -> '(' ')'  => '()';
        """
        # print("parsing in Vb", self.next_token)
        if self.next_token[1] == "IDENTIFIER":
            val = self.next_token[0]
            # print(self.next_token)
            self.read(self.next_token[0])
            Tree(val, 0)
            # print("setjfs")
        elif self.next_token[0] == "(":
            self.read("(")
            if self.next_token[0] == ")":
                self.read(")")
                Tree("()", 0)
            elif self.next_token[1] == "IDENTIFIER": #first set of Vl
                val = self.next_token[0]
                self.read(self.next_token[0])
                Tree(val,0)
                self.Vl()
                self.read(")")
        else:
            print(f"Error: Expected an identifier or  '(' but got {self.next_token[0]}")
            sys.exit()
        # print("Returning from Vb")

    def Vl(self):
        """
        Vl  -> <identifier> (',' <identifier>)*    => ','?
        """ 
        # print("parsing in Vl", self.next_token)
        n=0
        while self.next_token[0] == ",":
            self.read(",")
            if self.next_token[1] == "IDENTIFIER":
                val = self.next_token[0]
                self.read(self.next_token[0])
                Tree(val,0)
                n+=1
            else:
                print("Error from Vl")
        if n>0:
            Tree(",", n+1) 
        # print("Returning from Vl")
