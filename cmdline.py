# Command line tools module

from collections import deque
import inspect


class CommandLineCaller:
    """ A Class that calls functions based on command line arguments """

    moduleName_ = ""
    argFuncs_ = deque()

    def __init__(self, moduleName):
        self.argFuncs_ = deque()
        if (moduleName is None):
            self.moduleName_ = ""
        elif (len(moduleName.split("\\")) > 1):
            self.moduleName_ = moduleName.split("\\")[-1]
        elif (len(moduleName.split("/")) > 1):
            self.moduleName_ = moduleName.split("/")[-1]
        else:
            self.moduleName_ = moduleName

    def getUsageInformation(self):
        usage = "Usage:\n"
        for argFunc in self.argFuncs_:
            (flags, function) = argFunc
            usage += "    " + self.moduleName_ + " ("
            for flag in flags:
                if (flag is not flags[0]):
                    usage += ", "
                usage += flag
            usage += ")"
            (params, varParams, _, defs) = inspect.getargspec(function)
            offset = 0
            if (defs is None):
                offset = len(params)
            else:
                offset = len(params) - len(defs)
            for i, e in list(enumerate(params)):
                if (i - offset >= 0):
                    usage += " [" + e + "=" + str(defs[i - offset]) + "]"
                else:
                    usage += " <" + e + ">"
            if (varParams is None):
                varParams = []
            if (isinstance(varParams, str)):
                varParams = [varParams]
            for e in varParams:
                usage += " [%s=... ]" % e
            usage += "\n"
        return usage

    def createCommandFunction(self, flags, function):
        try:
            flags = flags.split(" ")
        except AttributeError:
            flags = list(flags)
        
        self.argFuncs_.append((flags, function))

    def callFromArgument(self, args):
        if args is None or len(args) == 0:
            return self.getUsageInformation()
        else:
            if (isinstance(args, str)):
                args = args.split(" ")
            for argFunc in self.argFuncs_:
                (flags, function) = argFunc
                if flags.count(args[0]) > 0:
                    if len(args[1:]) == 0:
                        return function()
                    elif len(args[1:]) == 1:
                        return function(args[1])
                    else:
                        return function(*args[1:])
            return self.getUsageInformation()

## Unit tests

# for __init__
assert(CommandLineCaller("C:\\Test_Case_0\\program_name").moduleName_ \
    == "program_name")
assert(CommandLineCaller("/usr/data/Test_Case_0/program_name").moduleName_ \
    == "program_name")
assert(CommandLineCaller("/test_case_1").moduleName_ == "test_case_1")
assert(CommandLineCaller("\\test_case_1").moduleName_ == "test_case_1")
assert(CommandLineCaller("test_case_2").moduleName_ == "test_case_2")
assert(CommandLineCaller("/usr/data/test_case_3/").moduleName_ == "")
assert(CommandLineCaller("").moduleName_ == "")
assert(CommandLineCaller("\\").moduleName_ == "")
assert(CommandLineCaller("/").moduleName_ == "")
assert(CommandLineCaller(None).moduleName_ == "")

# for printUsageInformation and callFromArgument
def testFunction(val1, val2="test", *val3):
    pass
mycaller = CommandLineCaller("testProgram")
mycaller.createCommandFunction("testFunction tstFunc", testFunction)

def testFunction2(val1, val2, *val3):
    if (val1 != "test1"):
        return False
    if (val2 != "test2"):
        return False
    if isinstance(val3, str):
        return 1
    else:
        return len(val3)

mycaller.createCommandFunction(["testFunction2","tstFunc2"], testFunction2)

def testFunction3(val1="test1", val2="test2"):
    pass

mycaller.createCommandFunction("testFunction3", testFunction3)

cmpString = "Usage:\n" + \
"    testProgram (testFunction, tstFunc) <val1> [val2=test] [val3=... ]\n" + \
"    testProgram (testFunction2, tstFunc2) <val1> <val2> [val3=... ]\n" + \
"    testProgram (testFunction3) [val1=test1] [val2=test2]\n"

#assert(mycaller.getUsageInformation() == cmpString)

def checkTypeError(str):
    try:
        mycaller.callFromArgument(str)
        return False
    except TypeError:
        return True

assert(mycaller.callFromArgument("tstFunc test") is None)
assert(mycaller.callFromArgument("tstFunc2 test1 test2") == 0)
assert(mycaller.callFromArgument("testFunction2 test0 test2") == False)
assert(mycaller.callFromArgument("tstFunc2 test1 test2 extra1 extra2") == 2)
assert(mycaller.callFromArgument("tstFunc2 test1 test2 extra1") == 1)
assert(checkTypeError("tstFunc2 test") == True)
assert(checkTypeError("tstFunc test testy testo") == False)
assert(checkTypeError("tstFunc") == True)