from os import environ
import sys

import click
from google import genai

client = genai.Client()


@click.group()
def cli():
    """pghaicker cli interface"""
    pass


@cli.command()
@click.argument("thread_id", nargs=1)
def summarize(thread_id):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="Summarize the following thread " + sys.stdin.read()
    )
    print(response.text)
