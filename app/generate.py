import os

from dotenv import load_dotenv
from groq import Groq


# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()


# =========================================
# GET API KEY
# =========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================
# CREATE GROQ CLIENT
# =========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================
# GENERATE AI ANSWER
# =========================================

def generate_answer(question, chunks):

    # =========================================
    # EXTRACT CONTEXT SAFELY
    # =========================================

    context_parts = []

    for chunk in chunks:

        if isinstance(chunk, dict):

            text = (
                chunk.get("text")
                or chunk.get("content")
                or chunk.get("document")
                or chunk.get("page_content")
                or str(chunk)
            )

            context_parts.append(text)

        else:

            context_parts.append(str(chunk))

    context = "\n".join(context_parts)

    # =========================================
    # PROMPT
    # =========================================

    prompt = f"""
You are NovaMind AI,
an advanced AI-powered research intelligence and
technical document analysis system.

Your responsibility is to deeply analyze the provided
document context and generate highly detailed,
professionally structured, technically rich,
human-understandable answers.

You must behave like:
- a research analyst
- technical reviewer
- AI scientist
- academic paper explainer
- enterprise documentation assistant

STRICT RULES:

1. ONLY use information from the provided document context.
2. NEVER hallucinate or invent facts.
3. Use technical terminology from the document whenever available.
4. Explain all concepts deeply and clearly.
5. Convert complex technical ideas into understandable explanations.
6. Maintain professional formatting.
7. Use headings, subheadings, bullet points, and sections.
8. Mention important:
   - methodologies
   - architectures
   - pipelines
   - datasets
   - frameworks
   - evaluation metrics
   - workflows
   - algorithms
   - models
   - findings
   - technical components
9. Include numerical values and metrics whenever present.
10. If the answer involves a process,
    explain it step-by-step.
11. If the question asks for summary,
    generate a FULL research-style detailed summary.
12. Make responses feel like an expert technical report.
13. Use markdown-style formatting.
14. Keep answers highly informative and educational.
15. Explain WHY things are important, not just WHAT they are.
16. Explain relationships between system components.
17. Explain practical impact and real-world applications.
18. Mention limitations/challenges if present.
19. Highlight innovations or novel contributions.
20. Keep formatting visually structured and clean.

VERY IMPORTANT FORMATTING STYLE:

# Main Topic

## Objective

Detailed explanation...

## System Architecture

Detailed explanation...

## Methodology

Step-by-step explanation...

### Data Collection

...

### Processing Pipeline

...

### Model Architecture

...

## Technical Components

- Component
- Role
- Importance

## Algorithms / Models Used

Detailed explanation...

## Evaluation Metrics

- Metric
- Purpose
- Interpretation

## Key Findings

Detailed explanation...

## Technical Insights

Detailed explanation...

## Advantages

- Point
- Point

## Challenges / Limitations

- Point
- Point

## Real-World Applications

Detailed explanation...

## Conclusion

Comprehensive concluding explanation.

ADDITIONAL INSTRUCTIONS:

- Use professional but understandable language.
- Do NOT give short answers.
- Make the answer educational.
- Expand technical concepts thoroughly.
- Explain abbreviations when first introduced.
- Use examples from the document whenever possible.
- Maintain logical flow between sections.
- Make the response feel like a premium AI research assistant.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

PROFESSIONAL DETAILED RESPONSE:
"""

    # =========================================
    # GROQ API CALL
    # =========================================

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.6,
        max_tokens=2500
    )

    # =========================================
    # FINAL RESPONSE
    # =========================================

    final_answer = (
        response
        .choices[0]
        .message
        .content
    )

    return final_answer