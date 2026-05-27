from app.generate import generate_answer


def generate_dashboard(chunks):

    text = "\n".join(
        str(chunk)
        for chunk in chunks
    )


    summary_prompt = f"""
Summarize this document professionally
in 5-6 lines.

Document:
{text}
"""


    findings_prompt = f"""
Give key findings from this document
in bullet points.

Document:
{text}
"""


    concepts_prompt = f"""
Extract important concepts/topics
from this document.

Document:
{text}
"""


    summary = generate_answer(
        summary_prompt,
        chunks
    )

    findings = generate_answer(
        findings_prompt,
        chunks
    )

    concepts = generate_answer(
        concepts_prompt,
        chunks
    )


    analytics = f"""
• Total Chunks: {len(chunks)}
• AI Processing: Successful
• Semantic Search: Enabled
• LLM Model: LLaMA 3
"""


    return {
        "summary": summary,
        "findings": findings,
        "concepts": concepts,
        "analytics": analytics
    }