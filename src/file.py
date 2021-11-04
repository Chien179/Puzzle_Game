import tkinter as tk
from tkinter import filedialog

class File:
    def __init__(self):
        self.root = tk.Tk()  # init a Tkapp
        self.root.withdraw()  # hide TKapp

    def file(self):
        filetypes = (
            ('image file', '*.jpg'),
            ('image file', '*.png')
        )

        file_path = filedialog.askopenfilename(title='Open a file',
                                               initialdir='/',
                                               filetypes=filetypes)

        self.root.destroy()

        return file_path