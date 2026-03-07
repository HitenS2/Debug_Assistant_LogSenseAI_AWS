import boto3
import uuid

def ask_graph_agent(prompt, session_id):
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    
    AGENT_ID = '7Y7AY7L03L' 
    AGENT_ALIAS_ID = 'TSTALIASID' 

    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt,
        enableTrace=True # <--- Turn this on to see why it's blank
    )

    answer = ""
    for event in response.get("completion"):
        # 1. Look for the actual answer
        if "chunk" in event:
            data = event["chunk"]["bytes"].decode("utf-8")
            answer += data
        
        # 2. Look for errors in the trace
        if "trace" in event:
            # This prints the 'Thinking' process so you can see where it fails
            trace = event["trace"]["trace"]
            if "orchestrationTrace" in trace:
                print("--- AI is thinking... ---")
    
    return answer


# --- Simple Terminal Test for Integration ---
if __name__ == "__main__":
    # Generate a unique session ID for this chat
    graph_session = str(uuid.uuid4())

    print("--- Statistical Visualization Agent (Type 'exit' to stop) ---")
    print("Example: 'Show me a pie chart of my monthly expenses'")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        print("Agent is generating data and rendering plot...")
        result = ask_graph_agent(user_input, graph_session)
        
        # NOTE: In your terminal, you will see the Markdown code: ![Graph](URL)
        # In a real Frontend/UI, that Markdown will turn into the actual image!
        print(f"Agent: {result}\n")