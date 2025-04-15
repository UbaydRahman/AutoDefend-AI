import json
import boto3

# Initialize AWS clients in eu-west-2
dynamodb = boto3.client("dynamodb", region_name="eu-west-2")
bedrock_runtime = boto3.client("bedrock-runtime", region_name="eu-west-2")

# Function to retrieve logs from DynamoDB
def get_logs():
    response = dynamodb.scan(TableName="SecurityLogsTable", Limit=5)  # Retrieves 5 logs
    logs = []
    for item in response.get("Items", []):
        # Convert DynamoDB item to a standard dict
        logs.append({key: list(value.values())[0] for key, value in item.items()})
    return logs

# Function to send logs to AWS Bedrock for AI analysis
def analyze_logs_with_ai(logs):
    log_text = json.dumps(logs, indent=4)

    # AI prompt for threat analysis
    prompt = f"""
    You are a cybersecurity AI assistant analyzing security logs for potential threats.
    Review the following security logs and provide an analysis of possible attack patterns,
    risk levels, and recommended security actions.

    Logs:
    {log_text}

    Provide a concise summary report.
    """

    # Invoke the AWS Bedrock model
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-text-lite-v1",  # Use the model ID you have access to
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 500,
                "stopSequences": [],
                "temperature": 0.7
            }
        })
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    return response_body["results"][0]["outputText"]

# Function to automate security responses based on the AI analysis report
def automate_security_response(report):
    print("\n🚨 Evaluating AI Analysis Report for automated response...")
    # Example logic: if report mentions "brute force", simulate blocking IP addresses
    if "brute force" in report.lower():
        print("🚨 Automated Response: Detected brute force attack. Blocking associated IP addresses...")
        # Here you would integrate with AWS WAF or your firewall to block IPs
    elif "ransomware" in report.lower():
        print("🚨 Automated Response: Detected ransomware threat. Initiating system quarantine procedures...")
        # Here you would trigger automated quarantining of affected instances/resources
    else:
        print("✅ No immediate automated response required based on the current analysis.")

if __name__ == "__main__":
    logs = get_logs()
    if logs:
        print("🚀 Logs retrieved from DynamoDB. Sending to AWS Bedrock AI for analysis...")
        ai_response = analyze_logs_with_ai(logs)
        print("\n✅ AI Analysis Report:\n")
        print(ai_response)
        
        # Now, automatically trigger a simulated security response based on the AI analysis
        automate_security_response(ai_response)
    else:
        print("⚠️ No logs found in DynamoDB.")
