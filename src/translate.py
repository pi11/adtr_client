from requests import Session

def translate(
    user_id: int, api_key: str, text: str, target_language: str = "russian"
) -> str:
    """
    Translate text to the specified target language.

    Args:
        user_id: User ID from rkn.name service
        api_key: Api key from rkn.name service
        text (str): Text to translate (max 300 characters)
        target_language (str, optional): Target language for translation. Defaults to "russian".

    Returns:
        str: translated text

    Raises:
        requests.exceptions.HTTPError: If the API returns an error
        ValueError: If input validation fails
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")

    if len(text) > 300:
        raise ValueError("Text must be 300 characters or less")

    base_url = "https://adtr.webnova.one"
    endpoint = f"{base_url}/translate"

    payload = {
        "user_id": user_id,
        "api_key": api_key,
        "text": text,
        "target_language": target_language,
    }

    session = Session()
    response = session.post(endpoint, json=payload)

    response.raise_for_status()

    data = response.json()
    return data["result"]
