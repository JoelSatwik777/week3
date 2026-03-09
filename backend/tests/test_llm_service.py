import pytest

from backend.services import llm_service
from backend.config.settings import get_settings


def test_truncate_does_not_cut_mid_line() -> None:
    # create a string longer than limit with multiple lines
    limit = get_settings().llm_max_chars
    assert limit > 0

    lines = ["first line"]
    # make a very long line that will definitely exceed the limit
    lines.append("a" * (limit + 50))
    text = "\n".join(lines)

    truncated = llm_service._truncate(text)
    # the truncated text should not include any of the overflowing a's
    assert "a" * (limit // 2) not in truncated
    # should end at or before a newline boundary
    assert not truncated.endswith("a")
    assert truncated.endswith("first line")


def test_normalize_bullet_report_strips_various_markers() -> None:
    sample = (
        "Summary of Portfolio:\n"
        "1. high churn in west\n"
        "2) older customers churn more\n"
        "- low turnover in east\n"
        "• some other point\n"
        "Final line"
    )
    normalized = llm_service._normalize_bullet_report(sample)
    # each meaningful line should begin with a dash after normalization
    for line in normalized.splitlines():
        assert line.startswith("- ") or line.endswith(":")
    # the heading should be preserved
    assert "Summary of Portfolio:" in normalized


@pytest.mark.parametrize("normalize", [True, False])
def test_call_ollama_accepts_normalize_flag(monkeypatch, normalize):
    # stub out requests.post to avoid real network calls
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "one\ntwo\n"}

    def fake_post(url, json, stream, options, timeout):
        return DummyResponse()

    monkeypatch.setattr(llm_service.requests, "post", fake_post)
    text = llm_service._call_ollama("prompt", normalize=normalize)
    if normalize:
        # normalization adds leading '- '
        assert text.strip().startswith("- one")
    else:
        assert text == "one\ntwo"


def test_default_token_limit_is_reasonable():
    # make sure the configuration default can't easily starve the model
    settings = get_settings()
    assert settings.llm_num_predict >= 200
