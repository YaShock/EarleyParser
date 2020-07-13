"""Compiler

Usage:
    compiler.py template [--app=<app>]
    compiler.py build <source> [--gendir=<gendir>]
    compiler.py bundle <outdir> [--app=<app>] [--gendir=<gendir>]
    compiler.py (-h | --help)
    compiler.py --version

Options:
    -h --help       Show this screen.
    --version       Show version.
    -a --app=<app>  Filename of the generated application [default: app.py].
    -g --gendir=<gendir>    Path to generated parser [default: generated].

"""
import os
import shutil
from parse import metagrammar
from docopt import docopt

app_text = '''from parse import earley
import generated.grammar

g = generated.grammar.grammar
parser = earley.Parser(g)
inp = input()
while inp != 'quit':
    res = parser.parse(inp)
    for r in res:
        r.print()
        r.walk()
    inp = input()
'''


def generate_template(path):
    with open(path, 'w') as file:
        file.write(app_text)


def build(source_path, gen_dir):
    mg = metagrammar.Metagrammar()
    if not os.path.isdir(gen_dir):
        os.mkdir(gen_dir)
    with open(source_path) as src:
        mg.process_grammar(
            src.read(),
            os.path.join(gen_dir, 'grammar.py'))


def bundle(out_dir, app_path, gen_dir):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    shutil.copyfile(app_path, os.path.join(out_dir, app_path))
    if not os.path.isdir(os.path.join(out_dir, 'parse')):
        os.mkdir(os.path.join(out_dir, 'parse'))
    shutil.copyfile(
        'parse/earley.py',
        os.path.join(out_dir, 'parse/earley.py'))
    shutil.copyfile(
        'parse/grammar.py',
        os.path.join(out_dir, 'parse/grammar.py'))
    if not os.path.isdir(os.path.join(out_dir, 'generated')):
        os.mkdir(os.path.join(out_dir, 'generated'))
    shutil.copyfile(
        os.path.join(gen_dir, 'grammar.py'),
        os.path.join(out_dir, 'generated/grammar.py'))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Compiler 1.0')
    print(arguments)
    if arguments['template'] is True:
        generate_template(arguments['--app'])
    elif arguments['build'] is True:
        build(
            arguments['<source>'],
            arguments['--gendir'])
    else:
        bundle(
            arguments['<outdir>'],
            arguments['--app'],
            arguments['--gendir'])
