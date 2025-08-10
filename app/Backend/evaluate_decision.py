import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_decision(query, clauses):
    prompt = f"""
You are an expert policy analyst. Based on the following query and clauses, determine:
1. Whether the query is approved or rejected.
2. If approved, what is the payout amount.
3. Justify your decision by referencing specific clauses.
Query: {query}
Clauses:
{chr(10).join(f"- {clause}" for clause in clauses)}
Return the result in JSON format with fields: status, amount, justification.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        output = response['choices'][0]['message']['content'].strip()
        result = json.loads(output)
        return {
            "status": result.get("status", "unknown"),
            "amount": result.get("amount", None),
            "justification": result.get("justification", "No justification provided.")
        }
    except json.JSONDecodeError:
        return {
            "status": "error",
            "amount": None,
            "justification": f"GPT response was not valid JSON:\n{output}"
        }
    except Exception as e:
        return {
            "status": "error",
            "amount": None,
            "justification": f"Failed to process GPT response: {str(e)}"
        }