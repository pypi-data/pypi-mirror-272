from pathlib import Path

from sh import infrable

from infrable import __version__

data = Path("tests/data")


def test_switch():
    infrable.switch.env.beta()
    assert infrable.switches(_tty_out=False).strip() == "env = beta"
    infrable.switch.env.prod()
    assert infrable.switches(_tty_out=False).strip() == "env = prod"
    infrable.switch.env.dev()
    assert infrable.switches(_tty_out=False).strip() == "env = dev"
