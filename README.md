# Adtr Translation Client

A simple Python client for the [Adtr Translation API](https://aitr.webnova.one/docs).

## Installation

Install the client using pip:

```bash
pip install adtr_client
```

## Usage

Use the client to translate or creatively rewrite text via the Adtr Translation API.
The API accepts several languages, with English-to-Russian and Russian-to-English
as the primary translation directions.

### Translate English to Russian

```python
from adtr_client import translate

result = translate(
    user_id=123,
    api_key="your_api_key",
    text="English title to translate",
    source_language="en",
    target_language="ru",
)

print(result)
```

Use `source_language="Auto"` (the default) when the source language should be
detected automatically. Existing calls that only provide `target_language`
continue to work.
Translation text can be up to 50,000 characters. For long descriptions, set a
larger `timeout` if needed because the API translates them in smaller sections.

Pass optional `context` to identify the medium or subject without including it
in the translated result:

```python
result = translate(
    user_id=123,
    api_key="your_api_key",
    text="Game title to translate",
    target_language="ru",
    context="This is the title of an adult flash game",
)
```

`context` also works with `synonymize`; its title limit remains 300 characters.

### Translate Russian to English

```python
from adtr_client import translate

result = translate(
    user_id=123,
    api_key="your_api_key",
    text="Текст для перевода",
    source_language="ru",
    target_language="en",
)

print(result)
```

### Creatively rewrite in the same language

```python
from adtr_client import synonymize

result = synonymize(
    user_id=123,
    api_key="your_api_key",
    text="Text to rewrite",
)

print(result)
```

## Configuration

1. Obtain your `user_id` and `api_key` from the rkn.name service
2. Replace the example credentials and text with your own values.
