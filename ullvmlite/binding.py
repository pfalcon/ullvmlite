from ullvm_c import *


def initialize():
    pass


def initialize_native_target():
    # TODO: Fix hardcoding to x86
    LLVMInitializeX86TargetInfo()
    LLVMInitializeX86Target()
    LLVMInitializeX86TargetMC()


def initialize_native_asmprinter():
    # TODO: Fix hardcoding to x86
    LLVMInitializeX86AsmPrinter()
