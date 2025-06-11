from google import genai
import click
import pypandoc
import sys
import re
from os import environ
import urllib.request


@click.group()
def cli():
    """pghaicker cli interface"""
    pass


@cli.command()
@click.argument("thread_id", nargs=1)
@click.option("-s", "--system_prompt", required=False,
              default=f"Summarize the following thread."
                      f"Be explicit about potential decision points and blockers."
                      f"If there's a decision to be made, say so.")
@click.option("-m", "--model", required=True, default='gemini-2.0-flash', help="default: gemini-2.0-flash")
def summarize(thread_id, system_prompt, model):
    """Download thread HTML, convert to Markdown, and summarize with Gemini."""

    # Check if input is a URL
    if re.match(r"^https?://", thread_id):
        url = thread_id

    else:
        try:
            # if passed int it's from the PgPro archives
            int(thread_id)
            # Step 1: Fetch HTML using urllib3 with a browser-like User-Agent
            url = f"https://postgrespro.com/list/thread-id/{thread_id}"
        except ValueError:
            url = f"https://www.postgresql.org/message-id/flat/{thread_id}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise RuntimeError(f"Failed to fetch thread. Status code: {response.status}")
            html_content = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP error occurred: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error occurred: {e.reason}")

    # Step 2: Convert HTML to Markdown using pypandoc
    markdown = pypandoc.convert_text(html_content, 'md', format='html')

    # Step 3: Send Markdown to Gemini for summarization
    gemini_input = f"{system_prompt}\n\n{markdown}"

    client = genai.Client(
        api_key=environ.get('GOOGLE_API_KEY') or environ.get('GEMINI_API_KEY')
    )

    summary_response = client.models.generate_content(
        model=model,
        contents=gemini_input
    )

    print(summary_response.text, file=sys.stdout)
