#!/usr/bin/env python3

import argparse
import os
import sys
from openai import OpenAI

MODEL = "gpt-4.1-mini"


def read_input(text, file_path):
    if text:
        return text
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()

    print("❌ No input provided.")
    sys.exit(1)


def review_content(client, content, instructions):
    prompt = f"""
You are an expert reviewer.

Review the following content according to these instructions:
{instructions}

Content:
{content}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
    )

    return response.output_text


def main():
    parser = argparse.ArgumentParser(
        description="Universal AI Review Tool"
    )

    parser.add_argument(
        "-t", "--text",
        help="Text to review"
    )

    parser.add_argument(
        "-f", "--file",
        help="File to review"
    )

    parser.add_argument(
        "-i", "--instructions",
        default="Provide a clear, honest, and constructive review.",
        help="How the content should be reviewed"
    )

    parser.add_argument(
        "-o", "--out",
        help="Save review to file"
    )

    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Missing OPENAI_API_KEY")
        sys.exit(1)

    content = read_input(args.text, args.file)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("🧠 Reviewing...")
    review = review_content(client, content, args.instructions)

    print("\n================= REVIEW =================\n")
    print(review)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(review)
        print(f"\n📄 Review saved to: {args.out}")


if __name__ == "__main__":
    main()
