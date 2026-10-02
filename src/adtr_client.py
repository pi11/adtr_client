from typing import Optional

from requests import Session
from requests.exceptions import HTTPError

MAX_TRANSLATION_LENGTH = 50_000
MAX_CONTEXT_LENGTH = 1_000


def _raise_for_status(response, verbose: bool) -> None:
    """Raise an HTTP error that includes a safe API-provided detail message."""
    try:
        response.raise_for_status()
    except HTTPError as exc:
        detail = None
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail")
        except (TypeError, ValueError):
            pass

        if verbose:
            print(f"[DEBUG] Error occurred: {exc}")
            print(f"[DEBUG] Response content: {response.text}")

        if isinstance(detail, str) and detail.strip():
            raise HTTPError(
                f"{exc} - API detail: {detail.strip()}",
                response=response,
                request=getattr(response, "request", None),
            ) from exc
        raise


def translate(
    user_id: int,
    api_key: str,
    text: str,
    target_language: str = "russian",
    timeout: int = 45,
    verbose: bool = False,
    source_language: str = "Auto",
    context: Optional[str] = None,
) -> str:
    """
    Translate text to the specified target language.

    Args:
        user_id: User ID from rkn.name service
        api_key: Api key from rkn.name service
        text (str): Text to translate (max 50,000 characters)
        target_language (str, optional): Target language for translation. Defaults to "russian".
        timeout (int, optional): Request timeout in seconds. Defaults to 45.
        verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        source_language (str, optional): Source language name or code. Defaults to automatic detection.
        context (str, optional): Background about the content or medium, up to 1,000 characters.

    Returns:
        str: translated text

    Raises:
        requests.exceptions.HTTPError: If the API returns an error
        ValueError: If input validation fails
    """
    if verbose:
        print(f"[DEBUG] Starting translation request")
        print(
            "[DEBUG] Parameters: "
            f"text length={len(text)}, source_language={source_language}, "
            f"target_language={target_language}"
        )

    if not text.strip():
        if verbose:
            print(f"[DEBUG] Error: Empty text provided")
        raise ValueError("Text cannot be empty")

    if len(text) > MAX_TRANSLATION_LENGTH:
        if verbose:
            print(f"[DEBUG] Error: Text exceeds maximum length ({MAX_TRANSLATION_LENGTH} characters)")
        raise ValueError(f"Text must be {MAX_TRANSLATION_LENGTH} characters or less")

    if context is not None:
        context = context.strip()
        if not context or len(context) > MAX_CONTEXT_LENGTH:
            raise ValueError(f"Context must be 1-{MAX_CONTEXT_LENGTH} characters")

    base_url = "https://aitr.webnova.one"
    endpoint = f"{base_url}/translate"

    payload = {
        "user_id": user_id,
        "api_key": api_key,
        "text": text,
        "source_language": source_language,
        "target_language": target_language,
    }
    if context is not None:
        payload["context"] = context

    if verbose:
        print(f"[DEBUG] Endpoint: {endpoint}")
        print(f"[DEBUG] Payload: {payload}")

    session = Session()

    if verbose:
        print(f"[DEBUG] Sending POST request")

    response = session.post(endpoint, json=payload, timeout=timeout)

    if verbose:
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Response headers: {response.headers}")

    _raise_for_status(response, verbose)

    data = response.json()

    if verbose:
        print(f"[DEBUG] Response data: {data}")
        print(f"[DEBUG] Translation completed successfully")

    return data["result"]


def synonymize(
    user_id: int,
    api_key: str,
    text: str,
    timeout: int = 45,
    verbose: bool = False,
    context: Optional[str] = None,
) -> str:
    """
    Synonymize adult text

    Args:
        user_id: User ID from rkn.name service
        api_key: Api key from rkn.name service
        text (str): Text to synonymize (max 300 characters)
        timeout (int, optional): Request timeout in seconds. Defaults to 45.
        verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        context (str, optional): Background about the content or medium, up to 1,000 characters.

    Returns:
        str: synonymized text

    Raises:
        requests.exceptions.HTTPError: If the API returns an error
        ValueError: If input validation fails
    """
    if verbose:
        print(f"[DEBUG] Starting synonymization request")
        print(f"[DEBUG] Parameters: text length={len(text)}")

    if not text.strip():
        if verbose:
            print(f"[DEBUG] Error: Empty text provided")
        raise ValueError("Text cannot be empty")

    if len(text) > 300:
        if verbose:
            print(f"[DEBUG] Error: Text exceeds maximum length (300 characters)")
        raise ValueError("Text must be 300 characters or less")

    if context is not None:
        context = context.strip()
        if not context or len(context) > MAX_CONTEXT_LENGTH:
            raise ValueError(f"Context must be 1-{MAX_CONTEXT_LENGTH} characters")

    base_url = "https://aitr.webnova.one"
    endpoint = f"{base_url}/synonymize"

    payload = {
        "user_id": user_id,
        "api_key": api_key,
        "text": text,
    }
    if context is not None:
        payload["context"] = context

    if verbose:
        print(f"[DEBUG] Endpoint: {endpoint}")
        print(f"[DEBUG] Payload: {payload}")

    session = Session()

    if verbose:
        print(f"[DEBUG] Sending POST request")

    response = session.post(endpoint, json=payload, timeout=timeout)

    if verbose:
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Response headers: {response.headers}")

    _raise_for_status(response, verbose)

    data = response.json()

    if verbose:
        print(f"[DEBUG] Response data: {data}")
        print(f"[DEBUG] Synonymization completed successfully")

    return data["result"]
