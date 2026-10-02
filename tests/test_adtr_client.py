import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from adtr_client import synonymize, translate


@patch("adtr_client.Session")
def test_translate_sends_explicit_language_direction(session_class):
    response = Mock()
    response.json.return_value = {"result": "result"}
    session_class.return_value.post.return_value = response

    result = translate(
        user_id=123,
        api_key="key",
        text="title",
        source_language="en",
        target_language="ru",
    )

    assert result == "result"
    session_class.return_value.post.assert_called_once_with(
        "https://aitr.webnova.one/translate",
        json={
            "user_id": 123,
            "api_key": "key",
            "text": "title",
            "source_language": "en",
            "target_language": "ru",
        },
        timeout=45,
    )


@patch("adtr_client.Session")
def test_translate_defaults_to_source_language_auto(session_class):
    response = Mock()
    response.json.return_value = {"result": "result"}
    session_class.return_value.post.return_value = response

    translate(123, "key", "title", "en", 12, False)

    payload = session_class.return_value.post.call_args.kwargs["json"]
    assert payload["source_language"] == "Auto"
    assert payload["target_language"] == "en"
    assert session_class.return_value.post.call_args.kwargs["timeout"] == 12


@patch("adtr_client.Session")
def test_translate_includes_api_error_detail(session_class):
    response = Mock()
    response.raise_for_status.side_effect = HTTPError(
        "502 Server Error", response=response
    )
    response.json.return_value = {
        "detail": "Translation provider returned invalid output after retry"
    }
    session_class.return_value.post.return_value = response

    with pytest.raises(HTTPError, match="invalid output after retry"):
        translate(123, "key", "title", target_language="en")


@patch("adtr_client.Session")
def test_translate_accepts_limit_and_sends_context(session_class):
    response = Mock()
    response.json.return_value = {"result": "translated"}
    session_class.return_value.post.return_value = response

    result = translate(123, "key", "x" * 50_000, context="  An adult flash game  ")

    assert result == "translated"
    payload = session_class.return_value.post.call_args.kwargs["json"]
    assert len(payload["text"]) == 50_000
    assert payload["context"] == "An adult flash game"


def test_translate_rejects_text_over_limit():
    with pytest.raises(ValueError, match="50000 characters"):
        translate(123, "key", "x" * 50_001)


@pytest.mark.parametrize("context", [" ", "x" * 1_001])
def test_translate_rejects_invalid_context(context):
    with pytest.raises(ValueError, match="Context must be"):
        translate(123, "key", "title", context=context)


@patch("adtr_client.Session")
def test_synonymize_sends_context(session_class):
    response = Mock()
    response.json.return_value = {"result": "rewritten"}
    session_class.return_value.post.return_value = response

    result = synonymize(123, "key", "title", context="An adult game")

    assert result == "rewritten"
    payload = session_class.return_value.post.call_args.kwargs["json"]
    assert payload["context"] == "An adult game"
