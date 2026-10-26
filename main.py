import os
from pathlib import Path
from sarvamai import SarvamAI

# Read .env into environment variables without extra dependencies
env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))

api_key = os.environ.get("SARVAM_API_KEY")
if not api_key:
    raise SystemExit("Error: Please paste your SARVAM_API_KEY into the .env file first.")

client = SarvamAI(api_subscription_key=api_key)

response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[
        {"role": "user", "content": "Hello! Introduce yourself in one short sentence."}
    ],
)

print(response.choices[0].message.content)