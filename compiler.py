from tkinter import ttk
import tkinter as tk

app_text = '''from parse import *

text = ''
with open('generated/grammar.cf', 'r') as grammar_file:
    text = grammar_file.read()

mg = metagrammar.Metagrammar()
g = mg.process_grammar(text, 'generated/functions.py')
parser = earley.Parser(g)    
res = parser.parse(input())
for r in res:
    r.print()
    r.walk()'''

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame_cf = tk.Frame(self.frame)
        self.frame_fn = tk.Frame(self.frame)
        self.frame_btn = tk.Frame(self)

        self.frame_btn.pack(fill="x", side="bottom", expand=False, anchor="s")

        ttk.Button(self.frame_btn, text="Generate app template", command=self.app_template).pack(fill="x")
        ttk.Button(self.frame_btn, text="Compile", command=self.compile).pack(fill="x")
        ttk.Button(self.frame_btn, text="Compile and run", command=self.compile_and_run).pack(fill="x")

        tk.Label(self.frame_cf, text="Grammar").pack(side="top")
        self.text_cf = tk.Text(self.frame_cf, width=5)
        self.text_cf.pack(fill="both", expand=True)

        self.frame_cf.pack(side="left", fill="both", padx=15, expand=True)
        self.frame.pack(side="top", fill="both", expand=True, anchor="center", pady=15)

    def compile(self):
        grammar_file = open('generated/grammar.cf', 'w')
        grammar_file.write(self.text_cf.get("1.0","end-1c"))
        grammar_file.close()

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
root.geometry("500x350+100+100")

app = Application(master=root)
app.mainloop()