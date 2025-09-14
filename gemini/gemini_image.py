def generate_content() -> str:
    from google import genai
    from google.genai.types import GenerateContentConfig, Modality
    from PIL import Image
    from io import BytesIO

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=("A photorealistic image of a classic motorcycle parked on a city street."),
        config=GenerateContentConfig(
            response_modalities=[Modality.TEXT, Modality.IMAGE],
            candidate_count=1,
            safety_settings=[
                {"method": "PROBABILITY"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT"},
                {"threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.text:
            print(part.text)
        elif part.inline_data:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save("motorcycle.png")
    return True


if __name__ == "__main__":
    generate_content()