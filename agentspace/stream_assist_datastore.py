import time
from google.cloud import discoveryengine_v1
from google.api_core.client_options import ClientOptions

def stream_assist_query(query: str):
    
    project_id = "xxxx"  # Your GCP project ID
    location = "global"
    engine_id = "xxxx"  # Your Search Engine ID
    datastore_id = "xxxx"  # Your Datastore ID
    
    start_time = time.time()
    
    print(f"🎯 StreamAssist with datastore targeting for: '{query}'")
    
    try:
        # Client setup with timing
        client_start = time.time()
        client_options = (
            ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
            if location != "global"
            else None
        )
        client = discoveryengine_v1.AssistantServiceClient(client_options=client_options)
        client_time = time.time() - client_start
        
        # API request with datastore targeting
        api_start = time.time()
        
        # Create DataStoreSpec for targeting specific datastore
        data_store_spec = discoveryengine_v1.types.SearchRequest.DataStoreSpec(
            data_store=f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{datastore_id}"
        )
        
        # Create VertexAiSearchSpec with datastore targeting
        vertex_ai_search_spec = discoveryengine_v1.types.StreamAssistRequest.ToolsSpec.VertexAiSearchSpec(
            data_store_specs=[data_store_spec]  # This narrows search to specific datastore
        )
        
        # Create ToolsSpec with vertex_ai_search_spec
        tools_spec = discoveryengine_v1.types.StreamAssistRequest.ToolsSpec(
            vertex_ai_search_spec=vertex_ai_search_spec
        )
        
        # Create request with datastore targeting
        request = discoveryengine_v1.StreamAssistRequest(
            name=f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/assistants/default_assistant",
            query=discoveryengine_v1.types.Query(text=query),
            tools_spec=tools_spec  # This enables datastore targeting
        )
        
        # Stream responses
        stream = client.stream_assist(request=request)
        responses = []
        for response in stream:
            responses.append(response)
            
        api_time = time.time() - api_start
        total_time = time.time() - start_time
        
        return format_results(responses, total_time, client_time, api_time, datastore_id)
        
    except Exception as e:
        total_time = time.time() - start_time
        return f"❌ StreamAssist failed: {e}\n⏱️ Failed in {total_time:.3f}s"

def format_results(responses, total_time, client_time, api_time, datastore_id):
    """Format StreamAssist results with timing"""
    timing_text = f"⏱️ StreamAssist completed in {total_time:.3f}s (Client: {client_time:.3f}s, API: {api_time:.3f}s)"
    
    if not responses:
        return f"❓ No responses from targeted datastore\n{timing_text}"
    
    answer_parts = [
        f"🎯 StreamAssist found answer from targeted datastore '{datastore_id}':",
        timing_text,
        ""
    ]
    
    # Extract final answer from responses
    try:
        final_answer = None
        
        # Look through responses for the final answer
        for response in responses:
            response_str = str(response)
            
            # Look for meaningful answer text
            if 'text:' in response_str:
                text_parts = response_str.split('text:')
                for part in reversed(text_parts[1:]):
                    clean_text = part.split('\n')[0].strip(' "\'')
                    # Find the actual answer (not thinking process)
                    if (len(clean_text) > 15 and 
                        not clean_text.startswith('**') and 
                        not 'thinking' in clean_text.lower() and
                        not 'search' in clean_text.lower()):
                        final_answer = clean_text
                        break
                        
        if final_answer:
            answer_parts.append(f"💬 AI Answer: {final_answer}")
            answer_parts.append("")
            answer_parts.append(f"✅ Search narrowed to datastore: {datastore_id}")
        else:
            answer_parts.append(f"📝 Processed {len(responses)} targeted responses")
            
    except Exception as e:
        answer_parts.append(f"❌ Failed to extract answer: {e}")
    
    return "\n".join(answer_parts)

if __name__ == "__main__":
    print("=== StreamAssist with Datastore Targeting ===")
    print("Using vertex_ai_search_spec.data_store_specs for precise targeting")
    
    # Example query - you can change this to any question
    query = "What does Yellow flashing LED mean on Dyson Supersonic r?"
    result = stream_assist_query(query)
    print(result)