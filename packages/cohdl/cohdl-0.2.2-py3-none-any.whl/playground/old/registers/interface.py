from cohdl import std, Variable, BitVector, Null

from . import reg


class Interface:
    def __init__(self):
        self._ctx: std.SequentialContext

    def read_handler(self):
        ...

    def write_handler(self):
        ...


def register_interface(interface: Interface, reg_device: reg.RegisterDevice):
    flat = reg_device._flatten_()

    for elem in flat:
        if type(elem)._impl_ is not reg.RegisterObject._impl_:
            elem._impl_(interface._ctx)

        if type(elem)._impl_sequential_ is not reg.RegisterObject._impl_sequential_:
            interface._ctx(elem._impl_sequential_)

        if type(elem)._impl_concurrent_ is not reg.RegisterObject._impl_concurrent_:
            std.concurrent(elem._impl_concurrent_)

    async def on_read(addr):
        result = Variable[BitVector[32]](Null)

        for elem in flat:
            if elem._readable_:
                if elem._addr_offset_ == addr:
                    result @= await std.as_awaitable(elem.on_read_base, addr)
                    break

        return result

    async def on_write(addr, data, mask):
        for elem in flat:
            if elem._writable_:
                if elem._addr_offset_ == addr:
                    await std.as_awaitable(elem.on_write_base, addr, data, mask)
