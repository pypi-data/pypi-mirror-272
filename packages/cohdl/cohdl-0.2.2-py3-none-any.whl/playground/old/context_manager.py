from cohdl import std, Signal, Bit, Entity, true


class Example(Entity):
    def architecture(self):
        addr = Signal[Bit]()

        async def minimal_impl():
            if addr:
                pass
            elif addr:
                await true
                std.comment("impl.done")
            std.comment("impl.end")

        @std.sequential
        async def minimal():
            await minimal_impl()
            std.comment("AFTER impl")
            await true


# print(std.VhdlCompiler.to_ir(Example).dump())

print(std.VhdlCompiler.to_string(Example))
