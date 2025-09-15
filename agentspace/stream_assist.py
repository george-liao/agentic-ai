from google.cloud import discoveryengine_v1
from google.api_core.client_options import ClientOptions

# Update accordingly
project_id = "xxxxxxxxxxxx"  # Your GCP project ID
location = "global"          # Values: "global", "us", "eu"
engine_id = "xxxxxxxxxxxx"   # Your Discovery Engine ID
search_query = "what is agentic ai"


def sample_stream_assist(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
    session_id=None,
):

    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine_v1.AssistantServiceClient(client_options=client_options)

    if session_id is None:
        request = discoveryengine_v1.StreamAssistRequest(
            name=f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/assistants/default_assistant",
            query=discoveryengine_v1.types.Query(text=search_query),
        )

        stream = client.stream_assist(request=request)

        for response in stream:
            return_value = response
        
        return return_value # This contains the session_info

    else:
        request = discoveryengine_v1.StreamAssistRequest(
            name=f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/assistants/default_assistant",
            query=discoveryengine_v1.types.Query(text=search_query),
            session=session_id,
        )
        stream = client.stream_assist(request=request)
        
        for response in stream:
            return_value = response
        
        return return_value 

def main():
    print("Querying discovery engine...")
    print(f"1st search query: {search_query}")
    result = sample_stream_assist(project_id, location, engine_id, search_query)

    # session_id = result.session_info.session
    # print(f"Session ID: {session_id}")

if __name__ == "__main__":
   main()
