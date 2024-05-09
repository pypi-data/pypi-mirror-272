from __future__ import annotations

from cohdl import Bit, BitVector, Unsigned, Signal, Null, Full
from cohdl import std


class Register:
    def __init__(self, offset):
        assert offset % 4 == 0
        self.offset = offset

    async def on_read(self):
        return Null

    async def on_write(self, data, mask=Full):
        pass


class RegisterSet:
    def __init__(self, content: list[Register | RegisterSet], offset=0):
        self._content = content
        self._offset = offset

    def get_registers(self, offset=0):
        result = []

        for entry in self._content:
            if isinstance(entry, Register):
                entry.offset += self._offset + offset
                result.append(entry)
            elif isinstance(entry, RegisterSet):
                entry._offset += self._offset + offset
                result.extend(entry.get_registers())

        return result


class RegisterDevice:
    def __init__(
        self, interface: MemoryInterface, registers: list[Register | RegisterSet]
    ):
        flat_registers: list[Register] = []

        for entry in registers:
            if isinstance(entry, Register):
                flat_registers.append(entry)
            else:
                flat_registers.extend(entry.get_registers())

        for reg in flat_registers:
            assert reg.offset < 2 ** interface.addr_width()

        async def on_read(addr):
            aligned_addr = addr.unsigned

            result = Variable[BitVector[32]](Null)

            for reg in flat_registers:
                if reg.offset == aligned_addr:
                    result @= await std.as_awaitable(reg.on_read)
                    break

            return result

        async def on_write(addr, data, mask):
            aligned_addr = addr.unsigned

            for reg in flat_registers:
                if reg.offset == aligned_addr:
                    await std.as_awaitable(reg.on_write, data, mask)
                    break

        interface.run_request_handler(on_read, on_write)


class SimpleRegister(Register):
    def __init__(
        self,
        offset: int,
        sig: Signal[BitVector[32]],
        read_only: bool = False,
        write_only: bool = False,
    ):
        super().__init__(offset)

        self.sig = sig
        self.read_only = read_only
        self.write_only = write_only

    async def on_read(self):
        if self.write_only:
            return Null
        else:
            return self.sig

    async def on_write(self, data, mask=Full):
        if self.read_only:
            pass
        else:
            self.sig <<= std.apply_mask(self.sig, data, std.stretch(mask, 8))


class PartialRegister(Register):
    def __init__(
        self,
        offset: int,
        sig: Signal[BitVector],
        read_only: bool = False,
        write_only: bool = False,
    ):
        super().__init__(offset)

        self.sig = sig
        self.read_only = read_only
        self.write_only = write_only

    async def on_read(self):
        if self.write_only:
            return Null
        else:
            return self.sig.unsigned.resize(32)

    async def on_write(self, data: Signal[BitVector[32]], mask=Full):
        if self.read_only:
            pass
        else:
            self.sig <<= data.lsb(self.sig.width)


class WaitRegister(Register):
    async def on_write(self, data: Unsigned, mask=Full):
        await std.wait_for(data.unsigned)


a = "asdf" "sadf"


class reg:
    class R:
        ...

    class W:
        ...

    class RW:
        ...

    class Field:
        def __class_getitem__(cls, *args) -> type[reg.Field]:
            ...

        ...

    class FieldS(Field):
        ...

    class FieldU(Field):
        ...

    class Register:
        ...

    class FieldRegister:
        def _data_view_(self, input, mask=Full) -> SpiMaster.CtrlRegister:
            ...

        def _super_init_(self):
            self._raw_ = Signal[BitVector[32]]()

            @std.concurrent
            def logic():
                self._raw_[5:2] <<= self.count
                self._raw_[8] <<= self.active

        def on_read_default(self):
            return self._raw_

        def on_write_default(self, data, mask=Full):
            field_view = self.field_view(data, mask)

    class RegisterDevice:
        ...


class RgbLed(reg.Register):
    "This register device controls the rgb leds"

    r: reg.FieldU[7:0]
    g: reg.FieldU[15:8]
    b: reg.FieldU[23:16]

    def __init__(self, ctx: std.SequentialContext, rgb):
        cnt = Signal[Unsigned[8]](Null)

        @ctx
        async def proc():
            await std.wait_for(std.us(5))
            cnt.next = cnt + 1
            rgb.red <<= cnt < self.r
            rgb.green <<= cnt < self.g
            rgb.blue <<= cnt < self.b


class SpiMaster(reg.RegisterDevice):
    class CtrlRegister(reg.Register):
        "This register controls the spi communication"

        count: reg.Field[5:2, 0]["asdf"]
        active: reg.Field[8]["set to '1' while a spi transaction is in progress"]

        def __init__(self):
            self.transaction_active = std.SyncFlag()

            std.concurrent_eval(self.active, self.transaction_active.is_set)

        def on_write(self, data, mask=Full):
            view = self._data_view_(data, mask)

            if view.active:
                assert not self.transaction_active.is_set()
                self.transaction_active.set()

            self.count <<= view.count

    ctrl: CtrlRegister[0]
    send_low: reg.W[4]
    send_high: reg.W[8]
    receive_low: reg.R[12]
    receive_high: reg.R[16]

    def __init__(
        self,
        ctx: std.SequentialContext,
        spi: std.spi.Spi,
        clk_period=std.Duration,
    ):
        super().__init__()

        master = std.spi.SpiMaster(ctx, spi, clk_period=clk_period)

        send_data = Signal[BitVector[64]](Null)
        receive_data = Signal[BitVector[64]](Null)

        @std.concurrent
        def logic():
            self.receive_low <<= receive_data[31:0]
            self.receive_high <<= receive_data[63:32]
            send_data[31:0] <<= self.send_low
            send_data[63:32] <<= self.send_high

        @ctx
        async def proc():
            nonlocal receive_data

            async with self.ctrl.transaction_active:
                receive_data <<= await master.parallel_transaction(
                    send_data, self.ctrl.count
                )


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

    def __init__(self, ctx, rgb_a, rgb_b, spi, spi_period):
        self.rgb_a = RgbLed(ctx, rgb_a)
        self.rgb_b = RgbLed(ctx, rgb_b)
        self.spi = SpiMaster(ctx, spi, spi_period)


class Args:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs


def _main_():
    con = interconnect.reserve(0x10000000, 10)

    con.registers()

    all_regs(
        {
            0: reg.R(switches, "switches"),
            4: reg.W(leds, "leds"),
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
