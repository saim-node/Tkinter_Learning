import tkinter as tk

root = tk.Tk()
root.title("Basic Tkinter Example")
root.geometry("300x200")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

btn = tk.Button(root, text="Click Me!")
btn.pack()




root.mainloop()
