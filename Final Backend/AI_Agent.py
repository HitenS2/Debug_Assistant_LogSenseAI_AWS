import boto3
import uuid

def ask_log_agent(prompt, session_id):
    # 1. Connect to the Bedrock Agent Runtime
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

    # 2. These are the IDs from your AWS Console
    # Find these on the "Agent details" page
    #Masking IDs
    AGENT_ID = 'GLXXXXXXXXX' 
    AGENT_ALIAS_ID = 'TSXXXXXXX' # Or your specific Alias ID

    # 3. Call the Agent
    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt
    )

    # 4. The Agent sends back a "stream" of data. We need to collect it.
    answer = ""
    for event in response.get("completion"):
        if "chunk" in event:
            data = event["chunk"]["bytes"].decode("utf-8")
            answer += data
    
    return answer

# --- Main Program ---
# Generate a unique session ID for this chat
my_session = str(uuid.uuid4())

print("--- Log Analysis Agent (Type 'exit' to stop) ---")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    
    print("Thinking...")
    result = ask_log_agent(user_input, my_session)
    print(f"Agent: {result}\n")
