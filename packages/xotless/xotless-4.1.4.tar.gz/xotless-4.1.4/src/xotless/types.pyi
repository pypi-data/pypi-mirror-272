import typing as t

from typing_extensions import Self

class TypeClass(t.Protocol):
    pass

class EqTypeClass(TypeClass, t.Protocol):
    def __eq__(self, other: t.Any, /) -> bool: ...
    def __ne__(self, other: t.Any, /) -> bool: ...

class OrdTypeClass(EqTypeClass, t.Protocol):
    def __le__(self, other: t.Any, /) -> bool: ...
    def __lt__(self, other: t.Any, /) -> bool: ...
    def __ge__(self, other: t.Any, /) -> bool: ...
    def __gt__(self, other: t.Any, /) -> bool: ...

T = t.TypeVar("T")
TEq = t.TypeVar("TEq", bound=EqTypeClass)
TOrd = t.TypeVar("TOrd", bound=OrdTypeClass)

@t.runtime_checkable
class Domain(t.Protocol[T]):
    @property
    def sample(self) -> t.Optional[T]:
        """Produces a value which is a member of the domain.

        Some non-empty domains cannot produce a sample.  For instance,
        `~xotless.domains.IntervalSet`:class: comprising only open ranges
        cannot produce a sample.  They return None.

        Different calls to `sample` should produce the same value.

        """
        ...

    def union(self: Self, *others: Self) -> Self:
        "Return a domain containing elements of `self` or `other`."
        ...

    def __contains__(self, which: T) -> bool:
        "Return True if `which` is a member."
        ...

    def __sub__(self: Self, other: Self) -> Self:
        "Return a domain containing elements of `self` which are not members of `other`."
        ...

    def __or__(self: Self, other: Self) -> Self:
        "Equivalent to `union`:meth:."
        ...

    def __le__(self: Self, other: Self) -> bool:
        "Return True if `self` is sub-set of `other`"
        ...

    def __lt__(self: Self, other: Self) -> bool:
        "Return True if `self` is a proper sub-set of `other`"
        ...

    def __ge__(self: Self, other: Self) -> bool:
        "Return True if `other` is a sub-set of `self`"
        ...

    def __gt__(self: Self, other: Self) -> bool:
        "Return True if `other` is a proper sub-set of `self`"
        ...

    def __and__(self: Self, other: Self) -> Self:
        "Return a domain containing common elements of `self` and `other`."
        ...

    def __bool__(self) -> bool:
        "Return True if the domain is not empty."
        ...
