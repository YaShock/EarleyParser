from tkinter import ttk
import tkinter as tk

app_text = '''from parse import *

grammar = grammar.Grammar()
cb = context.ContextBuilder(grammar)
cb.build()
parser = earley.Parser(grammar)

inp = input()
while inp != 'quit':
    lst = parser.parse(inp)
    for t in lst:
        t.print()
        context.walk_tree(t)
    inp = input()'''

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame_cf = tk.Frame(self.frame)
        self.frame_fn = tk.Frame(self.frame)

        tk.Label(self.frame_cf, text="Grammar").pack(side="top")
        self.text_cf = tk.Text(self.frame_cf, width=40)
        self.text_cf.pack(fill="both", expand=True)
        tk.Label(self.frame_fn, text="Functions").pack(side="top")
        self.text_fn = tk.Text(self.frame_fn, width=40)
        self.text_fn.pack(fill="both", expand=True)

        self.frame_cf.pack(side="left", fill="both", padx=15, expand=True)
        self.frame_fn.pack(side="right", fill="both", padx=15, expand=True)
        self.frame.pack(side="top", fill="both", expand=True)

        self.frame_btn = tk.Frame(self)
        self.frame_btn.pack(side="bottom", fill="x", expand=True)

        ttk.Button(self.frame_btn, text="Create functions", command=self.create_functions).pack(fill="x")
        ttk.Button(self.frame_btn, text="Generate app template", command=self.app_template).pack(fill="x")
        ttk.Button(self.frame_btn, text="Compile", command=self.compile).pack(fill="x")
        ttk.Button(self.frame_btn, text="Compile and run", command=self.compile_and_run).pack(fill="x")

    def create_functions(self):
        output = ''
        text = self.text_fn.get("1.0","end-1c")

        for line in self.text_cf.get("1.0","end-1c").split('\n'):
            if line[0] == '/' and line[1] == '/':
                continue
            lst = line.split('::=')
            if len(lst) > 2:
                raise ValueError('Invalid rule syntax: more than one ::=')
            elif len(lst) == 2:
                fn = lst[1].strip()
                fn_enter = 'def ' + fn + '_enter(children):'
                fn_exit = 'def ' + fn + '_exit(children):'
                if fn_enter not in text:
                    output += fn_enter + '\n    pass\n'
                if fn_exit not in text:
                    output += fn_exit + '\n    pass\n'
        self.text_fn.insert(1.0, output)

    def compile(self):
        grammar_file = open('generated/grammar.cf', 'w')
        grammar_file.write(self.text_cf.get("1.0","end-1c"))
        grammar_file.close()
        fn_file = open('generated/semantics.py', 'w')
        fn_file.write(self.text_fn.get("1.0","end-1c"))
        fn_file.close()

    def compile_and_run(self):
        self.compile()
        root.destroy()
        import app

    def app_template(self):
        app_file = open('app.py', 'w')
        app_file.write(app_text)
        app_file.close()

root = tk.Tk()
root.title('Compiler')
root.geometry("700x520+100+100")

app = Application(master=root)
app.mainloop()