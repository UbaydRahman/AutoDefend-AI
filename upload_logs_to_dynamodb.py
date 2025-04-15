import json
import boto3
import time

# Initialize DynamoDB client in eu-west-2
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table("SecurityLogsTable")

# Load the synthetic logs from JSON file
with open("synthetic_security_logs.json", "r") as f:
    logs = json.load(f)

# Batch write to DynamoDB (25 items per request is the limit)
def batch_write(logs):
    with table.batch_writer() as batch:
        for i, log in enumerate(logs):
            batch.put_item(Item=log)
            # Print progress every 1000 logs
            if (i + 1) % 1000 == 0:
                print(f"✅ Uploaded {i+1} logs...")

# Start the upload process
print("🚀 Uploading logs to DynamoDB...")
batch_write(logs)
print("✅ All logs successfully uploaded to DynamoDB!")
