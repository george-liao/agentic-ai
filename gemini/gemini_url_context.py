from google import genai
from google.genai.types import Tool, GenerateContentConfig, HttpOptions, UrlContext

client = genai.Client(http_options=HttpOptions(api_version="v1"))
model_id = "gemini-2.5-pro"

url_context_tool = Tool(
    url_context = UrlContext
)

response = client.models.generate_content(
    model=model_id,
    contents="Summarize this document: https://www.singaporeair.com/en_UK/sg/faq/check-in/auto-check-in/",
    config=GenerateContentConfig(
        tools=[url_context_tool],
        response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# get URLs retrieved for context
print(response.candidates[0].url_context_metadata)
