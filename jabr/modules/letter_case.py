#!/usr/bin/env python

LABEL = 'Letter Case'

class Module:
    def __init__(self):
        self.tkui = False
        self.options = { 'case': { 'Capitalization': 0, 'lower case': 1, 'UPPER CASE': 2 } }
        self.config = { 'case': self.options['case']['Capitalization'] }

    def show_ui(self, tkui):
        self.tkui = tkui
        case_options = self.options['case']
        case_label = tkui.tkinter.Label(tkui.module_grp, text='Case:')
        case_label.grid(column=0, row=0, sticky='e')
        case_var = tkui.tkinter.StringVar()
        case_var.set([key for key, val in case_options.items() if val == self.config['case']][0])
        case_optionmenu = tkui.tkinter.OptionMenu(
            tkui.module_grp,
            case_var,
            *case_options.keys(),
            command=self.update_ui
        )
        case_optionmenu.config(width=15)
        case_optionmenu.grid(column=1, row=0, sticky='w')

    def update_ui(self, case):
        self.config.update({ 'case': self.options['case'][case] })
        self.tkui.update_newnames()

    def update_filenames(self, files):
        case = self.config['case']
        case_options = self.options['case']
        if case == case_options['Capitalization']:
            return [f.title() for f in files]
        elif case == case_options['lower case']:
            return [f.lower() for f in files]
        else:
            return [f.upper() for f in files]

module = Module()

def get_options():
    return module.options

def show_ui(tkui):
    module.show_ui(tkui)

def update_filenames(files):
    return module.update_filenames(files)