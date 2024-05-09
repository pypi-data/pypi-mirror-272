from __future__ import annotations

from cohdl import std
from cohdl import Unsigned, BitVector, Null, Full, Signal

from cohdl.std import new_reg, bitfield

from typing import Annotated

reg32 = new_reg.RegisterTools[32]

inp_sig = Signal[BitVector[32]]()
out_sig = Signal[BitVector[32]]()

class MyRegister(reg32.Register):
    a: reg32.Field[7:0]
    b: reg32.Field[11]

raw = Signal[BitVector[32]](Null)

m = MyRegister(raw)

print(m.a)
print(m.a._value)
v = m(a=Full)
print(v.a)
print(v.a._value)


class OrExample(reg32.Register):
    a: reg32.MemField[7:0]
    b: reg32.MemField[15:8]
    c: reg32.MemField[23:16]

    result: reg32.Field[31:24]

    def _impl_concurrent_(self):
        self.result <<= self.a.val | self.b.val & self.c.val


class FlagExample(reg32.Register):
    value: reg32.MemField[15:0]
    result: reg32.Field[24:16]
    flag: reg32.FlagField[31]

    async def _impl_sequential_(self):
        async with self.flag:
            counter = Signal[Unsigned[16]](self.value.val)

            while counter:
                counter <<= counter - 1
            
            self.result <<= Unsigned[8](34)


if False:
    class MyWtcRegister(reg32.Register):
        a: reg32.Field[7:0]

        def _config_(self):
            self.counter = Signal[Unsigned[8]]()
            self.clear_bits = Signal[BitVector[7:0]]
            self.bits = Signal[BitVector[7:0]]()

            self.bits_inp = Signal[BitVector[7:0]]()
            self.bits_storage = Signal[BitVector[7:0]]()
            self.bits_clear = Signal[BitVector[7:0]](Null)
        
        def _on_write_(self, inp: MyWtcRegister):
            self.bits_clear ^= inp.a
            return inp

        def _on_read_(self):
            return self(
                a=self.bits_storage
            )

        def _impl_sequential_(self):
            self.bits_storage <<= (self.bits_storage & ~self.bits_clear) | self.bits_inp


            self.counter <<= self.counter + 1

            if self.counter == 0:
                self.bits <<= Full
            else:
                self.bits <<= self.bits & ~self.clear_bits
            
            if self.counter == 0:
                self.a.out <<= Full
            else:
                self.a.out <<= self.a.out & self.a.inp

    class MyRtcRegister(reg32.Register):


        b: reg32.Field[15:8]
        ma: reg32.MemField[7:0]
        f: reg32.Flag[11]

        # 

        # field without memory
        c: reg32.RoField[23:16]

        # 
        d: reg32.WoField[31:24]



        def _config_(self):
            self.counter = Signal[Unsigned[8]]()
            self.clear_bits = Signal[BitVector[7:0]]
            self.bits = Signal[BitVector[7:0]]()

            self.bits_inp = Signal[BitVector[7:0]]()
            self.bits_storage = Signal[BitVector[7:0]]()
            self.bits_clear = Signal[BitVector[7:0]](Null)
        
        # all mem fields are updated with returned fields
        # flag field is set if returnd bit is 1
        def _on_write_(self, inp: MyWtcRegister):
            self.bits_inp ^= inp.a

            # this is equivalent to a MemField
            self.b <<= inp.b

            return inp
        
        # return value passed to axi master
        # no other effects
        def _on_read_(self):
            self.bits_clear ^= Full
            return self
        
        def _impl_concurrent_(self):
            self.a <<= self.bits_storage

        def _impl_sequential_(self):
            self.bits_storage <<= (self.bits_storage & ~self.bits_clear) | self.bits_inp


            self.counter <<= self.counter + 1

            if self.counter == 0:
                self.bits <<= Full
            else:
                self.bits <<= self.bits & ~self.clear_bits
            
            if self.counter == 0:
                self.a.out <<= Full
            else:
                self.a.out <<= self.a.out & self.a.inp

    class MyRegister(reg32.Register):
        a: reg32.Field[0]
        b: reg32.Field[1]
        c: reg32.Field[2]
        d: reg32.Field[3]

        # reads as zero for master
        wo_x: reg32.WoField[7]

        # writes are ignored by slave
        ro_x: reg32.RoField[7]

        # read value is distinct from write value
        mixed_x: reg32.SpecialField[7]
        pushed_x: reg32.PushedField[7]

        # replaced with std.SyncFlag
        flag_x: reg32.Flag[7]

        def _handle_write_x(self, new_val): ...

        def _config_(self):
            self._raw = Signal[BitVector[32]]()
            self.mixed_x._set_handler_()

            self.wo_x._set_write_handler_()

        def _on_read_(self) -> BitVector:
            return self._raw

        def _on_write_(self, data, mask: std.Mask):
            data = MyRegister(mask.apply(self._raw, data))

        def _impl_concurrent_(self):
            self.storage <<= self.mixed_x.input()
            self.mixed_x <<= self.storage
            self.pushed_x <<= self._flag.is_set()

        def _impl_sequential_wtc_(self):
            
            
            ...

        async def _impl_sequential_(self):
            async with self.flag_x:
                """
                do something
                """



class MyAdder(reg32.RegisterDevice, word_count=4):
    inp_a: reg32.RW[0]
    inp_b: reg32.RW[4]
    out: reg32.RW[8]
    # ctrl: MyRegister[12]

    def _impl_concurrent_(self) -> None:
        self.out <<= self.inp_a._raw_().unsigned + self.inp_b._raw_().unsigned
        self.ctrl


class MySub(reg32.RegisterDevice, word_count=8):
    a: reg32.Input[0]
    b: reg32.Input[4]
    c: reg32.Output[8]
    d: MyAdder[12]

    def _config_(self, cnt):
        self.a._config_(inp_sig)
        self.b._config_(inp_sig)
        self.c._config_(inp_sig)

    def _impl_(self, ctx: std.SequentialContext) -> None:
        return super()._impl_(ctx)


class MyRoot(reg32.RootDevice, word_count=64):
    class MySub2(reg32.RegisterDevice, word_count=8):
        a: reg32.Input[0]
        b: reg32.Input[4]
        c: reg32.Input[8]

        def _config_(self, cnt):
            self.a._config_(inp_sig)
            self.b._config_(inp_sig)
            self.c._config_(inp_sig)

    input: reg32.Input[0]
    output: reg32.Output[4]
    sub: MySub[16]
    sub2: MySub2[48]

    def _config_(self):
        self.input._config_(inp_sig)
        self.output._config_(out_sig)
        self.sub._config_(1)
        self.sub2._config_(2)


my_root = MyRoot()

for entry in my_root._flatten_():
    print(entry)

print()

my_root._print_()

exit()


class Adder(reg.RegisterDevice):
    """
    Example register with two input registers, that
    are added together and returned in a result register
    """

    inp_a: reg.RW[0x00, "first summand"]
    inp_b: reg.RW[0x04, "second summand"]
    result: reg.R[0x08, "result of inp_a+inp_b"]

    def _impl_concurrent_(self):
        self.result <<= self.inp_a + self.inp_b


class Example(reg.RegisterDevice):
    my_reg: reg.AddrRange[0x100:0x104]

    my_adder: Adder[0x80]

    my_array: reg.Array[Adder, 0x200:0x400:0x20]
    my_array: reg.Array[Adder, 0x200:0x400:0x20]

    def __init__(self, parent):
        super().__init__(parent)

        self.my_reg = reg.RegisterRange()
        self.my_array = reg.Array([Adder() for _ in range(16)])


class ExampleReg(reg.Register):
    a: reg.Field[0]
    b: reg.Field[10:3]

    c: reg.Field[20:18, reg.ExampleEnum]

    def on_write(self, data: BitVector, mask: BitVector):
        inp = ExampleReg(data)
        self.a <<= inp.a

    def _impl_sequential_(self):
        if self.a.val():
            self.b <<= self.b.val().unsigned + 1
        else:
            self.b <<= self.b.val().unsigned - 1


my_collection = reg.collection(
    {
        0x0010: Adder(),
        0x0100: Adder(),
        0x0200: Adder(),
        0x0300: Example(),
        0x0400: ExampleReg(),
    }
)

#
#
#
#


#
#
#
#
#


class WaitRegister(reg.GenericRegister):
    async def on_write(self, data: Unsigned, mask=Full):
        await std.wait_for(data.unsigned)


class RgbLed(reg.Register):
    "This register device controls the rgb leds"

    r: reg.FieldU[7:0]
    g: reg.FieldU[15:8]
    b: reg.FieldU[23:16]

    async def _impl_sequential_(self):
        await std.wait_for(std.us(5))
        self.cnt <<= self.cnt + 1
        self.rgb.red <<= self.cnt < self.r.val
        self.rgb.green <<= self.cnt < self.g.val
        self.rgb.blue <<= self.cnt < self.b.val

    def __init__(self, rgb):
        self.rgb = rgb
        self.cnt = Signal[Unsigned[8]](Null)


class SpiCtrlRegister(reg.Register):
    "This register controls the spi communication"

    count: reg.Field[5:2, 0]["asdf"]
    active: reg.Field[8]["set to '1' while a spi transaction is in progress"]

    def __init__(self):
        self.transaction_active = std.SyncFlag()

    def _impl_concurrent_(self):
        self.active <<= self.transaction_active.is_set()

    def on_write(self, data, mask=Full):
        view = self._data_view_(data, mask)

        if view.active:
            assert not self.transaction_active.is_set()
            self.transaction_active.set()

        self.count <<= view.count


class MyOtherReg(reg.RegisterDevice):
    def __init__(self):
        self.a = reg.Register(Signal[BitVector[32]], offset=0x10)

        self._interface_.a = self.a


class SpiMaster(reg.RegisterDevice):
    ctrl: SpiCtrlRegister[0]
    send_low: reg.W[4]
    send_high: reg.W[8]
    receive_low: reg.R[12]
    receive_high: reg.R[16]

    def __init__(
        self,
        spi: std.spi.Spi,
        clk_period=std.Duration,
    ):
        super().__init__()
        self.spi = spi
        self.clk_period = clk_period

    def _impl_(self, ctx):
        self.master = std.spi.SpiMaster(ctx, self.spi, clk_period=self.clk_period)
        self.send_data = Signal[BitVector[64]](Null)
        self.receive_data = Signal[BitVector[64]](Null)

    async def _impl_sequential_(self):
        async with self.ctrl.transaction_active:
            self.receive_data <<= await self.master.parallel_transaction(
                self.send_data, self.ctrl.count
            )

    def _impl_concurrent_(self):
        self.receive_low <<= self.receive_data[31:0]
        self.receive_high <<= self.receive_data[63:32]
        self.send_data[31:0] <<= self.send_low
        self.send_data[63:32] <<= self.send_high


class Wait(reg.Register):
    async def on_write(self, value: BitVector, mask=Full):
        std.wait_for(value.unsigned)


class Interface(reg.RegisterDevice):
    """
    Collection of all hardware interfaces.
    """

    rgb_a: RgbLed[0x100]
    rgb_b: RgbLed[0x104]

    spi: SpiMaster[0x200]

    def __init__(self, rgb_a, rgb_b, spi, spi_period):
        self.rgb_a = RgbLed(rgb_a)
        self.rgb_b = RgbLed(rgb_b)
        self.spi = SpiMaster(spi, spi_period)


class Args:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs


def _main_(switches, leds, buttons, ethernet, eth, eth_ctx, uart_rx, uart_tx, all_regs):
    con = interconnect.reserve(0x10000000, 10)

    con.registers()

    all_regs(
        {
            0: reg.Input(switches, "switches"),
            4: reg.Output(leds, "leds"),
            8: Wait(),
            12: reg.R(buttons, "buttons"),
            0x100: ethernet.EthernetDevice(
                ctx=eth_ctx,
                crsdv=eth.crsdv,
                rxd0=eth.rxd0,
                rxd1=eth.rxd1,
                txen=eth.txen,
                txd0=eth.txd0,
                txd1=eth.txd1,
                uart_tx=uart_tx,
            ),
            0x200: ethernet.UartDevice(
                ctx=eth_ctx,
                rx=uart_rx,
                tx=uart_tx,
                baud=std.uart.Baud.BAUD_115200,
            ),
        }
    )

    class AllRegisters(reg.RegisterDeviceXX):
        SW = reg.R[0](switches)
        LED = reg.W[4](leds)
        WAIT = Wait[8]()
        BUTTONS = reg.R[12](buttons_vec)
        ETH = ethernet.EthernetDevice[0x100](
            ctx=eth_ctx,
            crsdv=eth.crsdv,
            rxd0=eth.rxd0,
            rxd1=eth.rxd1,
            txen=eth.txen,
            txd0=eth.txd0,
            txd1=eth.txd1,
            uart_tx=uart_tx,
        )

        UART = ethernet.UartDevice[0x200](
            ctx=eth_ctx,
            rx=uart_rx,
            tx=uart_tx,
            baud=std.uart.Baud.BAUD_115200,
        )

        SEVENT_SEG = ethernet.HexDisplay[0x300](
            ctx=eth_ctx, anodes=seven_seg.anodes, cathodes=seven_seg.cathodes
        )

        RGB_A = RgbLed[0x400](ctx=eth_ctx, rgb=rgb_1)
        RGB_B = RgbLed[0x404](ctx=eth_ctx, rgb=rgb_2)

        SPI = SpiMaster[0x800](
            ctx=eth_ctx, spi=acc.spi, clk_period=std.MHz(2.5).period()
        )

    RegisterDevice(
        interconnect.reserve(0x10000000, 10),
        [
            PartialRegister(0x00, switches, read_only=True),
            PartialRegister(0x04, leds, write_only=True),
            WaitRegister(0x08),
            PartialRegister(0x0C, button_vec, read_only=True),
            ethernet.EthernetDevice(
                0x10,
                ctx=eth_ctx,
                crsdv=eth.crsdv,
                rxd0=eth.rxd0,
                rxd1=eth.rxd1,
                txen=eth.txen,
                txd0=eth.txd0,
                txd1=eth.txd1,
                uart_tx=uart_tx,
            ),
            ethernet.UartDevice(
                0x20,
                ctx=eth_ctx,
                rx=uart_rx,
                tx=uart_tx,
                baud=std.uart.Baud.BAUD_115200,
            ),
            ethernet.HexDisplay(
                0x100, ctx=eth_ctx, anodes=seven_seg.anodes, cathodes=seven_seg.cathodes
            ),
            ethernet.RgbLed(0x180, ctx=eth_ctx, rgb=rgb_1),
            ethernet.RgbLed(0x184, ctx=eth_ctx, rgb=rgb_2),
            ethernet.SpiMaster(
                0x200, ctx=eth_ctx, spi=acc.spi, clk_period=std.MHz(2.5).period()
            ),
        ],
    )


if False:
    ctrl: CtrlRegister[0]

    send_low: reg.SimpleRegister.Wr[
        4,
        "dasd asist sfiasrlasfljsdalfölasd asdflsladjoislfldsafldn welsd wejjoinvhhsdf fsds",
    ]

    send_high: reg.SimpleRegister.Wr[8]

    receive_low: reg.SimpleRegister.Rd[12]
    receive_high: reg.SimpleRegister.Rd[16]

    def __init__(
        self,
        ctx: std.SequentialContext,
        spi: std.spi.Spi,
        clk_period=std.Duration,
    ):
        master = std.spi.SpiMaster(ctx, spi, clk_period=clk_period)

        send_data = Signal[BitVector[64]](Null)
        receive_data = Signal[BitVector[64]](Null)
        ctrl_register = Signal[BitVector[32]](Null)

        transaction_active = std.SyncFlag()

        @ctx
        async def proc():
            nonlocal receive_data

            async with transaction_active:
                receive_data <<= await master.parallel_transaction(
                    send_data, ctrl_register[5:0].unsigned
                )

        SimpleRegister()
        super().__init__(
            [
                CtrlRegister(0x00),
                SimpleRegister(0x04, send_data[31:0], write_only=True),
                SimpleRegister(0x08, send_data[63:32], write_only=True),
                SimpleRegister(0x0C, receive_data[31:0], read_only=True),
                SimpleRegister(0x10, receive_data[63:32], read_only=True),
            ],
        )
