import unittest

class BrainTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        print(".", end="")
        unittest.TestResult.addSuccess(self, test)
    def addError(self, test, err):
        if err[0].__name__ == "KeyError":
            print("-", end="")
        elif err[0].__name__ == "IOError":
            print(",", end="")
        else:
            print("+", end="")
        unittest.TestResult.addError(self, test, err)
    def addFailure(self, test, err):
        print(">", end="")
        unittest.TestResult.addFailure(self, test, err)
    def addSkip(self, test, reason):
        print("[", end="")
        unittest.TestResult.addSkip(self, test, reason)
    def addExpectedFailure(self, test, err):
        print("]", end="")
        unittest.TestResult.addExpectedFailure(self, test, err)
    def addUnexpectedSuccess(self, test):
        print("<", end="")
        unittest.TestResult.addUnexpectedSuccess(self, test)
    def printErrors(self):
        print()

class BrainTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return BrainTestResult(self.stream, self.descriptions, self.verbosity)

class BrainTestProgram(unittest.TestProgram):
    def __init__(self, *args, **kwargs):
        kwargs["testRunner"] = BrainTestRunner
        kwargs["verbosity"] = 1
        kwargs["module"] = None
        super().__init__(*args, **kwargs)

def main():
    BrainTestProgram()
