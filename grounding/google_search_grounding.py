def generate_content() -> str:
    from google import genai
    from google.genai.types import (
        GenerateContentConfig,
        GoogleSearch,
        HttpOptions,
        Tool,
    )

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="What's latest share price of Google?",
        config=GenerateContentConfig(
            tools=[
                # Use Google Search Tool
                Tool(google_search=GoogleSearch())
            ],
        ),
    )

    print(response.text)

    return response.text


if __name__ == "__main__":
    generate_content()