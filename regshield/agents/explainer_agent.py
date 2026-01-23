from pathlib import Path
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(temperature=0)

def explain_failure(rule_name, questions, status):
    prompt = f"""
You are a US compliance advisor.

Rule: {rule_name}
Audit Questions:
{questions}

Audit Status: {status}

Explain:
1. Why this failed
2. What evidence is missing
3. Exact steps to become compliant
"""
    resp = llm([HumanMessage(content=prompt)])
    return resp.content
