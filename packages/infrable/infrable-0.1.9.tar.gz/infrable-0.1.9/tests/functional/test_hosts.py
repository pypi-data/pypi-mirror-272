from pathlib import Path

from sh import infrable

from infrable import __version__, init

data = Path("tests/data")


def gen_test_data():
    infrable.hosts(_out=data.joinpath("hosts"))
    infrable.hosts(repr=True, _out=data.joinpath("hosts_repr"))
    infrable.hosts(format="{name},{ip},{fqdn}", _out=data.joinpath("hosts_format"))


def setup_module():
    infrable.switch.env.dev()
    # gen_test_data()
    init.init()


def test_hosts():
    assert infrable.hosts(_tty_out=False) == data.joinpath("hosts").read_text()
    assert (
        infrable.hosts(repr=True, _tty_out=False)
        == data.joinpath("hosts_repr").read_text()
    )
    assert (
        infrable.hosts(format="{name},{ip},{fqdn}", _tty_out=False)
        == data.joinpath("hosts_format").read_text()
    )
