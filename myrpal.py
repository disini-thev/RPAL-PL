import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def match(self, expected_token):
        # check this functionif it's necessary
        if self.current_token[1] == expected_token:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            return True
        return False
    
    def E(self):
        pass

    def Ew(self):
        pass

    def T(self):
        pass

    def Ta(self):
        pass

    def Tc(self):
        pass

    def B(self):
        pass

    def Bt(self):
        pass

    def Bs(self):
        pass

    def Bp(self):
        pass

    def A(self):
        pass

    def At(self):
        pass

    def Af(self):
        pass

    def Ap(self):
        pass

    def R(self):
        pass

    def Rn(self):
        pass

    def D(self):
        pass

    def Da(self):
        pass

    def Dr(self):
        pass

    def Db(self):
        pass

    def Vb(self): 
        pass

    def Vl(self):
        pass   




class LexicalAnalyser:
    
    # letters are handled using isalpha
    # digits are handled using isdigit
    # spaces are handled using isspace
    
    Operator_symbols = "+-*<>&.@/:=~|$!#%^_[]{}'?" +'"'

    """ each lexical analyzer instance should have a program file, a token list, 
    a pointer to the current position, and the text of the program initialized to an empty string"""
    def __init__(self, prog_file):
        self.prog_file = prog_file
        self.tokens = []
        self.pos = 0
        self.text = ""      
    
    def tokenize_spaces(self, token):
        """ Tokenize spaces in the text: Assign "DELETE" """
        while (self.pos < len(self.text) and self.text[self.pos].isspace()):
            token += self.text[self.pos]
            self.pos += 1
        self.tokens.append((token,"DELETE"))
    
    def tokenize_identifier(self, token):
        """ Tokenize identifiers in the text: Assign "IDENTIFIER" """
        while (self.pos < len(self.text) and (self.text[self.pos].isalnum()) or self.text[self.pos] == "_"):
            token += self.text[self.pos]
            self.pos += 1
        self.tokens.append((token,"IDENTIFIER"))
        # print(token)
    
    def tokenize_integer(self, token):
        """ Tokenize integers in the text: Assign "INTEGER" """
        while (self.pos < len(self.text) and self.text[self.pos].isdigit()):
            token += self.text[self.pos]
            self.pos += 1
        self.tokens.append((token,"INTEGER"))
        # print(token)
    
    def tokenize_operator(self, token):
        """ Tokenize operators in the text: Assign "OPERATOR" """
        while (self.pos < len(self.text) and self.text[self.pos] in self.Operator_symbols):
            token += self.text[self.pos]
            self.pos += 1
        self.tokens.append((token,"OPERATOR"))
        # print(token)

    def tokenize_string(self, token):
        """ Tokenize strings in the text: Assign "STRING" """
        while self.pos < (len(self.text)-1) and self.text[self.pos:self.pos+2] != "''":
            token += self.text[self.pos]
            self.pos += 1
        token += "''"  # Append closing quote
        self.pos += 2  # Move past the closing quote
        self.tokens.append((token, "STRING"))
        # print(token) 

    def tokenize_comment(self, token):
        """ Tokenize comments in the text: Assign "COMMENT" """
        while self.pos < len(self.text) and self.text[self.pos] != '\n':
            token += self.text[self.pos]
            self.pos += 1
        self.tokens.append((token, "COMMENT"))
        # print(token)
    
    def tokenize_punction(self, token):
        """ Tokenize symbols in the text: Assign the same symbol """
        self.tokens.append((token,token))
        # print(token)
    
    def lexical_analyser(self):
        with open(self.prog_file, 'r') as file:
            self.text = file.read()
        
        while self.pos < len(self.text):
            char = self.text[self.pos]
            # tokenize spaces
            if char.isspace():
                # print("Space found")
                token=char
                self.pos+=1
                self.tokenize_spaces(token)
                
            # tokenize identifiers
            elif char.isalpha():
                # print("Identifier found")
                token = char
                self.pos += 1
                self.tokenize_identifier(token)
            
            # tokenize integers
            elif char.isdigit():
                # print("Integer found")
                token = char
                self.pos += 1
                self.tokenize_integer(token)

            # tokenize comments
            elif char + self.text[self.pos+1] == "//":
                # print("Comment found")
                token = char+self.text[self.pos+1]
                self.pos += 2
                self.tokenize_comment(token)

            # tokenize strings
            elif char+ self.text[self.pos+1] == "''":
                # print("String found")       
                token = char+self.text[self.pos+1]
                self.pos += 2
                self.tokenize_string(token)
            
            # tokenize operators
            elif char in LexicalAnalyser.Operator_symbols:
                # print("Operator found")
                token = char
                self.pos += 1
                self.tokenize_operator(token)
                
            # tokenize punctuation
            elif char in ['(',')',';',',']:
                # print("Punctuation found")
                self.tokenize_punction(char)
                self.pos += 1
            else:    
                print(f"Error: Invalid character '{char}' found.")
                return
            # print(self.tokens)
        return self.tokens


def main():
    prog_file = sys.argv[1]

    LE = LexicalAnalyser(prog_file)
    tokens = LE.lexical_analyser()
    # for token in tokens:
    #     print(token[0], token[1])
    P=Parser(tokens)


if __name__ == "__main__":
    main()
