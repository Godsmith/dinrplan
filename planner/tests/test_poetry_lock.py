from pathlib import Path


def test_poetry_lock_does_not_contain_psycopg2():
    poetry_lock = (Path(__file__).parent.parent.parent / "poetry.lock").read_text()
    assert 'name = "psycopg2"' not in poetry_lock, (
        "Please remove the psycopg2 package from poetry.lock manually, as it will otherwise break new installs. "
        "psycopg2-binary is enough."
    )
