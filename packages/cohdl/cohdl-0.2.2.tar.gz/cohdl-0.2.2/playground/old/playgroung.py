from __future__ import annotations

from cohdl import Bit, BitVector, Unsigned, Signal, Signed, Entity, Port
from cohdl import std

from collections import namedtuple


class TemplateArg:
    def __new__(cls, *field_names: str):
        return namedtuple(cls.__name__, *field_names)


def _template_arg_hash(self):
    return hash(tuple([getattr(self, name) for name in self._field_names]))


def _template_arg_eq(self, other):
    return type(self) is type(other) and all(
        getattr(self, name) == getattr(other, name) for name in self._field_names
    )


def template_arg(*field_names):
    arg_type = namedtuple(*field_names)
    arg_type._field_names = field_names

    arg_type.__hash__ = _template_arg_hash
    arg_type.__eq__ = _template_arg_eq


class MyRecord(std.Record):
    a: Bit
    b: BitVector[8]


class MyEntity(Entity):

    inp_a = Port.input(Bit)
    inp_b = Port.input(BitVector[8])

    out_a = Port.output(Bit)
    out_b = Port.output(BitVector[8])

    def architecture(self):
        arr = std.Array[MyRecord, 8]()
        fifo = std.Fifo[MyRecord, 10]()

        @std.concurrent
        def logic():
            inp_rec = std.Ref[MyRecord](self.inp_a, self.inp_b)
            # out_rec = std.Ref[MyRecord](self.out_a, self.out_b)

            # arr[4] <<= inp_rec

            # arr[7].a <<= inp_rec.a

            # out_rec.a <<= inp_rec.a
            # out_rec.b <<= inp_rec.b

            # out_rec <<= arr[6]

            fifo.push(inp_rec)


print(std.VhdlCompiler.to_string(MyEntity))
