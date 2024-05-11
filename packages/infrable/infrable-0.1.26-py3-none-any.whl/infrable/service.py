from dataclasses import asdict, dataclass, field

from typer import Typer

from infrable.host import Host
from infrable.meta import Meta
from infrable.utils import format_item


@dataclass(unsafe_hash=True, order=True, eq=True)
class Service:
    """A generic service, maybe running on a host."""

    host: Host | None = None
    port: int | None = None
    meta: Meta = field(default_factory=Meta)
    typer: Typer | None = None

    def format(self, name: str, format: str) -> str:
        return format_item(format).render(name=name, **asdict(self))

    def __str__(self) -> str:
        return f'{self.host or ""}:{self.port or ""}'
