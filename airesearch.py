#!/usr/bin/env python3

import argparse
import os
import sys
from google import genai
from google.genai import types

MODEL = "models/gemini-2.5-flash"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Missing GEMINI_API_KEY")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def research_question(client, question):
    prompt = f"""
You are a research assistant.

Research the following question using current, reputable web sources.
Summarize the findings clearly and factually.
At the end, include a short list of sources with URLs.

Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ],
            temperature=0.3,
        ),
    )

    return response.text


def main():
    parser = argparse.ArgumentParser(
        description="AI Research CLI (Gemini + Google Search)"
    )
    parser.add_argument("question", help="Research question")
    args = parser.parse_args()

    print("🔎 Researching with Gemini + Google Search...")
    client = get_client()

    result = research_question(client, args.question)

    print("\n================= RESEARCH SUMMARY =================\n")
    print(result)


if __name__ == "__main__":
    main()
