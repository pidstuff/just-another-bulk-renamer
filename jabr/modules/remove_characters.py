#!/usr/bin/env python

LABEL = 'Remove Characters'

class Module:
    def __init__(self):
        self.tkui = False
        self.ui = {}
        self.has_validconfig = True
        self.limits = {
            'start': { 'min': 0, 'max': 9999 },
            'end': { 'min': 0, 'max': 9999 }
        }
        self.options = {
            'start': 'Any integer from {0} to {1}'.format(
                self.limits['start']['min'],
                self.limits['start']['max']
            ),
            'end': 'Any integer from {0} to {1}'.format(
                self.limits['end']['min'],
                self.limits['end']['max']
            ),
            'from': { 'From the Left': 0, 'From the Right': 1 }
        }
        self.config = {
            'start': self.limits['start']['min'],
            'end': self.limits['end']['min'],
            'from': self.options['from']['From the Left']
        }

    def show_ui(self, tkui):
        module.tkui = tkui
        start_label = tkui.tkinter.Label(tkui.module_grp, text='Start From:')
        start_label.grid(column=0, row=0, sticky='e')
        start_var = tkui.tkinter.StringVar()
        start_var.set(self.config['start'])
        start_spinbox = tkui.tkinter.Spinbox(
            tkui.module_grp,
            from_=self.limits['start']['min'],
            to=self.limits['start']['max'],
            textvariable=start_var,
            command=lambda: self.update_ui({ 'start': start_var.get() })
        )
        start_spinbox.grid(column=1, row=0, sticky='ew')
        start_spinbox.bind('<KeyRelease>', lambda _: self.update_ui({ 'start': start_var.get() }))
        self.ui['start_spinbox'] = start_spinbox

        end_label = tkui.tkinter.Label(tkui.module_grp, text='To:')
        end_label.grid(column=0, row=1, sticky='e')
        end_var = tkui.tkinter.StringVar()
        end_var.set(self.config['end'])
        end_spinbox = tkui.tkinter.Spinbox(
            tkui.module_grp,
            from_=self.limits['end']['min'],
            to=self.limits['end']['max'],
            textvariable=end_var,
            command=lambda: self.update_ui({ 'end': end_var.get() })
        )
        end_spinbox.grid(column=1, row=1, sticky='ew')
        end_spinbox.bind('<KeyRelease>', lambda _: self.update_ui({ 'end': end_var.get() }))
        self.ui['end_spinbox'] = end_spinbox

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
        if self.ui['start_spinbox'].get() != self.config['start']:
            self.config['start'] = self.ui['start_spinbox'].get()
        if self.ui['end_spinbox'].get() != self.config['end']:
            self.config['end'] = self.ui['end_spinbox'].get()
        self.has_validconfig = self.validate_config()

    def update_ui(self, setting):
        self.config.update(setting)
        self.has_validconfig = self.validate_config()
        self.tkui.update_newnames()

    def validate_config(self):
        if self.tkui:
            is_startvalid = self.check_spinbox(self.ui['start_spinbox'])
            is_endvalid = self.check_spinbox(self.ui['end_spinbox'])
            if not is_startvalid or not is_endvalid:
                return False

        start = self.config['start']
        end = self.config['end']
        if not str(start).isdigit() or not str(end).isdigit():
            return False

        start = int(start)
        end = int(end)
        if start < self.limits['start']['min'] or start > self.limits['start']['max']:
            return False
        if end < self.limits['end']['min'] or end > self.limits['end']['max']:
            return False
        if start >= end:
            return False
        return True

    def update_filenames(self, files):
        if not self.has_validconfig:
            return files

        newfilenames = []
        start = int(self.config['start'])
        end = int(self.config['end'])
        from_ = self.config['from']
        if from_ == self.options['from']['From the Left']:
            return [f[:start] + f[end:] for f in files]

        for f in files:
            start = -(len(f)) if (start == 0) else start
            newfilenames.append(f[:-(end)] + f[-(start):])
        return newfilenames

module = Module()

def get_options():
    return module.options

def show_ui(tkui):
    module.show_ui(tkui)

def update_filenames(files):
    return module.update_filenames(files)