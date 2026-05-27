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
an advanced AI-powered research and document assistant.

Your task is to deeply analyze the provided document context
and answer the user's question in a highly detailed,
well-structured, professional, and human-friendly manner.

VERY IMPORTANT INSTRUCTIONS:

- Give comprehensive explanations
- Explain concepts in depth
- Use proper headings and subheadings
- Use bullet points where useful
- Explain technical concepts clearly
- Add examples whenever possible
- Include interpretations and insights
- Write like a professional research assistant
- Make the answer educational and easy to understand
- Avoid very short responses
- Expand each important point properly
- Keep the response highly informative
- Structure the response professionally

RESPONSE STRUCTURE:

## Overview

## Detailed Explanation

## Key Concepts

## Technical Insights

## Important Findings

## Conclusion

Document Context:
{context}

User Question:
{question}

Now generate a highly detailed professional response.
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