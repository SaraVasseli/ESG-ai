from typing import List, Tuple, Dict, Any
from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL
from .models import GenerateDisclosureRequest

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an ESG reporting assistant.
You help sustainability teams draft disclosure-ready ESG narrative
based on structured ESG metrics and frameworks such as CSRD, SASB, GRI, and CDP.

Use clear business English, avoid greenwashing, and be specific and realistic.
"""


def _build_user_prompt(payload: GenerateDisclosureRequest) -> str:
    frameworks_str = ", ".join(payload.frameworks) or "general ESG best practices"

    metrics_lines: List[str] = []
    for m in payload.metrics:
        unit = f" {m.unit}" if m.unit else ""
        metrics_lines.append(f"- {m.name}: {m.value}{unit}")
    metrics_str = "\n".join(metrics_lines) or "- No metrics provided."

    if payload.tone == "regulatory":
        tone_instruction = (
            "Write in a formal, compliance-oriented tone appropriate for a sustainability report "
            "or regulatory filing."
        )
    else:
        tone_instruction = (
            "Write in a concise, investor-friendly tone focusing on financial relevance, "
            "strategy, and risk management."
        )

    return f"""
Company: {payload.company_name}
Sector: {payload.sector}
Year: {payload.year}
Frameworks to keep in mind: {frameworks_str}

Key metrics:
{metrics_str}

Initiatives and highlights (internal notes from the sustainability team):
{payload.initiatives}

Task:
1. Draft a 2–3 paragraph ESG disclosure section that could be used in a sustainability/ESG report.
2. Where appropriate, mention alignment with the specified frameworks in plain language (no legal boilerplate).
3. Be realistic and avoid over-claiming or promotional language.

{tone_instruction}

After the disclosure, add a short section titled "Suggestions for Improvement"
with 3–5 bullet points describing how the disclosure or underlying performance could improve.
"""


def generate_disclosure(
    payload: GenerateDisclosureRequest,
) -> Tuple[str, List[str], Dict[str, Any]]:
    """
    Calls the LLM and returns:
    - disclosure_text
    - improvement_suggestions (list of strings)
    - usage (dict with token usage & model info)
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    user_prompt = _build_user_prompt(payload)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )

    full_text = completion.choices[0].message.content or ""

    # --- Parse disclosure and suggestions ---
    marker = "Suggestions for Improvement"
    if marker in full_text:
        before, after = full_text.split(marker, 1)
        disclosure_text = before.strip()
        suggestions_block = after
    else:
        disclosure_text = full_text.strip()
        suggestions_block = ""

    suggestions: List[str] = []
    for line in suggestions_block.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "•", "*")):
            suggestions.append(stripped.lstrip("-•* ").strip())

    # --- Extract usage info safely ---
    usage: Dict[str, Any] = {
        "model": getattr(completion, "model", OPENAI_MODEL),
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }

    if getattr(completion, "usage", None) is not None:
        # For OpenAI chat completions, usage typically has prompt_tokens, completion_tokens, total_tokens
        usage["prompt_tokens"] = getattr(completion.usage, "prompt_tokens", None)
        usage["completion_tokens"] = getattr(completion.usage, "completion_tokens", None)
        usage["total_tokens"] = getattr(completion.usage, "total_tokens", None)

    # --- Log to server console ---
    print(
        "[ESG-ai] LLM usage:",
        f"model={usage['model']}, "
        f"prompt_tokens={usage['prompt_tokens']}, "
        f"completion_tokens={usage['completion_tokens']}, "
        f"total_tokens={usage['total_tokens']}",
    )

    return disclosure_text, suggestions, usage