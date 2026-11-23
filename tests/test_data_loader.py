import pytest
import requests

from modules import data_loader


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(data_loader.time, "sleep", lambda _: None)


class FakeResponse:
    def __init__(self, content: bytes, status_code: int = 200):
        self.content = content
        self.status_code = status_code

    @property
    def text(self) -> str:
        return self.content.decode()

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")


def test_download_csv_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **k: FakeResponse(b"a,b\n1,2\n"))
    out = tmp_path / "out.csv"

    data_loader.download_csv("http://exemple", str(out))

    assert out.read_bytes() == b"a,b\n1,2\n"


def test_download_csv_raises_runtime_error_after_retries(tmp_path, monkeypatch):
    calls = []

    def fail(*args, **kwargs):
        calls.append(1)
        raise requests.ConnectionError("panne")

    monkeypatch.setattr(requests, "get", fail)
    out = tmp_path / "out.csv"

    with pytest.raises(RuntimeError, match="Téléchargement impossible") as exc_info:
        data_loader.download_csv("http://exemple", str(out), retries=3)

    assert len(calls) == 3
    assert isinstance(exc_info.value.__cause__, requests.ConnectionError)
    assert not out.exists()


def test_download_csv_rejects_json_error_payload(tmp_path, monkeypatch):
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: FakeResponse(b'{"error": true}')
    )

    with pytest.raises(RuntimeError):
        data_loader.download_csv("http://exemple", str(tmp_path / "out.csv"))


def test_download_csv_retries_on_http_error_then_succeeds(tmp_path, monkeypatch):
    responses = iter([FakeResponse(b"", 429), FakeResponse(b"a\n1\n")])
    monkeypatch.setattr(requests, "get", lambda *a, **k: next(responses))
    out = tmp_path / "out.csv"

    data_loader.download_csv("http://exemple", str(out))

    assert out.read_bytes() == b"a\n1\n"
