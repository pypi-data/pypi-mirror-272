from __future__ import annotations

from cohdl import std
from cohdl.std import Template
from cohdl.std import Record
from cohdl import (
    Bit,
    BitVector,
    Signal,
    Unsigned,
    Signed,
    Variable,
    Port,
    Entity,
    Null,
    signal,
    variable,
)

from functools import wraps

from typing import Generic, TypeVar, Union, overload

B = TypeVar("B")
T = TypeVar("T")
U = TypeVar("U")


class Bar:
    def bar(self) -> float:
        return 0.0


# Signal[Bit]   -> Signal[Bit]
# Signal[Bar]   -> Bar


class Foo:
    def foo(self):
        ...


class First(Record):
    x: Bit
    y: Bit
    z: Bit


class Rec(Record):
    a: Bit
    b: BitVector[9]

    f: First

    def __add__(self, other):
        return std.make(Rec, self.a ^ other.a, self.b & other.b, self.f)

    def __sub__(self, other):
        return Rec(self.a ^ other.a, self.b & other.b, self.f)


std.ref


class MyEntity(Entity):
    port_a = Port.input(Bit)
    port_b = Port.input(BitVector[9])

    port_x = Port.output(Bit)
    port_y = Port.output(BitVector[9])

    def architecture(self):
        my_array = std.StdArray[Rec, 100]()

        @std.concurrent
        def logic():
            s_first = Signal[First](self.port_a, self.port_a, self.port_a)

            ref_first = ...

            qwe = Variable[First]()

            # self.port_x <<= s_first.x

            # my_first = First(self.port_a, self.port_a, self.port_a)
            # my_rec = Rec(self.port_b[0], self.port_b, my_first)

            # my_first = std.make_ref(First, self.port_a, self.port_a, self.port_a)
            # my_first = First(self.port_a, self.port_a, self.port_a, _qualifier_=std.ref)
            # my_rec = std.make[std.ref](Rec, self.port_b[0], self.port_b, my_first)

            # print(my_first)
            # print(my_rec)

            # my_array[4] <<= my_rec
            # my_array[4].ref.f <<= my_first

            # my_array[4].ref.f <<= my_first
            # my_array[21] <<= my_rec

            ...

        def logic():
            f = First(self.port_a, self.port_a, self.port_a)

            rec_in = Rec(self.port_a, self.port_b, f)

            std.comment("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

            serialized = std.to_bits(rec_in)

            std.comment("AAAAAAAAAA")

            ser = std.make[Signal](std.Serialized[Rec], Null)

            ser.ref.b <<= rec_in.b
            ser.ref.f <<= rec_in.f

            std.comment("AAAAA")

            std.comment("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

            deserialized = std.from_bits[Rec](serialized)

            std.comment("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

            fo = First(self.port_x, self.port_x, self.port_x)

            rec_out = Rec(self.port_x, self.port_y, fo)

            std.comment("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")

            rec_out <<= deserialized - rec_in


print(std.VhdlCompiler.to_string(MyEntity))
std.make
exit()


class TemplateArg:
    def __init__(self, args):
        self.a, self.b = args

    def __hash__(self):
        return hash(self.a) ^ hash(self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
        return f"{self.a},{self.b}"


class MyRecord(Record[TemplateArg]):
    a: BitVector[5]
    b: Bit
    c: Signed[7]
    d: Unsigned[TemplateArg.a]

    def __add__(self, other):
        return std.make(type(self), self.a, other.b, self.c + other.c, self.d - other.d)


m = MyRecord[4, 5]()
s = std.make[Signal](MyRecord[8, 9])
v = std.make[Variable](MyRecord[8, 9])

MyRecord()

print(m)
print(s)
print(v)
print(s + v)

print(std.to_bits(v))

exit()


class TemplateArg:
    def __init__(self, args):
        self.a, self.b = args

    def __hash__(self):
        return hash(self.a) ^ hash(self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
        return f"{self.a},{self.b}"


class MyTemplate(Template[TemplateArg]):
    a: TemplateArg.a
    b: TemplateArg.b


Template_1_2 = MyTemplate[1, 2]
Template_4_2 = MyTemplate[4, 2]

print(Template_1_2.mro())

a = Template_1_2()
b = Template_4_2()

print(
    Template_1_2, a._template_meta_.annotations["a"], a._template_meta_.annotations["b"]
)
print(
    Template_4_2, b._template_meta_.annotations["a"], b._template_meta_.annotations["b"]
)


exit()

from cohdl import Signed, Unsigned, std, Signal, BitVector, Bit, Null


class MyRecord(std.Record):
    a: Unsigned[7]
    b: Signed[4]
    c: BitVector[43]
    d: Bit


class Derived(MyRecord):
    asdf: Bit


a = std.make(Derived)
b = std.make[Signal](Derived, a)
c = std.make[std.ref](Derived, a)

print()
print(repr(a))
print(std.to_bits(a))

print()
print(repr(b))
print(std.to_bits(b))

print()
print(repr(c))
print(std.to_bits(c))


print("\n\nDONE\n\n")
exit()


class WidthType(int):
    pass


class MyRecordTemplate(std.Record[WidthType]):
    a: Unsigned[WidthType]
    b: Signed[WidthType]


print("\n\nDONE\n\n")

m = MyRecordTemplate[4](Signal[Unsigned[4]](), b=Signed[4]())
print("DONE")
m = MyRecordTemplate[4](a=Signal[Unsigned[4]](), b=Signed[4]())
m = MyRecordTemplate[5](b=Signed[5](12), a=Unsigned[5](7))

m = std.make(MyRecordTemplate[3], Unsigned[3](7), Signed[3](1))
v = std.make(MyRecordTemplate[3], Null, ~Null)

# e = Example[123]()

bits = std.to_bits(m)

print(bits)

n = std.from_bits[MyRecordTemplate[3]](bits)

print(n)
print(v)
print(repr(n))
print(n == n)
print(n != n)
