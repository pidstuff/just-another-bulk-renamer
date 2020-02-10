#!/usr/bin/env python

import datetime
import importlib
import os
import sys

from jabr.tkui import TkUI

class Files:
    def __init__(self):
        self.list = []
        self._existingfiles = set()

    def __str__(self):
        if not len(self.list):
            return 'There are no files to print'
        strformat = 'File no. {0}\nFile:\t{1}\nPath:\t{2}\n'
        output = ''
        for i, l in enumerate(self.list):
            output = '\n'.join([output, strformat.format(i+1, l['fullname'], l['dirpath'])])
        return output

    def add(self, files):
        """ Adds the non-duplicate files into self.list & self._existingfiles
            then returns the files that were added
        """
        files = [f for f in files if f not in self._existingfiles]
        for f in files:
            fullname = os.path.basename(f)
            base, ext = os.path.splitext(fullname)
            self._existingfiles.add(f)
            self.list.append({
                'fullname': fullname,
                'base': base,
                'ext': ext[1:],
                'fullpath': f,
                'dirpath': os.path.dirname(f)
            })
        return tuple(files)

    def remove(self, files):
        files.sort()
        for f in reversed(files):
            self._existingfiles.discard(self.list[f]['fullpath'])
            del self.list[f]

    def clear(self):
        del self.list[:]
        self._existingfiles.clear()

    def rename(self, newnames):
        """ Renames the files and updates self.list if there are no conflicts
            then returns the updated filenames and errors if any
        """
        output = {
            'newoldnames': [],
            'errormsg': '',
            'errorlog': ''
        }

        dirpaths = set()
        newnamesfullpaths = []
        for i, li in enumerate(self.list):
            dirpaths.add(li['dirpath'])
            newnamesfullpaths.append(os.path.join(li['dirpath'], newnames[i]))

        existingfullpaths = set()
        for dp in dirpaths:
            for ld in os.listdir(dp):
                existingfullpaths.add(os.path.join(dp, ld))
        nameconflicts = set(newnamesfullpaths).intersection(existingfullpaths)

        failedrenames = []
        for i, n in enumerate(newnames):
            if bool(nameconflicts):
                output['errormsg'] = 'Conflicts found. No file has been renamed.'
                output['errorlog'] = 'List of files in conflict:\n'
                output['errorlog'] = '\n'.join(str(nc) for nc in nameconflicts)
                break
            if not n:
                output['newoldnames'].append(self.list[i]['fullname'])
                continue
            try:
                os.rename(self.list[i]['fullpath'], newnamesfullpaths[i])
            except OSError as e:
                output['errormsg'] = 'Error/s found. Check error.log for info.'
                output['errorlog'] += '{0}: {1}\n'.format(str(e), self.list[i]['fullpath'])
                output['newoldnames'].append(self.list[i]['fullname'])
                continue
            output['newoldnames'].append(newnames[i])
            base, ext = os.path.splitext(n)
            self.list[i]['fullname'] = n
            self.list[i]['base'] = base
            self.list[i]['ext'] = ext[1:]
            self.list[i]['fullpath'] = os.path.join(self.list[i]['dirpath'], n)
        output['newoldnames'] = tuple(output['newoldnames'])
        return output

class JABR:
    def __init__(self):
        self.name = 'Just Another Bulk Renamer'
        self.version = 1.0
        self.workdir = self._get_workdir()
        self.files = Files()
        self.mods = {}

        self._load_mods(self._get_modsdir('modules'))

    def _get_dirpath(self, path):
        path = os.path.realpath(path)
        return path.replace('\\', '/')

    def _get_modsdir(self, directory):
        modsdir = os.path.join(self.workdir, directory)
        if not os.path.exists(modsdir):
            os.mkdir(modsdir)
        return self._get_dirpath(modsdir)

    def _get_workdir(self):
        isfrozen = getattr(sys, 'frozen', False)
        workdir = __file__ if not isfrozen else sys.executable
        return os.path.dirname(workdir)

    def _load_mods(self, directory):
        sys.path.append(directory)
        modlist = os.listdir(directory)
        for m in modlist:
            if not m.endswith(('.py', '.pyc')):
                continue
            mod = os.path.splitext(m)[0]
            importedmod = importlib.import_module(mod)
            if all(hasattr(importedmod, attr) for attr in ('LABEL', 'get_options', 'update_filenames')):
                self.mods[importedmod.LABEL] = { 'object': importedmod }

    def logerror(self, log=''):
        with open('error.log', 'a') as errorlog:
            errorlog.write(
                '{0} (Python {1}.{2}) {3}:\n{4}\n\n'.format(
                    self.name,
                    sys.version_info[0],
                    sys.version_info[1],
                    datetime.datetime.now(),
                    log
                )
            )

    def remove_mod(self, mod):
        del self.mods[mod]

def start():
    jabr = JABR()
    tkui = TkUI(None, jabr)
    tkui.title(jabr.name)
    tkui.minsize(480, 400)
    tkui.mainloop()
