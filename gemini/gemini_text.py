def generate_content() -> str:
    from google import genai
    from google.genai.types import HttpOptions

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Summarize agentic ai in less than 100 words.",
    )
    print(response.text)

    return response.text


if __name__ == "__main__":
    generate_content()