from sh import infrable

from infrable import __version__, init


def setup_module():
    init.init()


def test_workflows():
    assert "[WORKFLOW] Deploy nginx files" in infrable.deploy.nginx("--help")
