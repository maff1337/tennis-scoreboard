from collections.abc import Callable
from typing import Any, TypeVar, get_origin, get_type_hints

from tennis_scoreboard.exceptions import DIError

T = TypeVar('T')
_MARK = '__injectable__'


def inject(cls: type[T]) -> type[T]:
    setattr(cls, _MARK, True)
    return cls


class Container:
    def __init__(self) -> None:
        self._providers: dict[type, Callable[[], Any]] = {}
        self._resolving: list[type] = []

    def bind(self, abstract: type, impl: type) -> None:
        self._providers[abstract] = lambda: self._build(impl)

    def bind_instance(self, abstract: type, instance: Any) -> None:
        self._providers[abstract] = lambda: instance

    def resolve(self, key: type[T]) -> T:
        key = get_origin(key) or key

        if key in self._providers:
            return self._providers[key]()

        if getattr(key, _MARK, False):
            return self._build(key)

        raise DIError(f'No binding for {key!r}')

    def _build(self, cls: type[T]) -> T:
        if cls in self._resolving:
            chain = ' -> '.join(c.__name__ for c in [*self._resolving, cls])
            raise DIError(f'Circular dependency: {chain}')

        if cls.__init__ is object.__init__:
            return cls()

        self._resolving.append(cls)

        try:
            hints = get_type_hints(cls.__init__)
            hints.pop('return', None)
            return cls(**{name: self.resolve(tp) for name, tp in hints.items()})
        finally:
            self._resolving.pop()
