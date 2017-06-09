import earley, grammar, context, semantics
from tkinter import ttk
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame_cf = tk.Frame(self.frame)
        self.frame_fn = tk.Frame(self.frame)

       	tk.Label(self.frame_cf, text="Grammar").pack(side="top")
       	self.text_cf = tk.Text(self.frame_cf, width=40)
       	self.text_cf.pack(fill="both")
       	tk.Label(self.frame_fn, text="Functions").pack(side="top")
       	self.text_fn = tk.Text(self.frame_fn, width=40)
       	self.text_fn.pack(fill="both")

       	self.frame_cf.pack(side="left", fill="both", padx=15)
       	self.frame_fn.pack(side="right", fill="both", padx=15)
       	self.frame.pack(side="top", fill="both")

        self.btn_compile = ttk.Button(self, text="Compile", command=root.destroy)
        self.btn_compile.pack(side="bottom", fill="x")

root = tk.Tk()
root.title('Compiler')
root.geometry("700x500+100+100")

app = Application(master=root)
app.mainloop()

# file = open('math.cf')
# grammar = grammar.Grammar()
# cb = context.ContextBuilder(grammar)
# cb.read_file(file)
# file.close()
# parser = earley.Parser(grammar)

# module = __import__('generated')
# module.create()

# for rule in grammar.rules:
#     d = module.dict[id(rule)]
#     rule.fn_enter = d[0]
#     rule.fn_exit = d[1]

# lst = parser.parse('2 / 4 - 3 * 3 + 10')
# for t in lst:
#     t.print()
#     context.walk_tree(t)

# lst = parser.parse('load whatever')
# for t in lst:
#     t.print()

# lst = parser.parse("get,terms;frequency,between;1.5;and,4.8")
# for t in lst:
#     t.print()

# lst = parser.parse("delete words : lel asd 20")
# for t in lst:
#     t.print()