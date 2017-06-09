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

        self.btn_compile = ttk.Button(self, text="Compile", command=self.compile)
        self.btn_compile.pack(side="bottom", fill="x")

    def compile(self):
        grammar_file = open('grammar.cf', 'w')
        grammar_file.write(self.text_cf.get("1.0","end-1c"))
        grammar_file.close()
        fn_file = open('semantics.py', 'w')
        fn_file.write(self.text_fn.get("1.0","end-1c"))
        fn_file.close()
        root.destroy()
        import app

root = tk.Tk()
root.title('Compiler')
root.geometry("700x500+100+100")

app = Application(master=root)
app.mainloop()