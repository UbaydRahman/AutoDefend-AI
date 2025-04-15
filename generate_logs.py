import json
import random
from faker import Faker

fake = Faker()
log_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
threat_types = ["Brute Force Attack", "SQL Injection", "Phishing Attempt", "Malware Infection", "Ransomware Attack"]

def generate_logs(num_logs=15000):
    logs = []
    for _ in range(num_logs):
        log = {
            "log_id": fake.uuid4(),
            "timestamp": fake.iso8601(),
            "log_level": random.choice(log_levels),
            "source_ip": fake.ipv4(),
            "destination_ip": fake.ipv4(),
            "username": fake.user_name(),
            "threat_type": random.choice(threat_types),
            "message": fake.sentence(),
        }
        logs.append(log)
    return logs

if __name__ == "__main__":
    logs = generate_logs()
    with open("synthetic_security_logs.json", "w") as f:
        json.dump(logs, f, indent=4)
    print("✅ Generated 15,000 mock security logs.")