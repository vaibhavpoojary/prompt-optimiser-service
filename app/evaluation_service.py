import json
import re
from config import get_bedrock_client, MODEL_ID

def evaluate_outputs(original_output: str, optimized_output: str) -> dict:
    bedrock = get_bedrock_client()

    eval_prompt = f"""
You are a neutral evaluator AI. Compare the two outputs below.
Rate them (1-10) for Clarity, Accuracy, Completeness, and Conciseness.
Then provide a final verdict. Return only JSON.

Original Output:
{original_output}

Optimized Output:
{optimized_output}

Return JSON only, exactly in this format:
{{
  "clarity": int,
  "accuracy": int,
  "completeness": int,
  "conciseness": int,
  "verdict": "string"
}}
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": eval_prompt}
        ],
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json"
        )
        result = json.loads(response["body"].read())
        text_output = result["content"][0]["text"]

        # Extract JSON from the output using regex
        match = re.search(r"\{.*\}", text_output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        # If extraction fails, return error and raw output
        return {"error": "Could not extract JSON", "raw_text": text_output}
    except Exception as e:
        return {"error": str(e)}
