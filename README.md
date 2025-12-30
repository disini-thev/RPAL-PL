# RPAL Interpreter

This repository contains a complete implementation of a **Lexical Analyzer**, **Parser**, and **CSE Machine** for the RPAL (Recursive Programming Algorithmic Language) programming language. The project was developed as assessment for the module Programming Languages.

## Project Overview
The primary goal was to implement an interpreter that parses RPAL source code and executes it using a Control-Structure Evaluation (CSE) machine. The implementation follows these stages:
1.  **Lexical Analysis:** Tokenizes the source text.
2.  **Parsing:** Constructs an Abstract Syntax Tree (AST) based on RPAL grammar.
3.  **Standardization:** Converts the AST into a Standardized Tree (ST).
4.  **CSE Machine:** Evaluates the ST to produce the final output.

---

## Program Structure
The project is organized into six main sections:
* **Main Program:** Orchestrates the flow from file input to final execution.
* **Lexical Analyzer:** Handles tokenization of identifiers, integers, operators, strings, comments, and punctuation.
* **Parser:** A recursive descent parser that builds the AST according to RPAL non-terminals.
* **Tree Function:** Utility class used to manage tree nodes and standardization.
* **Stack Function:** Utility class to manage the control stack during parsing and evaluation.
* **CSE Machine:** The execution engine that manages control structures, environments, and stacks.

---

## Features
### Lexical Analysis
* Identifies and classifies tokens such as `IDENTIFIER`, `KEYWORD`, `INTEGER`, `OPERATOR`, and `STRING`.
* Includes a **Screener** function to remove `DELETE` (spaces) and `COMMENT` tokens.

### CSE Machine Evaluation
* **Expression Evaluation:** Supports integers, strings, lambdas, gammas (function application), and various unary/binary operators (e.g., `+`, `-`, `*`, `/`, `**`, `gr`, `eq`, `and`, `or`, `aug`).
* **Built-in Functions:** Includes support for `Print`, `Order`, `Conc`, `Stem`, `Stern`, `Isinteger`, and more.

---

## Usage

### Prerequisites
* Python 3.x installed on your system.

### Running the Interpreter
To execute an RPAL program file and see the result:
Sample Test file : test.txt 
```bash
python .\myrpal.py <file_name>
```

Use `-ast` switch to get the Abstract Syntax Tree

