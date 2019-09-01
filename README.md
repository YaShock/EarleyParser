# EarleyParser

This repository contains a flexible parser generator which can be build by adding rules and then parse any CF grammar. There is also a metaparser that can parse a grammar with a custom syntax that is a mesh between EBNF and JavaCC grammar definition.   Rules can be added just like in EBNF and each rule has a _begin_ and _end_ clouse that can contain any Python code. Terminals can be saved in variables.

## Example

There is an example grammar included in examples/grammar.cf that produces a simple algebraic expression evaluator.

## Metacompiler

There are two additional programs to aid parser generation. For CLI you can use compiler.py and a simple GUI application is contained in compiler_gui.py. 

## Building

You can produce a sample grammar by the following steps:  
Build the example grammar `python3 compiler.py build examples/grammar.cf`. This will produce the generated parser in the _generated_ folder. Next, generate a simple template for reading input, calling the parser and printing the result. A template is provided when you run `python3 compiler.py template`. Finally, you can bundle the generated files into a stand-alone python module containing all the necessary files to parse your grammar in the output directory: `python3 compiler.py bundle output`.
