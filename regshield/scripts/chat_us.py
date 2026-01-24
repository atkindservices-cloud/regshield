import json
from regshield.agents.chat_agent import chat

with open("regshield/data/reports_us/company_report.json") as f:
    report = json.load(f)

print("🤖 RegShield Chat (type 'exit' to quit)")
while True:
    q = input("You: ")
    if q.lower() == "exit":
        break
    print("AI:", chat(q, report))
