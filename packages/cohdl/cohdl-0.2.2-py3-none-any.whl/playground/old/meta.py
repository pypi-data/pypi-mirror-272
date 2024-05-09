from cohdl import std
from cohdl import BitVector, Unsigned, Signed, Bit, Null, Full, Signal


class MetaData:
    def _config_(self, *args, **kwargs):
        ...

    def __init__(self):
        ...


class MetaUser:
    def __init__(self):
        ...

    def _wrapped_init_(self, *args, **kwargs):
        self._real_init_(*args, **kwargs)

        for name, ann in type(self).__annotations__.items():
            if hasattr(self, name):
                assert isinstance(getattr(self, name), ann)
            else:
                assert issubclass(ann, MetaData)
                setattr(self, ann())

            getattr(self, name)._meta_name_ = name
            getattr(self, name)._config_(*ann._meta_args_)


class Register(MetaData, MetaUser):
    _global_offset_: int

    def __init__(self):
        self._offset_: int

        if not hasattr(self, "_comment_"):
            self._comment_ = ""

        type(self).__a

    def _config_(self, args):
        if not isinstance(args, tuple):
            args = (args,)

        assert len(args) == 1 or len(args) == 2
        assert isinstance(args[0], int)

        self._offset_ = args[0]
        self._comment_ = args[1] if len(args) == 2 else self._comment_


class Field(MetaData):
    ...


class RegisterDevice(MetaData, MetaUser):
    _global_offset_: int
    ...


class Adder(RegisterDevice):
    """
    Example register with two input registers, that
    are added together and returned in a result register
    """

    inp_a: Register.W[0x00, "first summand"]
    inp_b: Register.W[0x04, "second summand"]
    result: Register.R[0x08, "result of inp_a+inp_b"]

    def _impl_concurrent_(self):
        self.result <<= self.inp_a + self.inp_b


#
#
#
#
#


class WaitRegister(Register):
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
        self.rgb.red <<= cnt < self.r.val
        self.rgb.green <<= cnt < self.g.val
        self.rgb.blue <<= cnt < self.b.val

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
