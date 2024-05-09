from __future__ import annotations

import enum

from cohdl import std
from cohdl import BitVector, Unsigned, Signed, Bit, Null, Full, Signal

from .meta import MetaMember, MetaObject


class MetaData:
    def __init__(self, global_offset: int):
        self.global_offset = global_offset


class RegisterObject(MetaMember, MetaObject):
    _addr_offset_: int
    _addr_size_: int
    _comment_: str
    _name_: str

    _readable_: bool
    _writable_: bool

    def _impl_(self, ctx: std.SequentialContext):
        pass

    def _impl_sequential_(self):
        pass

    def _impl_concurrent_(self):
        pass

    def __init__(self):
        self._parent_offset_: int

    def _meta_config_(self, parent, name, /, parent_offset, comment=""):
        assert isinstance(parent, RegisterDevice)

        self._parent_offset_ = parent_offset
        self._comment_ = comment
        self._name_ = name

        self._addr_offset_ = parent._addr_offset_ + self._parent_offset_
        parent._items_.append(self)

        return super()._meta_config_(parent)

    def on_read_base(self, addr, meta: MetaData):
        return Null

    def on_write_base(self, addr, data, mask, meta: MetaData):
        pass

    def documentation(self, parent_offset: int = 0) -> TextBlock:
        offset = parent_offset + self._addr_offset_
        return TextBlock(title=f"@{offset:08x}")


class RegisterDevice(RegisterObject):
    _global_offset_: int

    def _flatten_(self):
        result: list[RegisterObject] = []

        for item in self._items_:
            if isinstance(item, RegisterDevice):
                result.extend(item._flatten_())
            else:
                result.append(item)

        return result

    def __init__(self):
        self._offset_: int
        self._items_: list[RegisterObject] = []

    def _meta_config_(self, parent, name, /, *args, **kwargs):
        return super()._meta_config_(parent, name, *args, **kwargs)


class GenericRegister(RegisterObject):
    def _meta_config_(self, parent, name, /, args):
        self._addr_size_ = 4

        if not isinstance(args, tuple):
            args = (args,)

        super()._meta_config_(parent, name, *args)

    async def on_read_base(self, addr, meta):
        return await std.as_awaitable(self.on_read)

    async def on_write_base(self, addr, data, mask, meta):
        return await std.as_awaitable(self.on_write, data, mask)

    def on_read(self):
        return Null

    def on_write(self, data, mask):
        pass


class Input(GenericRegister):
    def __init__(self, val: Signal[BitVector], comment: str | None = None):
        assert self._val.width <= 32
        self._val = val

    def on_read(self):
        return self.val()

    def val(self):
        if self._val.width == 32:
            return self._val
        else:
            return std.zeros(32 - self._val.width) @ self._val


class Output(GenericRegister):
    def __init__(self, val: Signal[BitVector]):
        self._val = val

    def on_read(self):
        return self.val()

    def on_write(self, data, mask):
        self._val <<= std.apply_mask(
            self._val, data.lsb(self._val.width), mask.lsb(self._val.width)
        )

    def val(self):
        if self._val.width == 32:
            return self._val
        else:
            return std.zeros(32 - self._val.width) @ self._val


class RW(GenericRegister):
    def __init__(self):
        super().__init__()
        self._val = Signal[BitVector[32]](Null)

    def on_read(self):
        return self._val

    def on_write(self, data, mask):
        self._val <<= std.apply_mask(self._val, data, mask)

    def val(self):
        return self._val


class W(GenericRegister):
    def __init__(self):
        super().__init__()
        self._val = Signal[BitVector[32]](Null)

    def on_read(self):
        return Null

    def on_write(self, data, mask):
        self._val <<= std.apply_mask(self._val, data, mask)

    def val(self):
        return self._val


class R(GenericRegister):
    def __init__(self):
        super().__init__()
        self._val = Signal[BitVector[32]](Null)

    def on_read(self):
        return self._val

    def on_write(self, data, mask):
        pass

    def val(self):
        return self._val

    def __ilshift__(self, value):
        self._val <<= value


class _FieldType(enum.Enum):
    BITVECTOR = enum.auto()
    UNSIGNED = enum.auto()
    SIGNED = enum.auto()


class Field(MetaMember):
    _field_type: _FieldType = _FieldType.BITVECTOR
    _is_bit: bool
    _width: int
    _bit_range_: slice
    _comment_: str
    _name_: str

    def __init__(self):
        self._field: Bit | BitVector

    def _meta_config_(self, parent, name, /, range: int | slice, comment: str = ""):
        assert isinstance(parent, Register)
        self._bit_range_ = range
        self._comment_ = comment
        self._name_ = name
        parent._fields_.append(self)

        if isinstance(range, int):
            self._is_bit = True
            self._width = 1

            if parent._raw is None:
                self._field = Signal[Bit](Null)
            else:
                self._field = parent._raw[range]
        else:
            self._is_bit = False
            self._width = abs(range.stop - range.start) + 1

            if parent._raw is None:
                match self._field_type:
                    case _FieldType.BITVECTOR:
                        self._field = Signal[BitVector[self._width]](Null)
                    case _FieldType.UNSIGNED:
                        self._field = Signal[Unsigned[self._width]](Null)
                    case _FieldType.SIGNED:
                        self._field = Signal[Signed[self._width]](Null)
                    case _:
                        raise AssertionError("invalid field type")
            else:
                match self._field_type:
                    case _FieldType.BITVECTOR:
                        self._field = parent._raw[range].bitvector
                    case _FieldType.UNSIGNED:
                        self._field = parent._raw[range].unsigned
                    case _FieldType.SIGNED:
                        self._field = parent._raw[range].signed
                    case _:
                        raise AssertionError("invalid field type")

    def __ilshift__(self, value):
        if isinstance(value, Field):
            self._field <<= value._field
        else:
            self._field <<= value

    def val(self):
        return self._field


class FieldU(Field):
    _field_type = _FieldType.UNSIGNED


class FieldS(Field):
    _field_type = _FieldType.SIGNED


class _UnusedField:
    def __init__(self, width: int):
        self._width = width

    def __ilshift__(self, value):
        assert isinstance(value, _UnusedField)
        assert self._width == value._width

    def val(self):
        return std.zeros(self._width)


class Register(GenericRegister):
    def __init__(self, raw: BitVector | None = None):
        if raw is not None:
            assert std.instance_check(raw, BitVector[32])

        self._fields_: list[Field] = []
        self._raw = raw

    def _meta_config_(self, parent, name, /, args):
        sorted_fields = sorted(self._fields_, key=lambda f: f._bit_range_.start)

        complete_fields = []
        prev_end = 0

        for field in sorted_fields:
            start = field._bit_range_.start
            end = field._bit_range_.stop

            if start != prev_end:
                assert start > prev_end
                complete_fields.append(_UnusedField(start - prev_end))

            complete_fields.append(field)
            prev_end = end + 1

        if prev_end != 32:
            assert prev_end < 32
            complete_fields.append(_UnusedField(32 - prev_end))

        return super()._meta_config_(parent, name, args)

    def on_read(self):
        return self.val()

    def on_write(self, data: BitVector, mask: BitVector):
        return super().on_write(data, mask)

    def val(self):
        return std.concat(*[f.val() for f in self._fields_[::-1]])

    def __ilshift__(self, value: Register):
        assert type(self) is type(value)

        for target, src in zip(self._fields_, value._fields_):
            target <<= src


class AddrRange(RegisterObject):
    def _meta_config_(self, parent, name, /, parent_offset, comment=""):
        return super()._meta_config_(parent, name, parent_offset, comment)

    def on_read_base(self, addr, spec):
        return super().on_read_base(addr, spec)

    def on_write_base(self, addr, data, mask, spec):
        return super().on_write_base(addr, data, mask, spec)


class Array(RegisterObject):
    def _flatten_(self):
        return [*self._elements]

    def __init__(self, elements: list[RegisterObject] | None = None):
        self._elements = elements

    def _meta_config_(
        self, parent, name, /, elem_type, offset_end_stride: slice, comment=""
    ):
        start = offset_end_stride.start
        stop = offset_end_stride.stop
        step = offset_end_stride.step

        count = (stop - start) // step

        if self._elements is None:
            self._elements = [elem_type() for _ in range(count)]
        else:
            assert len(self._elements) == count and all(
                isinstance(elem, elem_type) for elem in self._elements
            )

        for index, (elem, off) in enumerate(
            zip(self._elements, range(*offset_end_stride))
        ):
            elem._meta_config_(self, f"{name}[{index}]", off)

        super().__init__()

        return super()._meta_config_(parent, name, start, comment)


def collection(elements: dict[int, RegisterObject]):
    named_elements = [(f"ADDR_0x{pos:08x}", pos, obj) for pos, obj in elements.items()]

    class RegCollection(RegisterDevice):
        __annotations__ = {name: type(obj)[pos] for name, pos, obj in named_elements}

        def __init__(self):
            for name, _, obj in named_elements:
                setattr(self, name, obj)

    return RegCollection()


from cohdl.utility import IndentBlock, TextBlock


def documentation(inp: RegisterObject) -> TextBlock:
    return inp.documentation()
