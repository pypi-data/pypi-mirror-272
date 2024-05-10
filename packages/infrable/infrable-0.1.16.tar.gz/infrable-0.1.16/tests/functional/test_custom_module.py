from sh import infrable

from infrable import __version__, init


def setup_module():
    init.init()


def test_custom_module():
    assert "[WORKFLOW] Provision Ubuntu host" in infrable.cloud(
        "provision-ubuntu-host", "--help"
    )
