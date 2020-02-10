#!/usr/bin/env python

LABEL = 'Numbering'

class Module:
    def __init__(self):
        self.tkui = False
        self.ui = {}
        self.has_validconfig = True
        self.limits = {
            'leading zeros': { 'min': 0, 'max': 10 },
            'start': { 'min': 1 }
        }
        self.options = {
            'leading zeros': 'Any integer from {0} to {1}'.format(
                self.limits['leading zeros']['min'],
                self.limits['leading zeros']['max']
            ),
            'start': 'A positive integer',
            'format': {
                'OldName Text Number': 0,
                'Number Text OldName': 1,
                'Text Number': 2,
                'Number Text': 3
            },
            'text': 'Text which serves as the label for the file'
        }
        self.config = {
            'leading zeros': self.limits['leading zeros']['min'],
            'start': 1,
            'format': self.options['format']['OldName Text Number'],
            'text': ''
        }

    def show_ui(self, tkui):
        module.tkui = tkui
        leading_zeros_label = tkui.tkinter.Label(tkui.module_grp, text='Leading Zeros:')
        leading_zeros_label.grid(column=0, row=0, sticky='e')
        leading_zeros_var = tkui.tkinter.StringVar()
        leading_zeros_var.set(self.config['leading zeros'])
        leading_zeros_spinbox = tkui.tkinter.Spinbox(
            tkui.module_grp,
            from_=self.limits['leading zeros']['min'],
            to=self.limits['leading zeros']['max'],
            textvariable=leading_zeros_var,
            command=lambda: self.update_ui({ 'leading zeros': leading_zeros_var.get() })
        )
        leading_zeros_spinbox.grid(column=1, row=0, sticky='w')
        leading_zeros_spinbox.bind('<KeyRelease>', lambda _: self.update_ui({ 'leading zeros': leading_zeros_var.get() }))
        self.ui['leading_zeros_spinbox'] = leading_zeros_spinbox

        start_label = tkui.tkinter.Label(tkui.module_grp, text='Start with:')
        start_label.grid(column=2, row=0, sticky='e')
        start_entry = tkui.tkinter.Entry(tkui.module_grp, width=1)
        start_entry.grid(column=3, row=0, sticky='ew')
        start_entry.bind('<KeyRelease>', lambda _: self.update_ui({ 'start': start_entry.get() }))
        start_entry.insert(0, self.config['start'])
        self.ui['start'] = start_entry

        format_label = tkui.tkinter.Label(tkui.module_grp, text='Format:')
        format_label.grid(column=0, row=1, sticky='e')
        format_options = self.options['format']
        format_var = tkui.tkinter.StringVar()
        format_var.set([key for key, val in format_options.items() if val == self.config['format']][0])
        format_optionmenu = tkui.tkinter.OptionMenu(
            tkui.module_grp,
            format_var,
            *format_options.keys(),
            command=lambda format: self.update_ui({ 'format': format_options[format] })
        )
        format_optionmenu.configure(width=20)
        format_optionmenu.grid(column=1, row=1, sticky='w')

        text_label = tkui.tkinter.Label(tkui.module_grp, text='Text:')
        text_label.grid(column=2, row=1, sticky='e')
        text_entry = tkui.tkinter.Entry(tkui.module_grp, width=1)
        text_entry.grid(column=3, row=1, sticky='ew')
        text_entry.bind('<KeyRelease>', lambda _: self.update_ui({ 'text': text_entry.get() }))
        text_entry.insert(0, self.config['text'])

        tkui.module_grp.grid_columnconfigure(3, weight=1)
        self.check_ui()

    def check_numeric_ui(self, ui):
        if ui.get().isdigit():
            ui.config(bg='white')
            return True
        else:
            ui.config(bg='red')
            return False

    def check_ui(self):
        if self.ui['leading_zeros_spinbox'].get() != self.config['leading zeros']:
            self.config['leading zeros'] = self.ui['leading_zeros_spinbox'].get()
        self.has_validconfig = self.validate_config()

    def update_ui(self, setting):
        self.config.update(setting)
        self.has_validconfig = self.validate_config()
        self.tkui.update_newnames()

    def validate_config(self):
        if self.tkui:
            is_leading_zeros_valid = self.check_numeric_ui(self.ui['leading_zeros_spinbox'])
            is_start_valid = self.check_numeric_ui(self.ui['start'])
            if not is_leading_zeros_valid or not is_start_valid:
                return False

        leading_zeros = self.config['leading zeros']
        start = self.config['start']
        if not str(start).isdigit() or not str(leading_zeros).isdigit():
            return False

        leading_zeros = int(leading_zeros)
        start = int(start)
        if leading_zeros < self.limits['leading zeros']['min'] or leading_zeros > self.limits['leading zeros']['max']:
            return False
        if start < self.limits['start']['min']:
            return False
        return True

    def update_filenames(self, files):
        if not self.has_validconfig:
            return files

        leading_zeros = int(self.config['leading zeros']) + 1
        start = int(self.config['start'])
        format = self.config['format']
        text = self.config['text']
        if format == self.options['format']['OldName Text Number']:
            return [''.join([f, text, '%0{0}d'.format(leading_zeros) % (start + i)]) for i, f in enumerate(files)]
        elif format == self.options['format']['Number Text OldName']:
            return [''.join(['%0{0}d'.format(leading_zeros) % (start + i), text, f]) for i, f in enumerate(files)]
        elif format == self.options['format']['Text Number']:
            return [''.join([text, '%0{0}d'.format(leading_zeros) % (start + i)]) for i, f in enumerate(files)]
        return [''.join(['%0{0}d'.format(leading_zeros) % (start + i), text]) for i, f in enumerate(files)]

module = Module()

def get_options():
    return module.options

def show_ui(tkui):
    module.show_ui(tkui)

def update_filenames(files):
    return module.update_filenames(files)