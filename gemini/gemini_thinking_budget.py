def generate_content() -> str:
    from google import genai
    from google.genai.types import GenerateContentConfig, ThinkingConfig

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="solve x^2 + 4x + 4 = 0",
        config=GenerateContentConfig(
            thinking_config=ThinkingConfig(
                # thinking_budget=8192,  
                thinking_budget=128,  # min 128 for pro and 1 for flash
            )
        ),
    )

    print(response.text)

    # Token count for `Thinking`
    print(response.usage_metadata.thoughts_token_count)

    # Total token count
    print(response.usage_metadata.total_token_count)
 
    return response.text


if __name__ == "__main__":
    generate_content()