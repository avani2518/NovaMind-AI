import os

from dotenv import load_dotenv
from groq import Groq


# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()


# =========================================
# GROQ CLIENT
# =========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================
# GENERATE SMART QUESTIONS
# =========================================

def generate_suggested_questions(chunks):

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


    # LIMIT CONTEXT SIZE
    context = "\n".join(context_parts[:8])


    prompt = f"""
You are NovaMind AI.

Analyze the uploaded document context carefully.

Your task:
Generate 5 highly relevant and natural questions
that a normal user would realistically ask
about this document.

IMPORTANT RULES:
- Questions MUST adapt to the document type
- Questions should be useful and meaningful
- Avoid overly technical questions unless necessary
- Questions should sound human and practical
- Keep questions concise
- Make them diverse
- Return ONLY questions
- One question per line
- No numbering
- No bullet points

Examples of GOOD questions:
- What is the main purpose of this document?
- Summarize the key findings
- What technologies are discussed?
- Explain the methodology used
- What are the important takeaways?

Document Context:
{context}
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.7,
        max_tokens=300
    )


    output = (
        response
        .choices[0]
        .message
        .content
    )


    questions = []

    for line in output.split("\n"):

        cleaned = (
            line
            .strip()
            .replace("-", "")
            .replace("*", "")
            .strip()
        )

        if cleaned:

            questions.append(cleaned)


    return questions[:5]