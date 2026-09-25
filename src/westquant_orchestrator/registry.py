from __future__ import annotations
from .model import FrameworkDescriptor


class FrameworkRegistry:
    def __init__(self) -> None:
        self._items: dict[str, FrameworkDescriptor] = {}

    def register(self, descriptor: FrameworkDescriptor) -> None:
        if descriptor.framework in self._items:
            raise ValueError(f"framework already registered: {descriptor.framework}")
        self._items[descriptor.framework] = descriptor

    def get(self, framework: str) -> FrameworkDescriptor:
        return self._items[framework]

    def list(self) -> list[FrameworkDescriptor]:
        return [self._items[k] for k in sorted(self._items)]
