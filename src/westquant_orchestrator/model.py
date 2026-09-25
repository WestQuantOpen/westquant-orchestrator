from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class FrameworkDescriptor:
    framework: str
    package: str
    plugin_version: str
    native_version: str | None = None
    capabilities: tuple[str, ...] = ()
    status: str = "alpha"


@dataclass(frozen=True)
class FrameworkJob:
    job_id: str
    framework: str
    challenge_id: str
    runner: Callable[[], Any]
    metadata: dict[str, Any] = field(default_factory=dict)
