from __future__ import annotations

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
c = std.make[std.identity](Derived, a)

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
