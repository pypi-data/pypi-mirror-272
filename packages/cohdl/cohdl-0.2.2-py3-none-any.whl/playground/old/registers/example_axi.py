from __future__ import annotations

from cohdl import std
from cohdl import Unsigned, BitVector, Bit, Null, Full, Signal, Entity, Port

from cohdl.std import reg
from cohdl.std.axi.axi4_light import Axi4Light

from cohdl.std.reg import reg32


class OrExample(reg32.Register):
    a: reg32.MemField[7:0]
    b: reg32.MemField[15:8]
    c: reg32.MemField[23:16]

    result: reg32.Field[31:24]

    irq_rd: reg32.ReadTick
    irq_wr: reg32.WriteTick

    def _on_read_(self) -> BitVector:
        std.comment("THIS IS AN OrExample")
        self.a = 3
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


class MyAddrRange(reg32.AddrRange, word_count=64):
    def _config_(self):
        self._mem = Signal[BitVector[32]](name="ASDFASDF_RANGE")

    def _on_read_relative_(self, addr: Unsigned):
        return self._mem

    def _on_write_relative_(self, addr: Unsigned, data: BitVector, mask: BitVector):
        self._mem <<= data


class RootDevice(reg32.RootDevice, word_count=1024):
    sub_a: SubDevice[0]
    sub_b: SubDevice[32]

    rgb: RgbReg[64]

    my_range: MyAddrRange[256]

    my_array: reg32.Array[OrExample, 512:576:8]

    def _config_(self, r, g, b):
        self.rgb._config_(r, g, b)


class MyEntity(Entity):
    clk = Port.input(Bit)
    reset = Port.input(Bit)

    r = Port.output(Bit)
    g = Port.output(Bit)
    b = Port.output(Bit)

    def architecture(self):
        clk = std.Clock(self.clk)
        reset = std.Reset(self.reset)

        axi = Axi4Light.signal(clk, reset, 32, 32)

        axi.connect_addr_map(RootDevice(self.r, self.g, self.b))


with open("example.vhdl", "w") as file:
    print(std.VhdlCompiler.to_string(MyEntity), file=file)
