from __future__ import annotations

from cohdl import Port, BitVector, Signed, Unsigned
from cohdl import Entity

from cohdl import std

# obtain generic type and use it to produce a generic record
T = std.template_arg.Type


class Coord(std.Record[T]):
    x: T
    y: T

    def __add__(self, other: Coord) -> Coord:
        return type(self)(x=self.x + other.x, y=self.y + other.y)


class MyEntity(Entity):
    x_in = Port.input(BitVector[32])
    y_in = Port.input(BitVector[32])

    x_out_signed = Port.output(BitVector[32])
    y_out_signed = Port.output(BitVector[32])

    x_out_unsigned = Port.output(BitVector[16])
    y_out_unsigned = Port.output(BitVector[16])

    def architecture(self):
        # specialize the generic
        out_signed = std.Ref[Coord[Signed[32]]](self.x_out_signed, self.y_out_signed)

        @std.concurrent
        def logic_signed():
            nonlocal out_signed

            # specialize generic Coord with Signed[32]
            coord_in = Coord[Signed[32]](self.x_in, self.y_in)

            # coord is not a signal
            # but can be assigned like one
            out_signed <<= coord_in

        @std.concurrent
        def logic_unsigned():

            # specialize generic Coord with Unsigned[16]
            a = Coord[Unsigned[16]](self.x_in[15:0], self.y_in[15:0])
            b = Coord[Unsigned[16]](self.x_in[31:16], self.y_in[31:16])

            # create a new instance of Coord from constant arguments
            c = Coord[Unsigned[16]](3, 4)

            sum = a + b + c

            self.x_out_unsigned <<= sum.x
            self.y_out_unsigned <<= sum.y


vhdl = std.VhdlCompiler.to_string(MyEntity)
print(vhdl)
