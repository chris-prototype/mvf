import subprocess

command = [
    "curl",
    "-X", "POST",
    "http://127.0.0.1:8000/webhook/linear",
    "-H", "Content-Type: application/json",
    "-d", '{"action": "create", "type": "Issue", "data": {"id": "ISS-123", "title": "Fix login bug"}}',
]

result = subprocess.run(command, capture_output=True, text=True, check=True)
print(result.stdout)