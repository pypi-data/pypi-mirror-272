from __future__ import annotations

import typing
from typing import Generic, TypeVar, TypeVarTuple

TemplateArgs = TypeVar("TemplateArgs")


class Template(Generic[TemplateArgs]):
    _template_args: TemplateArgs

    @classmethod
    def _template_arg_transform_(cls, args) -> TemplateArgs:
        return args

    @classmethod
    def _template_instantiate_(cls, args):
        raise AssertionError("abstract function called")

    def __class_getitem__(cls, args):
        if cls is Template:
            print()

        args = cls._template_arg_transform_(args)
        ...

    ...


class MyArgs:
    def __init__(self, width, t):
        self.width = width
        self.t = t


class MyTemplate(Template[MyArgs]):
    @classmethod
    def _template_arg_transform_(cls, args):
        return

    @classmethod
    def _template_instantiate_(cls):
        ...

    ...
