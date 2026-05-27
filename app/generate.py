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
an advanced AI research assistant.

Answer the user's question ONLY using the provided context.

VERY IMPORTANT FORMATTING RULES:

- Use proper headings
- Use short paragraphs
- Avoid huge spacing
- Keep content clean and professional
- Use bullet points when needed
- Keep structure compact and readable
- Explain concepts clearly
- Do NOT leave empty lines unnecessarily

Use this structure whenever possible:

## Overview

## Key Findings

## Technical Details

## Important Concepts

## Conclusion

Context:
{context}

Question:
{question}

Answer:
"""

    # =========================================
    # GROQ API CALL
    # =========================================

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,
        max_tokens=1024
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