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


class Engine:

    def __init__(self, engine):
        self.engine = engine

    def __int__(self):
        return self.engine

    def add_module(self, mod):
        LLVMAddModule(self.engine, mod)

    def get_function_address(self, name):
        return LLVMGetFunctionAddress(self.engine, name)


def create_mcjit_compiler(mod, target_machine):
    print("Warning: create_mcjit_compiler: target_machine is ignored")
    engine_ref = by_ref("P")
    errmsg_ref = by_ref("P")
    res = LLVMCreateMCJITCompilerForModule(engine_ref, mod, 0, 0, errmsg_ref)
    assert not res
    return Engine(engine_ref[0])


class Target:

    @staticmethod
    def from_default_triple():
        # TODO
        return Target()

    def create_target_machine(self):
        # TODO
        pass
