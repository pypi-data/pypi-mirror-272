from dataclasses import asdict, dataclass, field

from sh import Command, ssh
from typer import Typer

from infrable.meta import Meta
from infrable.utils import format_item


@dataclass(unsafe_hash=True, order=True, eq=True)
class Host:
    """A generic host in the infrastructure."""

    ip: str  # The only required field

    fqdn: str | None = None
    admin: str = "root"
    meta: Meta = field(default_factory=Meta)
    typer: Typer | None = None

    def remote(self, login=None) -> Command:
        login = login or self.admin
        address = f"{login}@{self.ip}"
        return ssh.bake(address, "-o", "StrictHostKeyChecking=no")

    def format(self, name: str, format: str) -> str:
        return format_item(format).render(name=name, **asdict(self))

    def __str__(self) -> str:
        host = self.fqdn or self.ip
        return f"{self.admin}@{host}"
