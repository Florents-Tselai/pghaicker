from os import environ
import sys

import click
from google import genai
import click
import pypandoc
import sys
import urllib3

client = genai.Client()


@click.group()
def cli():
    """pghaicker cli interface"""
    pass


@cli.command()
@click.argument("thread_id", nargs=1)
def summarize(thread_id):
    """Download thread HTML, convert to Markdown, and summarize with Gemini."""

    # Step 1: Fetch HTML using urllib3 with a browser-like User-Agent
    url = f"https://postgrespro.com/list/thread-id/{thread_id}"
    http = urllib3.PoolManager(headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    })
    response = http.request("GET", url)

    if response.status != 200:
        raise RuntimeError(f"Failed to fetch thread. Status code: {response.status}")

    html_content = response.data.decode("utf-8")

    # Step 2: Convert HTML to Markdown using pypandoc
    markdown = pypandoc.convert_text(html_content, 'md', format='html')

    # Step 3: Send Markdown to Gemini for summarization
    gemini_input = f"Summarize the following thread:\n\n{markdown}"
    summary_response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=gemini_input
    )

    print(summary_response.text)
