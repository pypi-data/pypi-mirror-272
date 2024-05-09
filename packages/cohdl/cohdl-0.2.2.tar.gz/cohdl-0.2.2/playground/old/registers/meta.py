from cohdl import consteval

pyeval = consteval


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
def _wrapped_init_(self, *args, **kwargs):
    meta_class_info: _MetaClassInfo = getattr("@meta_class_info", type(self))
    meta_class_info._original_init(self, *args, **kwargs)

    for name, ann in type(self).__annotations__.items():
        if not issubclass(ann, MetaMember):
            continue

        if hasattr(self, name):
            assert isinstance(getattr(self, name), ann)
        else:
            assert issubclass(ann, MetaMember)
            setattr(self, name, ann())

        obj: MetaMember = getattr(self, name)
        obj._meta_config_(self, name, *getattr(ann, "@meta_args"))


class MetaObject:
    def __init_subclass__(cls) -> None:
        original_init = cls.__init__
        setattr("@meta_class_info", _MetaClassInfo(original_init))
        cls.__init__ = _wrapped_init_
