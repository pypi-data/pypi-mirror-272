from __future__ import annotations

import cohdl
from cohdl import std


class TopEntity(cohdl.Entity):
    def architecture(self):

        @std.sequential
        async def proc():
            while True:
                break


print(std.VhdlCompiler.to_string(TopEntity))
