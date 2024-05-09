from __future__ import annotations
from typing import Any, Type

from cohdl import std
from cohdl import Temporary, Signal, Signed, Unsigned, BitVector, Array, pyeval, Bit
from cohdl import Entity, Port
from cohdl._core import AssignMode, concurrent_context


if False:

    class MyArgs:
        def __init__(self, args):
            self.width = args[0]
            self.t = args[1]

        def __str__(self):
            return f"MyArgs(width={self.width}, t={self.t})"

        def __eq__(self, other: MyArgs):
            return self.width == other.width and self.t == other.t

    class MyTemplate(std.Template[MyArgs]):
        def __init__(self, arg):
            print(f" >> {self._template_arg_.t} == {arg}")

        @classmethod
        def _from_bits_(cls, bits, qualifier=std.tc):
            return cls(cls._template_arg_.t)

        def _to_bits_(self):
            ...

    my_fixed = std.SFixed[12:-5]()

    my_fixed.variable

    a = MyTemplate[1:2, 4](4)
    b = MyTemplate[1:2, 4](3)
    c = MyTemplate[1:2, 4](2)
    d = MyTemplate[1:2, 3](1)

    print(a is b)
    print(a is c)
    print(a is d)


#
#
#


class Complex(std.Template[int], std.AssignableType):
    @classmethod
    def _make_qualified_(cls, Qualifier, real=None, imag=None):
        return cls(
            real=Qualifier(Signed[cls._template_arg_]() if real is None else real),
            imag=Qualifier(Signed[cls._template_arg_]() if imag is None else imag),
        )

    def _assign_(self, source: Complex, mode: AssignMode) -> None:
        self._real._assign_(source._real, mode)
        self._imag._assign_(source._imag, mode)

    def __init__(self, real: Signed, imag: Signed):
        assert real.width == self._template_arg_ == imag.width

        self._real = real
        self._imag = imag

    @classmethod
    def _from_bits_(cls, bits: BitVector, qualifier) -> Complex:
        # deserialize an instance of this class from a BitVector
        #
        # _from_bits_ takes two arguments
        #   - an input bitvector containing the serialized data
        #   - a type qualifier like Signal/Variable/Temporary that
        #       should be applied to each component of the generated
        #       output value
        #
        # by default std.from_bits will pass std.tc as the qualifier
        # to keep values as runtime constants if possible.

        assert bits.width == cls._template_arg_ * 2

        print(" ----- ", qualifier, cls, bits.lsb(cls._template_arg_))

        return cls(
            real=qualifier(bits.lsb(cls._template_arg_)).signed,
            imag=qualifier(bits.msb(cls._template_arg_)).signed,
        )

    def _to_bits_(self):
        return self._imag @ self._real

    def __str__(self):
        return f"Complex[{self._template_arg_}]({self._real}, {self._imag})"

    @classmethod
    def _template_deduce_(cls, real, imag):
        assert real.width == imag.width

        print(f">>>>>>>>>>< deduce type {real.width}")
        print("")

        return Complex[real.width]


class Complex(std.Template[int]):
    def __init__(self, real: Signed, imag: Signed):
        assert real.width == imag.width == self._template_arg_
        self._real = real
        self._imag = imag

    def _serialize_width_(cls):
        ...

    @classmethod
    def _count_bits_(cls) -> int:
        return cls._template_arg_ * 2

    @classmethod
    def _from_bits_(cls, bits: BitVector, qualifier) -> Complex:
        assert bits.width == cls._bit_width_()

        return cls(
            real=qualifier(bits.lsb(cls._template_arg_)).signed,
            imag=qualifier(bits.msb(cls._template_arg_)).signed,
        )

    def _to_bits_(self):
        return self._imag @ self._real


class ComplexArg:
    value: int


class Complex(std.Template[ComplexArg]):
    _real: Signed[ComplexArg.value]

    def __init__(self, real: Signed, imag: Signed):
        assert real.width == imag.width == self._template_arg_
        self._real = real
        self._imag = imag

    def _serialize_width_(cls):
        ...

    @classmethod
    def _count_bits_(cls) -> int:
        return cls._template_arg_ * 2

    @classmethod
    def _from_bits_(cls, bits: BitVector, qualifier) -> Complex:
        assert bits.width == cls._bit_width_()

        return cls(
            real=qualifier(bits.lsb(cls._template_arg_)).signed,
            imag=qualifier(bits.msb(cls._template_arg_)).signed,
        )

    def _to_bits_(self):
        return self._imag @ self._real


class _TupleArgs:
    def __init__(self, args):
        self._args = args


class Tuple(std.Template[_TupleArgs]):
    def __init__(self, args):
        self._content = []

    @staticmethod
    @pyeval
    def _add_element(l: list, element):
        l.append(element)

    @classmethod
    @pyeval
    def _count_bits_(cls) -> int:
        return sum(elem._count_bits_() for elem in cls._template_arg_._args)

    @classmethod
    def _from_bits_(cls, bits: BitVector, qualifier) -> Tuple:
        class ConditionLock:
            """
            a class, that ensure that all calls to .check()
            and by default the constructor occur in the same condition
            block that means are not separated by an calls to if/if-expr/select/match
            """

        with std.Deserializer[qualifier](bits) as deserializer:
            content = []

            for elem_type in cls._template_arg_._args:
                cls._add_element(content, deserializer.deserialize(elem_type))

        return cls(content)

    def _to_bits_(self):
        return std.concat(*[std.to_bits(elem) for elem in self._content][::-1])


class MyEntity(Entity):
    clk = Port.input(Bit)

    a = Port.input(Signed[8])
    b = Port.input(Signed[8])
    c = Port.input(Signed[8])

    x = Port.output(Signed[8])
    y = Port.output(Signed[8])

    def architecture(self):
        arr = std.StdArray[Complex[8], 8]()

        # @std.sequential(std.Clock(self.clk))
        @concurrent_context
        def proc():
            cplx = Complex(self.a, self.b)

            asdf = arr[self.c]

            ser = asdf.bits()
            deser = std.from_bits[Complex[8]](ser)

            arr[self.b] <<= deser

            cplx_out = Complex[8](self.x, self.y)

            cplx_out <<= deser


print(std.VhdlCompiler.to_string(MyEntity))

exit()

my_array = std.Array[Complex[8], 16]()


a = Complex(Signed[8](12), Signed[8](45))

bv = std.to_bits(a)

b = std.from_bits[Complex[8]](bv, Signal)

print(a)
print(bv)
print(b)
