# Command line tools module

from collections import deque
import inspect

def printUsageHeader():
    print("Usage: <arg> means required argument, " + \
        "[arg] means optional argument\n")

class CommandLineError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class CommandLineFunction:
    """ A Class that holds function information for a command line function """
    
    def no_func(): print("There is no function assigned to this command.")

    flags = []
    func = no_func
    args = None
    varargs = None
    keywords = None
    defaults = None
    description = ""

    def __init__(self, flags, function, description=None):
        try:
            flags = flags.split(" ")
        except (AttributeError, TypeError):
            try:
                flags = list(flags)
            except (AttributeError, TypeError):
                raise CommandLineError("Cannot create list from argument " + \
                    "'flags'.")
        self.flags = flags

        self.func = function;

        arglist = inspect.getargspec(self.func)
        arglist = list(arglist)
        for i in range(len(arglist)):
            if arglist[i] is None: arglist[i] = []
            elif isinstance(arglist[i], str): arglist[i] = [arglist[i]]
        (self.args, self.varargs, self.keywords, self.defaults) = tuple(arglist)
        self.description = description

    def printUsage(self):
        print("Command: " + self.flags[0])
        print("    Aliases:   ", end="")
        for flag in self.flags:
            print(flag, end=" ")
        print("")
        print("    Arguments: ", end="")
        if self.description is not None: print(self.description)
        offset = len(self.args) - len(self.defaults)
        for i in range(len(self.args)):
            if i < offset:
                print("<" + self.args[i] + ">", end=" ")
            else:
                deft = self.defaults[i - offset]
                print("[" + self.args[i] + "=\"" + str(deft) + "\"]", end=" ")
        for vararg in self.varargs: print("[" + vararg + "=*]", end=" ")
        for keyword in self.keywords: print("[" + keyword + "=**]", end=" ")
        print("")

    def callFromArgument(self, args):
        if args is None: args = ""
        if (isinstance(args, str)):
            args = args.split(" ")
        if len(args) < len(self.args) - len(self.defaults):
            raise CommandLineError( \
                "Insufficient number of arguments provided.")
        else:
            if len(args) == 0: return self.func()
            elif len(args) == 1: return self.func(args[0])
            else: return self.func(*args)

    def hasFlag(self, flag):
        return self.flags.count(flag) > 0






class CommandLineCaller:
    """ A Class that calls functions based on command line arguments """

    moduleName_ = ""
    commands_ = deque()

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

    def printUsage(self):
        printUsageHeader()
        for command in self.commands_:
            command.printUsage()
            print("")

    def createCommandFunction(self, flags, function):
        self.commands_.append(CommandLineFunction(flags, function))

    def callFromArgument(self, args):
        if args is None: args = ""
        if (isinstance(args, str)):
            args = args.split(" ")
        try:
            name = args.pop(0)
            for command in self.commands_:
                if command.hasFlag(name): return command.callFromArgument(args)
        except IndexError:
            self.printUsage()


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

def checkError(str):
    try:
        mycaller.callFromArgument(str)
        return False
    except CommandLineError:
        return True

assert(mycaller.callFromArgument("tstFunc test") is None)
assert(mycaller.callFromArgument("tstFunc2 test1 test2") == 0)
assert(mycaller.callFromArgument("testFunction2 test0 test2") == False)
assert(mycaller.callFromArgument("tstFunc2 test1 test2 extra1 extra2") == 2)
assert(mycaller.callFromArgument("tstFunc2 test1 test2 extra1") == 1)
assert(checkError("tstFunc2 tst"))
assert(checkError("tstFunc2"))
assert(not checkError("tstFunc2 tst tst"))

mycaller = None