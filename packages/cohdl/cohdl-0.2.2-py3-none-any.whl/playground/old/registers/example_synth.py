from __future__ import annotations

from cohdl import std
from cohdl import Unsigned, BitVector, Bit, Null, Full, Signal, Entity, Port

from cohdl.std import new_reg

reg32 = new_reg.RegisterTools[32]


class OrExample(reg32.Register):
    a: reg32.MemField[7:0]
    b: reg32.MemField[15:8]
    c: reg32.MemField[23:16]

    result: reg32.Field[31:24]

    def _on_read_(self) -> BitVector:
        return self(a=Null, b=Full)

    def _impl_concurrent_(self):
        self.result <<= self.a.value() | self.b.value() & self.c.value()


class FlagExample(reg32.Register):
    """
    a flag example register
    """

    a: reg32.MemField[7:0]
    b: reg32.MemField[15:8]

    flag: reg32.FlagField[20]

    result: reg32.Field[31:24]

    async def _impl_sequential_(self):
        await std.wait_for(100)
        self.flag.clear()

    def _impl_concurrent_(self):
        self.result <<= self.a.value() | self.b.value()


class SubDevice(reg32.RegisterDevice, word_count=8):
    reg_1: OrExample[0]
    reg_2: OrExample[4]
    reg_3: FlagExample[8]
    reg_4: FlagExample[12]


class RgbReg(reg32.Register):
    """
    rgb fhgjfhg
    """

    r: reg32.MemUField[7:0]
    g: reg32.MemUField[15:8]
    b: reg32.MemUField[23:16]
    cnt: reg32.UField[31:24]

    def _config_(self, r, g, b):
        self.sig_r = r
        self.sig_g = g
        self.sig_b = b
        self.counter = Signal[Unsigned[8]](0)

    async def _impl_sequential_(self):
        await std.wait_for(1000)
        self.counter <<= self.counter + 1
        self.sig_r <<= self.counter < self.r.value()
        self.sig_g <<= self.counter < self.g.value()
        self.sig_b <<= self.counter < self.b.value()
        self.cnt <<= self.counter


class RootDevice(reg32.RootDevice, word_count=64):
    sub_a: SubDevice[0]
    sub_b: SubDevice[32]

    rgb: RgbReg[64]

    def _config_(self, r, g, b):
        self.rgb._config_(r, g, b)


class MyEntity(Entity):
    clk = Port.input(Bit)

    rd_addr = Port.input(Unsigned[32])
    rd_data = Port.output(BitVector[32])
    rd_done = Port.output(Bit, default=False)

    wr_addr = Port.input(Unsigned[32])
    wr_data = Port.output(BitVector[32])

    r = Port.output(Bit)
    g = Port.output(Bit)
    b = Port.output(Bit)

    def architecture(self):
        clk = std.Clock(self.clk)
        ctx = std.SequentialContext(clk)

        root = RootDevice(self.r, self.g, self.b)

        root._print_()

        regs = root._flatten_()

        for reg in regs:
            if hasattr(reg, "_impl_"):
                reg._impl_(ctx)

        for reg in regs:
            if hasattr(reg, "_impl_sequential_"):

                @std.sequential(clk)
                async def proc_impl_sequential(reg_inst=reg):
                    await std.as_awaitable(reg_inst._impl_sequential_)

        for reg in regs:
            if hasattr(reg, "_impl_concurrent_"):

                @std.concurrent
                def logic():
                    reg._impl_concurrent_()

        @std.sequential(clk)
        async def proc_read():
            for reg in regs:
                if (
                    reg._global_offset_
                    <= self.rd_addr
                    < reg._global_offset_ + reg._unit_count_()
                ):
                    self.rd_data <<= await reg._basic_read_(self.rd_addr, None)
                    break
            self.rd_done ^= True

        @std.sequential(clk)
        async def proc_write():
            for reg in regs:
                if (
                    reg._global_offset_
                    <= self.rd_addr
                    < reg._global_offset_ + reg._unit_count_()
                ):
                    await reg._basic_write_(
                        self.wr_addr, self.wr_data, std.Mask(Full), None
                    )
                    break


with open("example.vhdl", "w") as file:
    print(std.VhdlCompiler.to_string(MyEntity), file=file)
