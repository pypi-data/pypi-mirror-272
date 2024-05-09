import shutil
from pathlib import Path

from sh import infrable

from infrable import __version__, init, paths

data = Path("tests/data")


def gen_old_files(copy: bool):
    for new in paths.files.glob("**/*.new"):
        old = (paths.files / new.relative_to(paths.files)).with_suffix(".old")
        text = new.read_text() if copy else ""
        old.write_text(text)


def gen_test_data():
    infrable.files.gen(_out=data.joinpath("pre_files_gen"))
    infrable.files.gen(_out=data.joinpath("post_files_gen"))
    gen_old_files(copy=False)
    infrable.files.diff(_out=data.joinpath("files_diff"))


def setup_module():
    infrable.switch.env.dev()
    # gen_test_data()
    init.init()


def test_files_gen():
    shutil.rmtree(paths.files, ignore_errors=True)
    assert (
        infrable.files.gen(_tty_out=False) == data.joinpath("pre_files_gen").read_text()
    )
    assert (
        infrable.files.gen(_tty_out=False)
        == data.joinpath("post_files_gen").read_text()
    )


def test_files_diff():
    shutil.rmtree(paths.files, ignore_errors=True)
    infrable.files.gen()
    gen_old_files(copy=True)
    assert infrable.files.diff(_tty_out=False) == ""
    gen_old_files(copy=False)
    assert (
        infrable.files.diff(_tty_out=False) == data.joinpath("files_diff").read_text()
    )


def test_files_backup():
    infrable.files.gen()
    gen_old_files(copy=False)
    backups_count = len(list(paths.backups.glob("*")))
    out = infrable.files.backup(_tty_out=False)
    assert out.strip().startswith(f"backup: {paths.backups}/")
    assert len(list(paths.backups.glob("*"))) == backups_count + 1


# def test_files_revert():
#     infrable.files.gen()
#     gen_old_files(copy=False)
#     infrable.files.backup()  # <-- this fails for some reason
#
#     news1, olds1 = [f.read_text() for f in paths.files.glob("**/*.new")], [
#         f.read_text() for f in paths.files.glob("**/*.old")
#     ]
#
#     out = infrable.files.revert(_tty_out=False)
#     assert out.strip().startswith(f"reverting from: {paths.backups}/")
#
#     news2, olds2 = [f.read_text() for f in paths.files.glob("**/*.new")], [
#         f.read_text() for f in paths.files.glob("**/*.old")
#     ]
#
#     assert news1 == olds2
#     assert olds1 == news2


def test_files_affect_hosts():
    infrable.files.gen()
    gen_old_files(copy=True)
    assert infrable.files("affected-hosts", _tty_out=False) == ""
    gen_old_files(copy=False)
    assert (
        infrable.files("affected-hosts", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="dev_host", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="dev.example.com", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="127.0.0.1", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="managed_hosts", _tty_out=False).strip()
        == "root@dev.example.com"
    )
    assert (
        infrable.files("affected-hosts", only="prod_host", _tty_out=False).strip() == ""
    )
