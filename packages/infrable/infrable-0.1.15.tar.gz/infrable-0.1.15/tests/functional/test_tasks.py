from sh import infrable

from infrable import __version__, init


def setup_module():
    init.init()


def test_tasks():
    assert "[TASK] Reload nginx" in infrable.nginx.reload("--help")
