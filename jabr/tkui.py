#!/usr/bin/env python

import os
import sys

if sys.version_info[0] >= 3:
    # Python 3 or greater
    import tkinter
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
else:
    import Tkinter as tkinter
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

class TkUI(tkinter.Tk):
    def __init__(self, parent, jabr):
        tkinter.Tk.__init__(self, parent)
        self.tkinter = tkinter
        self.parent = parent
        self.jabr = jabr

        self.initialize_ui()

    def initialize_ui(self):
        self.grid()

        # About
        self.about = tkinter.Toplevel()
        self.about.title('About')
        self.about.resizable(0, 0)
        self.about.protocol('WM_DELETE_WINDOW', self.about.withdraw)
        if os.name == 'nt':
            self.about.attributes('-toolwindow', 1)
        self.about.withdraw()

        about_grp = tkinter.LabelFrame(self.about, padx=5, pady=10, borderwidth=0)
        about_grp.grid(column=0, row=0, sticky='news')

        about_ver_label = tkinter.Label(about_grp, text='Version:')
        about_ver_label.grid(column=0, row=0, sticky='e')
        about_ver = tkinter.Label(about_grp, text=self.jabr.version)
        about_ver.grid(column=1, row=0, sticky='w')

        about_author_label = tkinter.Label(about_grp, text='Author:')
        about_author_label.grid(column=0, row=1, sticky='e')
        about_author = tkinter.Label(about_grp, text='pidstuff')
        about_author.grid(column=1, row=1, sticky='w')

        about_license_label = tkinter.Label(about_grp, text='License:')
        about_license_label.grid(column=0, row=2, sticky='e')
        about_license = tkinter.Label(about_grp, text='GPLv3')
        about_license.grid(column=1, row=2, sticky='w')

        about_grp.grid_columnconfigure(0, weight=1)
        about_grp.grid_columnconfigure(1, weight=1)
        self.about.grid_columnconfigure(0, weight=1)

        # Add, Remove, Clear & About buttons
        add_files_btn = tkinter.Button(self, text='Add', command=self.add_files, width=6)
        add_files_btn.grid(column=0, row=0, sticky='w')

        rem_files_btn = tkinter.Button(self, text='Remove', command=self.remove_files, width=6)
        rem_files_btn.grid(column=1, row=0, sticky='w')

        clr_files_btn = tkinter.Button(self, text='Clear', command=self.clear_files, width=6)
        clr_files_btn.grid(column=2, row=0, sticky='w')

        abt_btn = tkinter.Button(self, text='About', command=self.show_about, width=6)
        abt_btn.grid(column=19, row=0, columnspan=2, sticky='e')

        # Before & After Listboxes
        self.oldname_lstbx = tkinter.Listbox(selectmode='extended', exportselection=0, width=28)
        self.oldname_lstbx.grid(column=0, row=1, columnspan=10, sticky='news')
        self.oldname_lstbx.bind('<<ListboxSelect>>', self.sync_selection)
        self.oldname_lstbx.configure(yscrollcommand=lambda *args: self.listbox_scrollbar.set(*args))

        self.newname_lstbx = tkinter.Listbox(selectmode='extended', exportselection=0, width=28)
        self.newname_lstbx.grid(column=10, row=1, columnspan=10, sticky='news')
        self.newname_lstbx.bind('<<ListboxSelect>>', self.sync_selection)
        self.newname_lstbx.configure(yscrollcommand=lambda *args: self.listbox_scrollbar.set(*args))

        self.listbox_scrollbar = tkinter.Scrollbar(orient='vertical', command=self.yscroll)
        self.listbox_scrollbar.grid(column=20, row=1, sticky='nes')

        # Filename & Extension Group
        self.filepart_options = ('Filename Only', 'Extension Only', 'Filename & Extension')
        self.filepart_var = tkinter.StringVar()
        self.filepart_var.set(self.filepart_options[0])
        filepart_optionmenu = tkinter.OptionMenu(
            self,
            self.filepart_var,
            *self.filepart_options,
            command=self.update_newnames
        )
        filepart_optionmenu.configure(width=10)
        filepart_optionmenu.grid(column=11, row=2, columnspan=10, sticky='news', padx=(0, 5))

        # Rename Button
        self.rename_btn = tkinter.Button(self, text='Rename', command=self.rename_files)
        self.rename_btn.config(state='disabled')
        self.rename_btn.grid(column=19, row=4, columnspan=2, sticky='e', padx=5, pady=(0, 5))

        # Initialize module options & group
        self.rename_mod_optionmenu = tkinter.Frame(self)
        self.module_grp = tkinter.LabelFrame(self, padx=5, pady=5)
        self.initialize_rename_mod_optionmenu()

        # Makes the two Listboxes stretch
        self.grid_columnconfigure(9, weight=1)
        self.grid_columnconfigure(19, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def initialize_rename_mod_optionmenu(self):
        self.rename_mod_optionmenu.destroy()
        rename_mod_options = list(self.jabr.mods.keys())
        rename_mod_options.sort()
        self.rename_mod_var = tkinter.StringVar()

        if not rename_mod_options:
            self.show_error('There are no modules available for use.')
            sys.exit()

        self.rename_mod_var.set(rename_mod_options[0])
        self.rename_mod_optionmenu = tkinter.OptionMenu(
            self,
            self.rename_mod_var,
            *rename_mod_options,
            command=self.show_module
        )
        self.rename_mod_optionmenu.configure(width=10)
        self.rename_mod_optionmenu.grid(column=0, row=2, columnspan=10, sticky='news', padx=(5, 0))
        self.show_module(self.rename_mod_var.get())

    def show_about(self):
        abt_width = 240
        abt_height = 200
        self.about.geometry(
            '{0}x{1}+{2}+{3}'.format(
                abt_width,
                abt_height,
                self.winfo_x() + int(self.winfo_width()/2) - int(abt_width/2),
                self.winfo_y() + int(self.winfo_height()/2) - int(abt_height/2)
            )
        )
        self.about.deiconify()

    def add_files(self):
        files = filedialog.askopenfilenames(title='Select files to rename')
        files = self.tk.splitlist(files) # Windows fix
        addedfiles = self.jabr.files.add(files)
        for af in addedfiles:
            filename = os.path.basename(af)
            self.oldname_lstbx.insert('end', filename)
        self.update_newnames()

    def remove_files(self):
        files = self.oldname_lstbx.curselection()
        self.jabr.files.remove(files)
        for f in reversed(files):
            self.oldname_lstbx.delete(f)
            self.newname_lstbx.delete(f)
        self.update_newnames()

    def clear_files(self):
        self.jabr.files.clear()
        self.oldname_lstbx.delete(0, 'end')
        self.newname_lstbx.delete(0, 'end')
        self.rename_btn.config(state='disabled')

    def rename_files(self):
        newnames = self.newname_lstbx.get(0, 'end')
        output = self.jabr.files.rename(newnames)

        self.oldname_lstbx.delete(0, 'end')
        self.newname_lstbx.delete(0, 'end')
        for r in output['newoldnames']:
            self.oldname_lstbx.insert('end', r)

        if (output['errormsg']):
            self.show_error(output['errormsg'], output['errorlog'])
        self.update_newnames()

    def show_module(self, modname):
        """ Calls the given module's 'show_ui' function
            which initializes the module's interface
        """
        self.module_grp.destroy()
        self.module_grp = tkinter.LabelFrame(self, padx=5, pady=5)
        self.module_grp.grid(column=0, row=3, columnspan=32, sticky='news', padx=5, pady=5)
        try:
            self.jabr.mods[modname]['object'].show_ui(self)
        except Exception as e:
            self.show_error(': '.join([modname, str(e)]), e)
            self.jabr.remove_mod(modname)
            self.initialize_rename_mod_optionmenu()
        self.update_newnames()

    def update_newnames(self, *_):
        """ Gets the part of the file to be renamed,
            sends it to the selected module's 'update_filenames' function,
            then inserts the results into newname_lstbx
        """
        newnames = []
        filepart = 'fullname'
        module = self.jabr.mods[self.rename_mod_var.get()]

        self.oldname_lstbx.selection_clear(0, 'end')
        self.newname_lstbx.selection_clear(0, 'end')
        if self.filepart_var.get() == self.filepart_options[0]:
            filepart = 'base'
        if self.filepart_var.get() == self.filepart_options[1]:
            filepart = 'ext'
        newnames = [f[filepart] for f in self.jabr.files.list]
        if not newnames:
            return

        try:
            newnames = module['object'].update_filenames(newnames)
        except Exception as e:
            self.show_error(': '.join([self.rename_mod_var.get(), str(e)]))
            self.jabr.remove_mod(self.rename_mod_var.get())
            self.initialize_rename_mod_optionmenu()

        self.newname_lstbx.delete(0, 'end')
        for i, f in enumerate(self.jabr.files.list):
            if filepart == 'base':
                if f['ext']:
                    newnames[i] = '.'.join([newnames[i], f['ext']])
            elif filepart == 'ext':
                if newnames[i]:
                    newnames[i] = '.'.join([f['base'], newnames[i]])
            if f['fullname'] == newnames[i]:
                newnames[i] = ''

            self.newname_lstbx.insert('end', newnames[i])

        self.validate_newnames(newnames)

    def validate_newnames(self, newnames):
        """ Gets a set of non-unique entries and counts the number
            of blanks in newnames in order to highlight duplicate entries
            and set the state for the Rename button
        """
        blanks = 0
        duplicates = {n for n in newnames if newnames.count(n) > 1 and n}
        self.rename_btn.config(state='normal')
        for i, n in enumerate(newnames):
            if not n:
                blanks += 1
            if n in duplicates:
                self.rename_btn.config(state='disabled')
                self.newname_lstbx.itemconfig(i, fg='red')

        if blanks == len(newnames):
            self.rename_btn.config(state='disabled')

    def sync_selection(self, event):
        """ Gets the active ListBox selection,
            clears the selected values in the other ListBox,
            then finally syncs the active selection with the other ListBox
        """
        evt = event.widget
        lstbx = self.oldname_lstbx
        curselection = evt.curselection()

        if curselection == self.oldname_lstbx.curselection():
            lstbx = self.newname_lstbx
        lstbx.selection_clear(0, 'end')

        for i in curselection:
            self.newname_lstbx.selection_set(i)
            self.oldname_lstbx.selection_set(i)

    def yscroll(self, *args):
        self.oldname_lstbx.yview(*args)
        self.newname_lstbx.yview(*args)

    def show_error(self, errmsg, log=''):
        messagebox.showerror('Error', errmsg)
        if log:
            self.jabr.logerror(log)
