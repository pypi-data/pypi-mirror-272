from __future__ import annotations

from cohdl.std.axi.axi4_light.base import Axi4Light
from cohdl.std.reg import reg32
from cohdl import Signal, Unsigned

from cohdl import Signal
from cohdl.std.axi.axi4_light.base import Axi4Light
from cohdl.std.reg import reg32

import cohdl
from cohdl import Port, Bit, BitVector, Unsigned, Null, Full
from cohdl import std
from cohdl.std.axi import axi4_light as axi

from typing import Annotated as Ann
from cohdl.std.reg import to_system_rdl


class AxiBaseEntity(cohdl.Entity):
    clk = Port.input(Bit)
    reset = Port.input(Bit)

    axi_awaddr = Port.input(Unsigned[32])
    axi_awprot = Port.input(Unsigned[3])
    axi_awvalid = Port.input(Bit)
    axi_awready = Port.output(Bit, default=Null)

    axi_wdata = Port.input(BitVector[32])
    axi_wstrb = Port.input(BitVector[4])
    axi_wvalid = Port.input(Bit)
    axi_wready = Port.output(Bit, default=Null)

    axi_bresp = Port.output(BitVector[2], default=Null)
    axi_bvalid = Port.output(Bit, default=Null)
    axi_bready = Port.input(Bit)

    axi_araddr = Port.input(Unsigned[32])
    axi_arprot = Port.input(Unsigned[3])
    axi_arvalid = Port.input(Bit)
    axi_arready = Port.output(Bit, default=Null)

    axi_rdata = Port.output(BitVector[32], default=Null)
    axi_rresp = Port.output(BitVector[2], default=Null)
    axi_rvalid = Port.output(Bit, default=Null)
    axi_rready = Port.input(Bit)

    def impl_registers(self, connection: axi.Axi4Light):
        raise NotImplementedError()

    def architecture(self):
        clk = std.Clock(self.clk)
        reset = std.Reset(self.reset)

        axi_con = axi.Axi4Light(
            clk=clk,
            reset=reset,
            wraddr=axi.Axi4Light.WrAddr(
                valid=self.axi_awvalid,
                ready=self.axi_awready,
                awaddr=self.axi_awaddr,
                awprot=self.axi_awprot,
            ),
            wrdata=axi.Axi4Light.WrData(
                valid=self.axi_wvalid,
                ready=self.axi_wready,
                wdata=self.axi_wdata,
                wstrb=self.axi_wstrb,
            ),
            wrresp=axi.Axi4Light.WrResp(
                valid=self.axi_bvalid,
                ready=self.axi_bready,
                bresp=self.axi_bresp,
            ),
            rdaddr=axi.Axi4Light.RdAddr(
                valid=self.axi_arvalid,
                ready=self.axi_arready,
                araddr=self.axi_araddr,
                arprot=self.axi_arprot,
            ),
            rddata=axi.Axi4Light.RdData(
                valid=self.axi_rvalid,
                ready=self.axi_rready,
                rdata=self.axi_rdata,
                rresp=self.axi_rresp,
            ),
        )

        self.impl_registers(axi_con)


class ClkDevice(reg32.RegFile, word_count=2):
    class Ctrl(reg32.Register):
        enable: reg32.MemField[0]
        prescaler: reg32.MemUField[31:16]

    ctrl: Ctrl[0]
    count: reg32.UWord[4]

    def _config_(self):
        self._counter = Signal[Unsigned[32]](0)

    def _impl_sequential_(self) -> None:
        if self.ctrl.enable:
            if self._counter >= self.ctrl.prescaler.val():
                self.count <<= self.count.raw + 1
                self._counter <<= 0
            else:
                self._counter <<= self._counter + 1


class AddrMap(reg32.AddrMap, word_count=64):
    clk_1: Ann[ClkDevice[0x00], "asdfasdfasdf"]
    clk_2: ClkDevice[0x08]
    clk_3: ClkDevice[0x10]
    clk_4: ClkDevice[0x18]

    def _config_(self):
        self.clk_1._config_()
        self.clk_2._config_()
        self.clk_3._config_()
        self.clk_4._config_()


class ExampleEntity(AxiBaseEntity):
    def impl_registers(self, connection: Axi4Light):
        connection.connect_addr_map(AddrMap())


print(to_system_rdl(AddrMap))
