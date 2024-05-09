from __future__ import annotations

from cohdl import pyeval

from cohdl import enum

enum.Enum()


class _MetaClassInfo:
    def __init__(self, original_init):
        self._original_init = original_init


class MetaMember:
    def __class_getitem__(cls, args):
        class _MetaMember(cls):
            pass

        setattr(_MetaMember, "@meta_args", args)
        return _MetaMember

    def _meta_config_(self, parent, /, *args, **kwargs):
        pass


@pyeval
def _wrapped_init_(self: MetaObject, *args, **kwargs):
    meta_class_info: _MetaClassInfo = getattr("@meta_class_info", type(self))

    self._interface_ = MetaInterface()
    meta_class_info._original_init(self, *args, **kwargs)

    annotations = type(self).__annotations__

    assert isinstance(self._interface_, MetaInterface)

    for name, ann in annotations.items():
        if issubclass(ann, MetaMember):
            if name not in self._interface_.__dict__:
                setattr(self._interface_, name, ann._default_construct_())

            member = self._interface_.__dict__[name]

            assert isinstance(member, MetaMember)
            assert not member._reg_is_configured_()

            member._meta_config_(self, name, ann._meta_args_())

    for value in self._interface_.__dict__.values():
        assert isinstance(value, MetaMember)
        assert value._reg_is_configured()

    for name, value in self.__dict__.items():
        if isinstance(value, MetaMember):
            assert (
                name in self._interface_.__dict__
            ), "the object '{name}' is not part of the interface definition of this class"

    self._interface_._frozen = True


class MetaInterface:
    _frozen = False

    def __setattr__(self, attr, value):
        if getattr(self, "_frozen"):
            raise AttributeError("Trying to set attribute on a frozen instance")
        return super().__setattr__(attr, value)

    def _cohdlstd_on_freeze(self):
        for name, value in self.__dict__.items():
            assert isinstance(
                value, MetaMember
            ), f"'{name}' is not a valid interface member"

    def _cohdlstd_members(self) -> list[MetaMember]:
        return [*self.__dict__.values()]

    def _cohdlstd_sorted_members(self) -> list[MetaMember]:
        return sorted(self._cohdl_members_(), lambda m: m._offset_)


class MetaObject:
    _cohdlstd_interface_type: type[MetaInterface]

    _interface_: MetaInterface

    def __init_subclass__(cls) -> None:
        cls._cohdlstd_reg_class_info = _MetaClassInfo(cls.__init__)
        cls.__init__ = _wrapped_init_
