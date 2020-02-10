#!/usr/bin/env python

LABEL = 'Replace'

import re

class Module:
    def __init__(self):
        self.tkui = False
        self.ui = {}
        self.options = {
            'find': 'The text or pattern to find',
            'replacer': 'The text to replace it with',
            'regex': { 'False': 0, 'True':1 }
        }
        self.config = {
            'find': '',
            'replacer': '',
            'regex': self.options['regex']['False']
        }

    def show_ui(self, tkui):
        self.tkui = tkui
        find_label = tkui.tkinter.Label(tkui.module_grp, text='Replace:')
        find_label.grid(column=0, row=0, sticky='e')
        find_entry = tkui.tkinter.Entry(tkui.module_grp, width=1)
        find_entry.grid(column=1, row=0, sticky='ew')
        find_entry.bind('<KeyRelease>', lambda _: self.update_ui({ 'find': find_entry.get() }))
        find_entry.insert(0, self.config['find'])
        self.ui['find_entry'] = find_entry

        regex_var = tkui.tkinter.IntVar()
        regex_var.set(self.config['regex'])
        regex_chkbx = tkui.tkinter.Checkbutton(
            tkui.module_grp,
            text='Regex',
            variable=regex_var,
            command=lambda: self.update_ui({ 'regex': regex_var.get() })
        )
        regex_chkbx.grid(column=2, row=0, sticky='w')

        replacer_label = tkui.tkinter.Label(tkui.module_grp, text='With:')
        replacer_label.grid(column=0, row=1, sticky='e')
        replacer_entry = tkui.tkinter.Entry(tkui.module_grp, width=1)
        replacer_entry.grid(column=1, row=1, sticky='ew')
        replacer_entry.bind('<KeyRelease>', lambda _: self.update_ui({ 'replacer': replacer_entry.get() }))
        replacer_entry.insert(0, self.config['replacer'])
        self.ui['replacer_entry'] = replacer_entry

        tkui.module_grp.grid_columnconfigure(1, weight=1)

    def update_ui(self, setting):
        self.config.update(setting)
        self.tkui.update_newnames()

    def update_filenames(self, files):
        find = self.config['find']
        replacer = self.config['replacer']
        is_regex = self.config['regex']
        if not find:
            return files

        if is_regex:
            newfilenames = []
            for f in files:
                try:
                    newfilenames.append(re.sub(find, replacer, f))
                except re.error:
                    newfilenames.append(f)
            return newfilenames
        return [f.replace(find, replacer) for f in files]

module = Module()

def get_options():
    return module.options

def show_ui(tkui):
    module.show_ui(tkui)

def update_filenames(files):
    return module.update_filenames(files)