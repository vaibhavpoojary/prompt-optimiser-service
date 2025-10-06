import json
from config import bedrock, MODEL_ID

DETAILED_OPTIMIZER_PROMPT = """
You are an expert Prompt Optimizer for Large Language Models (LLMs).

Your goal: Rewrite and enhance the user's input prompt to maximize clarity, specificity, and effectiveness for LLMs such as Claude, GPT, or similar.

Instructions:
- Analyze the user's raw prompt and identify ambiguities, missing context, or unclear instructions.
- Rewrite the prompt in a structured format with the following sections:
    Role: Clearly define the persona or expertise the LLM should assume.
    Task: Specify the exact task or question the LLM should address.
    Constraints: List any requirements, limitations, or formatting rules.
    Output: Describe the expected output format and level of detail.
    Checks: Suggest validation criteria or self-checks for the LLM to ensure quality.

Best Practices:
- Use explicit instructions and avoid vague language.
- Add relevant context or examples if missing.
- Ensure the prompt is actionable and unambiguous.
- If the prompt is for code, specify language, libraries, and input/output formats.
- If the prompt is for analysis, specify the scope, data, and expected insights.

Example Input:
"Summarize the following article."

Example Output:
Role: Expert summarizer.
Task: Summarize the provided article in 3 concise paragraphs.
Constraints: Use only information from the article; avoid personal opinions.
Output: A summary in clear, academic English.
Checks: Ensure the summary covers all main points and is under 300 words.
"""


def optimize_prompt(raw_prompt: str, temperature: float = 0.5, top_p: float = 0.9, top_k: int = 50, max_tokens: int = 2098) -> str:
    """Optimize a raw prompt using Claude Sonnet on Bedrock."""

    prompt_string = f"{DETAILED_OPTIMIZER_PROMPT}\n\nUser prompt:\n{raw_prompt}"

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": prompt_string}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType='application/json'
        )
        response_body = json.loads(response['body'].read())
        return response_body.get('content', [{}])[0].get('text', '').strip()
    except Exception as e:
        return f"Error optimizing prompt: {str(e)}"