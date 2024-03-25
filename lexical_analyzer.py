import sys

class Lexer:
    # Define the static tokens list
    tokens = [
        # Add your tokens here
    ]

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            char = self.text[self.pos]


        return tokens

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python myrpal.py file_name")
        sys.exit(1)

    file_name = sys.argv[1]
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            for token in tokens:
                print(token)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

   