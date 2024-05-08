from __future__ import annotations
from typing import TYPE_CHECKING
import ctypes as ct
from .lib import gsf, c_str, c_str_or, py_str
if TYPE_CHECKING:
    from .context import Context
    from .data import Class


class classproperty(property):
    def __get__(self, obj, obj_type=None):
        return super().__get__(obj_type)


class Typing:
    def __init__(self, handle, const: bool = True, *, own: bool = False) -> None:
        self.handle = ct.c_void_p(handle)
        self._const = const and not own
        self._own = own

    @classmethod
    def new(cls, context: Context, type_amount: int) -> Typing:
        return Typing(gsf.typing_new(context.handle, ct.c_size_t(type_amount)), own=True)

    def __del__(self) -> None:
        if self._own:
            gsf.delete_typing[None](self.handle)

    def __str__(self) -> str:
        return Typing.to_string(self)

    @classmethod
    def from_string(cls, string: str, ctx: Context | None) -> Typing:
        result = Typing(gsf.create_typing(), own=True)
        gsf.typing_from_string(result.handle, c_str(string), ctx.handle)
        return result

    @classmethod
    def to_string(cls, typing: Typing, max_size: int = 128) -> str:
        return py_str(gsf.typing_to_string[ct.c_char_p](typing.handle))

    @property
    def context(self) -> Context:
        return Context(gsf.typing_get_context(self.handle))

    @property
    def type_amount(self) -> int:
        return gsf.typing_types_amount[ct.c_size_t](self.handle)

    def add_type(self, type_: Type | str) -> Type:
        return Type(gsf.typing_add_type(self.handle, c_str_or(type_, lambda t: t.handle)))

    def get_type(self, index: int) -> Type:
        return Type(gsf.typing_get_type(self.handle, ct.c_size_t(index)))

    @property
    def default(self) -> Type:
        return Type(gsf.typing_get_default(self.handle))

    def set_default(self, index: int) -> Type:
        return Type(gsf.typing_set_default(self.handle, ct.c_size_t(index)))

    def reset_default(self) -> None:
        gsf.typing_reset_default(self.handle)

    def remove_type(self, index: int) -> None:
        gsf.typing_remove_type(self.handle, ct.c_size_t(index))

    def matches_type(self, preset: Type) -> Type | None:
        result = gsf.typing_matching_type(self.handle, preset.handle)
        return Type(result) if result else None


class Type:
    def __init__(self, handle, const: bool = True, *, own: bool = False) -> None:
        self.handle = ct.c_void_p(handle)
        self._const = const and not own
        self._own = own

    def __del__(self) -> None:
        if self._own:
            gsf.delete_type[None](self.handle)

    def __str__(self) -> str:
        return Type.to_string(self)

    @classmethod
    def from_string(cls, string: str, ctx: Context | None) -> Type:
        result = Type(gsf.create_typing(), own=True)
        gsf.type_from_string(result.handle, c_str(string), ctx.handle)
        return result

    @classmethod
    def to_string(cls, type_: Type, max_size: int = 128) -> str:
        string = ' ' * max_size
        return py_str(gsf.type_to_string[ct.c_char_p](c_str(string), max_size, type_.handle))

    @classproperty
    def i8(cls) -> Type:
        return Type(gsf.get_type_i8())

    @classproperty
    def i16(cls) -> Type:
        return Type(gsf.get_type_i16())

    @classproperty
    def i32(cls) -> Type:
        return Type(gsf.get_type_i32())

    @classproperty
    def i64(cls) -> Type:
        return Type(gsf.get_type_i64())

    @classproperty
    def u8(cls) -> Type:
        return Type(gsf.get_type_u8())

    @classproperty
    def u16(cls) -> Type:
        return Type(gsf.get_type_u16())

    @classproperty
    def u32(cls) -> Type:
        return Type(gsf.get_type_u32())

    @classproperty
    def u64(cls) -> Type:
        return Type(gsf.get_type_u64())

    @classproperty
    def f32(cls) -> Type:
        return Type(gsf.get_type_f32())

    @classproperty
    def f64(cls) -> Type:
        return Type(gsf.get_type_f64())

    @classproperty
    def str(cls) -> Type:
        return Type(gsf.get_type_str())

    @classmethod
    def new_array(cls, element: Type | str, ctx: Context | None) -> Type:
        result = gsf.create_type()
        return Type(gsf.type_init_array(result, c_str_or(element, lambda t: t.handle), ctx.handle if ctx else None), own=True)

    @classmethod
    def new_list(cls, element: Typing | str, ctx: Context | None) -> Type:
        result = gsf.create_type()
        return Type(gsf.type_init_list(result, c_str_or(element, lambda t: t.handle), ctx.handle if ctx else None), own=True)

    @classmethod
    def new_map(cls, element: Typing | str, ctx: Context | None) -> Type:
        result = gsf.create_type()
        return Type(gsf.type_init_map(result, c_str_or(element, lambda t: t.handle), ctx.handle if ctx else None), own=True)

    @classmethod
    def new_object(cls, class_: Class) -> Type:
        result = gsf.create_type()
        return Type(gsf.type_init_object(result, class_.handle), own=True)

    def matches(self, preset: Type, strict: bool = False) -> bool:
        func = gsf.type_matches
        if strict:
            func = gsf.type_matches_strict
        return func(self.handle, preset.handle)

    def is_primitive(self) -> bool:
        return gsf.type_is_primitive[ct.c_bool](self.handle)

    def is_string(self) -> bool:
        return gsf.type_is_string[ct.c_bool](self.handle)

    def is_scalar(self) -> bool:
        return gsf.type_is_scalar[ct.c_bool](self.handle)

    def is_int(self) -> bool:
        return gsf.type_is_int[ct.c_bool](self.handle)

    def is_uint(self) -> bool:
        return gsf.type_is_uint[ct.c_bool](self.handle)

    def is_float(self) -> bool:
        return gsf.type_is_primitive[ct.c_bool](self.handle)

    def is_non_primitive(self) -> bool:
        return gsf.type_is_non_primitive[ct.c_bool](self.handle)

    def is_collection(self) -> bool:
        return gsf.type_is_collection[ct.c_bool](self.handle)

    def is_array(self) -> bool:
        return gsf.type_is_array[ct.c_bool](self.handle)

    def is_list(self) -> bool:
        return gsf.type_is_list[ct.c_bool](self.handle)

    def is_map(self) -> bool:
        return gsf.type_is_map[ct.c_bool](self.handle)

    def is_object(self) -> bool:
        return gsf.type_is_object[ct.c_bool](self.handle)

    def get_element_type(self) -> Type:
        return Type(gsf.type_get_element_type(self.handle))

    def get_element_typing(self) -> Typing:
        return Typing(gsf.type_get_element_typing(self.handle))

    def get_object_class(self) -> Class:
        return Class(gsf.type_get_object_class(self.handle))
