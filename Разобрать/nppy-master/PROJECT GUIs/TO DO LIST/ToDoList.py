import os
import sys
from tkinter import *
from tkinter import messagebox


class ToDoList:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.overrideredirect(True)
        self.master.title('TO-DO LIST')
        self.master.after(0, self.master.deiconify)
        self.master.wm_attributes("-topmost", 'true')
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.file_name = os.path.abspath(os.path.join('.', 'to_do_list.txt'))

        self.buttons_attributes = {'bd': 1, 'fg': 'white', 'bg': '#002157', 'relief': GROOVE, 'cursor': 'hand2', 'activeforeground': 'white', 'activebackground': '#002157'}

        self.screenwidth, self.screenheight = self.master.winfo_screenwidth() - 400, self.master.winfo_screenheight()
        self.width, self.height = 400, self.screenheight - 40
        self.master.geometry(f'{self.width}x{self.height}+{self.screenwidth}+0')

        self.is_collapsed = False
        self.collapse_frame = Frame(self.master)
        self.collapse_button = Button(self.collapse_frame, text='>>', **self.buttons_attributes, height=46, command=self.collapse)
        self.collapse_button.grid(row=0, column=0)
        self.collapse_frame.place(x=0, y=0)

        self.label_frame = Frame(self.master)
        self.label = Label(self.label_frame, text='MY TO-DO LIST', bg='#002157', fg='white', font=('Courier', 28))
        self.label.grid(row=0, column=0)
        self.label_frame.place(x=210, y=25, anchor="center")

        self.entry_var = StringVar()
        self.entry_frame = Frame(self.master, bg='#002157')
        self.entry_box = Entry(self.entry_frame, font=("Arial", 15), fg='grey', textvariable=self.entry_var)
        self.entry_var.set('I have to do ...')
        self.add_button = Button(self.entry_frame, text='ADD', width=10, height=2, bg='Green', fg='white', activebackground='Green', activeforeground='white', cursor='hand2', command=self.add_command)
        self.entry_box.grid(row=0, column=0)
        self.add_button.grid(row=0, column=1, padx=20)
        self.entry_frame.place(x=40, y=50)

        self.list_box_frame = Frame(self.master, relief="sunken")
        self.list_box = Listbox(self.list_box_frame, bg='#002157', fg='white', width=27, height=23, font=('Courier', 15), selectmode=MULTIPLE)
        self.list_box.grid(row=0, column=0)
        self.list_box_frame.place(x=40, y=103)

        self.scrollbar = Scrollbar(self.list_box_frame, orient="vertical", command=self.list_box.yview)

        self.delete_menu = Menu(self.master, tearoff=0)
        self.delete_menu.add_command(label="Delete from list", command=self.popup_delete)
        self.delete_menu.add_command(label="Delete from list and file", command=lambda: self.popup_delete(mode='from both file and list'))

        self.load_prev_frame = Frame(self.master)
        self.load_prev_button = Button(self.load_prev_frame, text='LOAD PREVIOUS DATA', width=30, height=2, **self.buttons_attributes, command=self.add_to_list)
        self.load_prev_button.grid(row=0, column=0)
        self.load_prev_frame.place(x=150, y=self.master.winfo_screenheight() - 126)

        self.del_prev_frame = Frame(self.master)
        self.del_prev_button = Button(self.del_prev_frame, text='DELETE ALL PREVIOUS DATA', width=30, height=2, **self.buttons_attributes, command=lambda: self.check_for_file(clear_all=True))
        self.del_prev_button.grid(row=0, column=0)
        self.del_prev_frame.place(x=150, y=self.master.winfo_screenheight() - 87)

        self.clear_frame = Frame(self.master)
        self.clear_button = Button(self.clear_frame, text='CLEAR', width=13, height=4, **self.buttons_attributes, command=self.clear)
        self.clear_button.grid(row=0, column=0, ipadx=4, ipady=4)
        self.clear_frame.place(x=40, y=self.master.winfo_screenheight() - 125)

        self.exit_frame = Frame(self.master)
        self.exit_button = Button(self.exit_frame, text='X', font=('Arial Black', 9, 'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', bd=0, command=self.master.destroy)
        self.exit_button.grid(row=0, column=0, ipadx=4, ipady=1)
        self.exit_frame.place(x=0, y=self.master.winfo_screenheight() - 67)

        self.master.bind('<Button-3>', self.popup_menu)
        self.master.bind('<Button-1>', self.key_bindings)
        self.entry_box.bind('<FocusIn>', self.key_bindings)
        self.add_button.bind('<FocusIn>', self.key_bindings)

        self.add_to_list()
        self.show_scrollbar()

        self.master.config(bg='#002157')
        self.master.mainloop()

    def key_bindings(self, event):
        '''
        Different actions when user click to different widgets
        '''

        get = self.entry_var.get().strip()

        if event.widget == self.entry_box and get == 'I have to do ...':
            self.entry_var.set('')
            self.entry_box.config(fg='black')

        elif event.widget != self.entry_box:
            if not get:
                self.entry_var.set('I have to do ...')
                self.entry_box.config(fg='grey')

        if event.widget not in [self.entry_box, self.add_button]:
            self.master.focus()

    def collapse(self):
        '''
        Expand and shrink window
        '''

        if self.is_collapsed:
            self.is_collapsed = False
            self.master.geometry('{}x{}+{}+{}'.format(400, self.height, self.master.winfo_screenwidth() - 400, 0))
            self.collapse_button.config(text='>>')

        else:
            self.is_collapsed = True
            self.master.geometry('{}x{}+{}+{}'.format(25, self.height, self.master.winfo_screenwidth() - 25, 0))
            self.collapse_button.config(text='<<')

    def show_scrollbar(self):
        '''
        Show scrollbar when text is more than the text area
        '''

        if len(self.list_box.get(0, END)) > self.list_box.cget('height'):
            self.scrollbar.grid(column=1, row=0, sticky=N + S)
            self.list_box.config(yscrollcommand=self.scrollbar.set)
            self.master.after(100, self.hide_scrollbar)

        else:
            self.master.after(100, self.show_scrollbar)

    def hide_scrollbar(self):
        '''
        Hide scrollbar when text is less than the text area
        '''

        if len(self.list_box.get(0, END)) <= self.list_box.cget('height'):
            self.scrollbar.grid_forget()
            self.list_box.config(yscrollcommand=None)
            self.master.after(100, self.show_scrollbar)

        else:
            self.master.after(100, self.hide_scrollbar)

    def popup_menu(self, event=None):
        '''
        Display menu when right click is clicked
        '''

        try:
            selection = self.list_box.curselection()

            if selection:
                self.delete_menu.entryconfig(0, state=NORMAL)
                self.delete_menu.entryconfig(1, state=NORMAL)

            else:
                self.delete_menu.entryconfig(0, state=DISABLED)
                self.delete_menu.entryconfig(1, state=DISABLED)

            self.delete_menu.tk_popup(event.x_root, event.y_root)

        finally:
            self.delete_menu.grab_release()

    def check_for_file(self, clear_all=False):
        '''
        Create "to_do_list.txt" file if not exists or delete the contents of
        file if user press delete previous data
        '''

        if not os.path.exists(self.file_name) or clear_all:
            with open(self.file_name, 'w'):
                pass

            self.clear()

    def save_content(self, contents):
        '''
        Save user list to the file
        '''

        with open(self.file_name, 'a') as file:
            for content in contents:
                file.write(f'{content}\n')

    def read_content(self):
        '''
        Read contents of the file
        '''

        with open(self.file_name, 'r') as file:
            contents = [content.strip('\n') for content in file.readlines()]

        return contents

    def add_to_list(self, data=None):
        '''
        Get the contents from the file and add them to the list box
        '''

        if os.path.exists(self.file_name):
            if data:
                contents = data

            else:
                contents = self.read_content()

            self.clear()

            for index, content in enumerate(contents):
                self.list_box.insert(index, content.strip('\n'))

    def add_command(self, event=None):
        '''
        Command for add button
        '''

        get_from_entry_box = self.entry_box.get().strip()

        if get_from_entry_box and get_from_entry_box != 'I have to do ...':
            self.check_for_file()
            self.save_content([get_from_entry_box])
            self.add_to_list()

            self.entry_box.delete(0, END)

        else:
            messagebox.showerror('Invalid Entry', 'Enter something in the entry box')

    def clear(self):
        '''
        Command for clear button
        '''

        self.list_box.delete(0, END)

    def popup_delete(self, mode=None):
        '''
        Command when user right clicks
        '''

        selection = self.list_box.curselection()
        from_list = [value for index, value in enumerate(self.list_box.get(0, END)) if index not in selection]

        if mode == 'from both file and list':
            self.check_for_file(clear_all=True)

            if from_list:
                self.save_content(from_list)
                self.add_to_list(from_list)

        else:
            self.clear()

            if from_list:
                self.add_to_list(from_list)

    def resource_path(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    ToDoList()
