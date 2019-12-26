# ullvmlite - Reimplemetation of llvmlite module
# (https://github.com/numba/llvmlite) on top of ullvm_c module
# (https://github.com/pfalcon/ullvm_c).
#
# https://github.com/pfalcon/ullvmlite
#
# This project is a conceptual part of the Pycopy project, minimalist
# and lightweight Python ecosystem.
#
# https://github.com/pfalcon/pycopy
# https://github.com/pfalcon/pycopy-lib
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from ullvm_c import *


VoidType = LLVMVoidType
IntType = LLVMIntType
FloatType = LLVMFloatType
DoubleType = LLVMDoubleType
FunctionType = LLVMFunctionType

def PointerType(tp, addrspace=0):
    return LLVMPointerType(tp, addrspace)


class Module:

    def __init__(self, name):
        self.mod = LLVMModuleCreateWithName(name)

    def __int__(self):
        return self.mod

    def verify(self):
        assert LLVMVerifyModule(self.mod, LLVMReturnStatusAction, None) == 0


class Value:

    def __init__(self, v):
        self.v = v

    def __int__(self):
        return self.v

    @property
    def type(self):
        return LLVMTypeOf(self.v)

    @property
    def name(self):
        return LLVMGetValueName(self.v)


class Constant(Value):

    def __init__(self, typ, v):
        if isinstance(v, int):
            self.v = LLVMConstInt(typ, v, True)
        else:
            raise NotImplementedError


class Function(Value):

    def __init__(self, mod, func_typ, name):
        self.v = LLVMAddFunction(mod, name, func_typ)

    def append_basic_block(self, label):
        return LLVMAppendBasicBlock(self.v, label)

    @property
    def args(self):
        args = []
        for i in range(LLVMCountParams(self.v)):
            args.append(LLVMGetParam(self.v, i))
        return args


class IRBuilder:

    def __init__(self, bblock):
        self.bld = LLVMCreateBuilder()
        LLVMPositionBuilderAtEnd(self.bld, bblock);

    def position_at_end(self, bblock):
        LLVMPositionBuilderAtEnd(self.bld, bblock);

    def alloca(self, typ, name=""):
        return LLVMBuildAlloca(self.bld, typ, name)

    def load(self, ptr, name=""):
        return Value(LLVMBuildLoad(self.bld, ptr, name))

    def store(self, val, ptr):
        return LLVMBuildStore(self.bld, val, ptr)

    def add(self, v1, v2, name=""):
        return Value(LLVMBuildAdd(self.bld, v1, v2, name))

    def ret(self, val):
        return LLVMBuildRet(self.bld, val)

    def branch(self, label):
        return LLVMBuildBr(self.bld, label)
