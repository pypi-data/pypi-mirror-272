from pathlib import Path

from sh import infrable

from infrable import __version__, init

data = Path("tests/data")


def setup_module():
    infrable.switch.env.dev()
    init.init()


def test_switch():
    assert infrable.switches(_tty_out=False).strip() == "env = dev"
    infrable.switch.env.beta()
    assert infrable.switches(_tty_out=False).strip() == "env = beta"
    infrable.switch.env.prod()
    assert infrable.switches(_tty_out=False).strip() == "env = prod"
