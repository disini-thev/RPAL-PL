import sys

# read the text file, append tho token and the token type as a tuple to a list "tokens"
def lexical_analyser(prog_file):
    with open(prog_file, 'r') as file:
        text = file.read()
        pos = 0
        tokens = []
    
    # letters are handled using isalpha
    # digits are handled using isdigit
    # spaces are handled using isspace
        
    # to handle operators:
    Operator_symbols = "+-*<>&.@/:=~|$!#%^_[]{}'?" +'"'

    # functions to tokenize each lexeme type
    def tokenize_spaces(token):
        """ Tokenize spaces in the text: Assign "DELETE" """
        while (pos < len(text) and text[pos].isspace()):
            token += text[pos]
            pos += 1
        tokens.append((token,"DELETE"))
    
    def tokenize_identifier(token):
        """ Tokenize identifiers in the text: Assign "IDENTIFIER" """
        while (pos < len(text) and (text[pos].isalnum()) or text[pos] == "_"):
            token += text[pos]
            pos += 1
        tokens.append((token,"IDENTIFIER"))
    
    def tokenize_integer(token):
        """ Tokenize integers in the text: Assign "INTEGER" """
        while (pos < len(text) and text[pos].isdigit()):
            token += text[pos]
            pos += 1
        tokens.append((token,"INTEGER"))
    
    def tokenize_operator(token):
        """ Tokenize operators in the text: Assign "OPERATOR" """
        while (pos < len(text) and text[pos] in Operator_symbols):
            token += text[pos]
            pos += 1
        tokens.append((token,"OPERATOR"))

    def tokenize_string(token):
        """ Tokenize strings in the text: Assign "STRING" """
        # complete 
        pass

    def tokenize_comment(token):
        """ Tokenize comments in the text: Assign "COMMENT" """
        # complete 
        pass
    
    def tokenize_punction():
        """ Tokenize symbols in the text: Assign the same symbol """
        tokens.append((text[pos],text[pos]))
    

            
    while pos < len(text):
            char = text[pos]
            # tokenize spaces
            if char.isspace():
                token=char
                pos+=1
                tokenize_spaces(token)
            
            # tokenize identifiers
            elif char.isalpha():
                token = char
                pos += 1
                tokenize_identifier(token)
            
            # tokenize operators
            elif char.isdigit():
                token = char
                pos += 1
                tokenize_integer(token)
            
            # tokenize 
            
            print(f"Error: Invalid character '{char}' found.")
            return
    print(tokens)

def main():
    if len(sys.argv) != 2:
        print("Error in command line arguments. Usage: python myrpal.py file_name")
        return

    prog_file = sys.argv[1]

    # lexical_analyser(prog_file)
    Operator_symbols = "+-*<>&.@/:=~|$!#%^_[]{}'?" +'"'
    print(Operator_symbols)
if __name__ == "__main__":
    main()
