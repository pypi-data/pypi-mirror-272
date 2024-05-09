from __future__ import annotations

import cohdl
from cohdl import Bit, Port
from cohdl import std


class CondWithSideEffect:
    def __init__(self, cond, comment):
        self.cond = cond
        self.comment = comment

    def __bool__(self):
        std.comment(self.comment)
        return bool(self.cond)


class test_while_return_06(cohdl.Entity):
    clk = Port.input(Bit)
    reset = Port.input(Bit)

    def architecture(self):
        @std.sequential
        async def proc():
            while CondWithSideEffect(self.reset, "XXXXXXXXX"):
                await cohdl.true
                continue


print(std.VhdlCompiler.to_string(test_while_return_06))
