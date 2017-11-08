# this is importing BaseModuleTestCase from 
# the tests/utils/sorting/__init__.py
#from . import BaseSortingTestCase
#
import sys
from FSBA2.utils.sorting import *
#
#import random
import unittest

class ParametrizedTestCase(unittest.TestCase):
    def __init__(self, testName, f=None):
        super(ParametrizedTestCase, self).__init__(testName)
        self.func = f

    def setUp(self):
        super().setUp()
        print(self._testMethodName)

    def tearDown(self):
        print("OK\n")

class SortingTestCase(ParametrizedTestCase):
    def test_EmptyList(self):
        self.assertEqual(self.func([]),[])

    def test_OneElem(self):
        self.assertEqual(self.func([0]), [0])

    def test_ThreeElemASC(self):
        self.assertEqual(self.func([0,1,2]), [0,1,2])

    def test_ThreeElemDESC(self):
        self.assertEqual(self.func([2,1,0]), [0,1,2])


def runTestCasesOnFunctionList(cls, funcList):
    for f in funcList:
        print(f.__name__)
        print("-" * len(f.__name__))
        suite = unittest.TestSuite()
        for testName in (testName for _, testName in SortingTestCase.__dict__.items() if callable(testName) and testName.__name__[:4] == "test"):
            suite.addTest(cls(testName.__name__, f=f))
        unittest.TextTestRunner().run(suite)
        print()

#unittest.TextTestRunner(verbosity=2).run(suite)
runTestCasesOnFunctionList(SortingTestCase, [qsort, msort, insertionsort, selectionsort, bubblesort])



