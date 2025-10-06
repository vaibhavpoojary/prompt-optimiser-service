import json
from config import get_bedrock_client, MODEL_ID

def run_prompt(prompt: str, temperature: float, top_p: float, top_k: int, max_tokens: int) -> str:
    bedrock = get_bedrock_client()

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json"
        )
        result = json.loads(response["body"].read())
        return result["content"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ Error running prompt: {str(e)}"
