#!/usr/bin/env python

LABEL = 'Insert'

class Module:
    def __init__(self):
        self.tkui = False
        self.ui = {}
        self.has_validconfig = True
        self.limits = {
            'position': { 'min': 0, 'max': 9999 }
        }
        self.options = {
            'insert': 'The text to insert',
            'position': 'Any integer from {0} to {1}'.format(
                self.limits['position']['min'],
                self.limits['position']['max'],
            ),
            'from': { 'From the Left': 0, 'From the Right': 1 }
        }
        self.config = {
            'insert': '',
            'position': self.limits['position']['min'],
            'from': self.options['from']['From the Left']
        }

    def show_ui(self, tkui):
        self.tkui = tkui
        insert_label = tkui.tkinter.Label(tkui.module_grp, text='Insert:')
        insert_label.grid(column=0, row=0, sticky='e')
        insert_entry = tkui.tkinter.Entry(tkui.module_grp, width=1)
        insert_entry.grid(column=1, row=0, sticky='ew')
        insert_entry.bind('<KeyRelease>', lambda _: self.update_ui({ 'insert': insert_entry.get() }))
        insert_entry.insert(0, self.config['insert'])
        self.ui['find_entry'] = insert_entry

        position_label = tkui.tkinter.Label(tkui.module_grp, text='At position:')
        position_label.grid(column=0, row=1, sticky='e')
        position_var = tkui.tkinter.StringVar()
        position_var.set(self.config['position'])
        position_spinbox = tkui.tkinter.Spinbox(
            tkui.module_grp,
            from_=self.limits['position']['min'],
            to=self.limits['position']['max'],
            textvariable=position_var,
            command=lambda: self.update_ui({ 'position': position_var.get() })
        )
        position_spinbox.grid(column=1, row=1, sticky='ew')
        position_spinbox.bind('<KeyRelease>', lambda _: self.update_ui({ 'position': position_var.get() }))
        self.ui['position_spinbox'] = position_spinbox

        from_options = self.options['from']
        from_var = tkui.tkinter.StringVar()
        from_var.set([key for key, val in from_options.items() if val == self.config['from']][0])
        from_optionmenu = tkui.tkinter.OptionMenu(
            tkui.module_grp,
            from_var,
            *from_options.keys(),
            command=lambda from_: self.update_ui({ 'from': from_options[from_] })
        )
        from_optionmenu.configure(width=15)
        from_optionmenu.grid(column=1, row=2, sticky='ew')

        tkui.module_grp.grid_columnconfigure(1, weight=1)
        self.check_ui()

    def check_spinbox(self, spinbox):
        if spinbox.get().isdigit():
            spinbox.config(bg='white')
            return True
        else:
            spinbox.config(bg='red')
            return False

    def check_ui(self):
        if self.ui['position_spinbox'].get() != self.config['position']:
            self.config['position'] = self.ui['position_spinbox'].get()
        self.has_validconfig = self.validate_config()

    def update_ui(self, setting):
        self.config.update(setting)
        self.has_validconfig = self.validate_config()
        self.tkui.update_newnames()

    def validate_config(self):
        if self.tkui and not self.check_spinbox(self.ui['position_spinbox']):
            return False

        if not str(self.config['position']).isdigit():
            return False
        return True

    def update_filenames(self, files):
        if not self.has_validconfig:
            return files

        newfilenames = []
        insert = self.config['insert']
        position = int(self.config['position'])
        from_ = self.config['from']

        for f in files:
            if position > len(f):
                newfilenames.append(f)

            if from_ == self.options['from']['From the Left']:
                filename = ''.join(
                    f[0:position],
                    insert,
                    f[position:len(f)]
                )
            else:
                filename = ''.join(
                    f[0:len(f)-position],
                    insert,
                    f[len(f)-position:len(f)]
                )
            newfilenames.append(filename)
        return newfilenames

module = Module()

def get_options():
    return module.options

def show_ui(tkui):
    module.show_ui(tkui)

def update_filenames(files):
    return module.update_filenames(files)
