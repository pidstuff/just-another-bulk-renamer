#!/usr/bin/env python

# This script is for automatically testing the functionality of JABR and Files

import datetime
import importlib
import os
import random
import shutil
import sys
import timeit
import unittest

jabr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(jabr_path)

import jabr.main

class Test_Data():
    def __init__(self, num=0, rand=False):
        self.dir = 'sample'
        self.logfile = 'testing.log'
        self.jabr = jabr.main.JABR()
        self.modules = self.get_test_modules()
        self.files = self.get_dir_files(self.dir, num, rand)

    def clear_files(self):
        del self.files[:]
        self.jabr.files.clear()

    def get_dir_files(self, dir='sample', num=0, rand=False):
        files = [os.path.abspath(os.path.join(dir, f)) for f in os.listdir(dir)]
        random.shuffle(files) if rand else files
        files = files[:num] if num > 0 else files

        self.jabr.files.add(files)
        return files

    def get_test_file(self, num, rand=True):
        files = self.files.copy()
        random.shuffle(files) if rand else files
        return files[:num]

    def get_test_modules(self):
        return [f[:-3] for f in os.listdir('modules') if f.endswith('.py')]

    def log(self, unit, log):
        with open(self.logfile, 'a') as testlog:
            testlog.write('LOG:{0}:{1}: {2}\n'.format(datetime.datetime.now(), unit, log))

class JAR_Test(unittest.TestCase):
    def setUp(self):
        files = 8
        random = True
        self.testdata = Test_Data(files, random)

    def tearDown(self):
        self.testdata.clear_files()

    def test_jabr_add(self):
        unit = 'JABR Add'
        self.testdata.log(unit, 'Adding files with duplicates into JABR')
        new_files = self.testdata.get_dir_files(num=5, rand=True)
        self.testdata.files += [f for f in new_files if f not in self.testdata.files]
        new_files += self.testdata.get_test_file(3) # certain duplicates
        self.testdata.jabr.files.add(new_files)

        rand_index = random.randint(0, len(self.testdata.files) - 1)
        fullname = os.path.basename(self.testdata.files[rand_index])
        base, ext = os.path.splitext(fullname)
        dirpath = os.path.dirname(self.testdata.files[rand_index])
        self.testdata.log(unit, 'Comparing file \'{0}\' at index {1}'.format(fullname, rand_index))

        self.assertEqual(len(self.testdata.jabr.files.list), len(self.testdata.files))
        self.assertEqual(self.testdata.jabr.files.list[rand_index]['fullname'], fullname)
        self.assertEqual(self.testdata.jabr.files.list[rand_index]['base'], base)
        self.assertEqual(self.testdata.jabr.files.list[rand_index]['ext'], ext[1:])
        self.assertEqual(self.testdata.jabr.files.list[rand_index]['dirpath'], dirpath)
        self.testdata.log(unit, 'TESTING COMPLETE!')

    def test_jabr_remove(self):
        unit = 'JABR Remove'
        rand_indexes = random.sample(range(0, len(self.testdata.files)), 3)
        self.testdata.log(unit, 'Removing files on indices ({0}, {1}, {2})'.format(rand_indexes[0], rand_indexes[1], rand_indexes[2]))
        removed_files = [f for i, f in enumerate(self.testdata.files) if i in rand_indexes]
        self.testdata.files = [f for f in self.testdata.files if f not in removed_files]
        self.testdata.jabr.files.remove(rand_indexes)
        self.testdata.log(unit, 'Comparing remaining files')
        self.assertEqual(len(self.testdata.jabr.files.list), len(self.testdata.files))
        failed_remove = [f for f in self.testdata.jabr.files.list if f['fullpath'] in removed_files]
        self.assertFalse(failed_remove)
        self.testdata.log(unit, 'TESTING COMPLETE!')

    def test_jabr_clear(self):
        unit = 'JABR Clear'
        self.testdata.log(unit, 'Clearing files on JABR')
        self.testdata.jabr.files.clear()
        self.assertEqual(len(self.testdata.jabr.files.list), 0)
        self.testdata.log(unit, 'TESTING COMPLETE!')

    def test_jabr_rename(self):
        unit = 'JABR Rename'
        self.testdata.log(unit, 'Renaming files on JABR')
        new_filenames = ['{0}.test'.format(os.path.basename(f)) for f in self.testdata.files]
        result = self.testdata.jabr.files.rename(new_filenames)
        self.testdata.log(unit, 'Comparing renamed files with expected results')
        inequal_results = set(result['newoldnames']).difference(set(new_filenames))
        self.assertFalse(inequal_results)
        new_filenames = [f[:-5] for f in new_filenames]
        self.testdata.jabr.files.rename(new_filenames)
        self.testdata.log(unit, 'TESTING COMPLETE!')

    def test_jabr_remove_mods(self):
        unit = 'JABR Remove Mods'
        mods = list(self.testdata.jabr.mods.keys())
        mod = random.choice(mods)
        self.testdata.log(unit, 'Removing \'{0}\' module and checking result'.format(mod))
        self.testdata.jabr.remove_mod(mod)
        self.assertEqual(len(list(self.testdata.jabr.mods.keys())), len(mods)-1)
        self.assertFalse(mod in list(self.testdata.jabr.mods.keys()))
        self.testdata.log(unit, 'TESTING COMPLETE!')

    def test_jabr_add_performance(self):
        unit = 'JABR Add Performance'
        dir = 'jabr_performance'
        number_of_files = 10000
        self.testdata.log(unit, 'Creating {0} files for testing adding performance'.format(number_of_files))
        if not os.path.exists(dir):
            os.mkdir(dir)
        for i in range(0, number_of_files):
            file = '{0}_{1}'.format('performance', i+1)
            if not os.path.exists(file):
                open(os.path.join(dir, file), 'a').close()
        files = self.testdata.get_dir_files(dir)
        start = timeit.default_timer()
        self.testdata.log(unit, 'Adding files')
        self.testdata.jabr.files.add(files)
        end = timeit.default_timer()
        self.testdata.log(unit, 'Operating time in seconds: {0}'.format(end - start))
        shutil.rmtree(dir)
        self.testdata.log(unit, 'TESTING COMPLETE!')
        
if __name__ == '__main__':
    unittest.main()