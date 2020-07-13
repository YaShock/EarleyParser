# EarleyParser

This repository contains a flexible parser generator which can be build by adding rules and then parse any CF grammar. There is also a metaparser that can parse a grammar with a custom syntax that is a mesh between EBNF and JavaCC grammar definition.   Rules can be added just like in EBNF and each rule has a _begin_ and _end_ clouse that can contain any Python code. Terminals can be saved in variables.

## Example

There is an example grammar included in examples/grammar.cf that produces a simple algebraic expression evaluator.

## Building grammars

The algorithm itself is found in *earley.py* module. The Parser object needs a grammar instance, which is given in *grammar.py* module. To initialize the Parser just create a Grammar instance and add production rules.

## Generating grammars

The alternative method for creating grammars is to generate them with a Metagrammar. It parses an EBNF based grammar description and generates the desired grammar. The description consists of tokens and production rules with a powerful method to add Python function definitions which are executed before or after the rule is visited.

### Tokens

Tokens are given by names and consuming values. The values can be regular expressions (given by "" quotes) or literals (given by '' quotes) with or operators. There is a special token, SKIP, that expresses which tokens should ignored in the generated grammar.

### Production rules

Production rules are given with a function notation, where the function name is the left side of the rule, the right side is given within the 'expansion', where the given variable can be expanded to every set of symbol strings seperated by | (or) operators.
The string of terminals is given by comma seperated (,) list, where each variable can be saved in a Python identifier that can be accessed in 'end' section. The 'begin' describes a Python code that runs before the rule is visited, and the 'end' describes a Python code that runs after the rule is visited.

## Metacompiler

There are two additional programs to aid parser generation. For CLI you can use compiler.py and a simple GUI application is contained in *compiler_gui.py*. 

## Building

You can produce a sample grammar by the following steps:  
Build the example grammar `python3 compiler.py build examples/grammar.cf`. This will produce the generated parser in the _generated_ folder. Next, generate a simple template for reading input, calling the parser and printing the result. A template is provided when you run `python3 compiler.py template`. Finally, you can bundle the generated files into a stand-alone python module containing all the necessary files to parse your grammar in the output directory: `python3 compiler.py bundle output`.
