#!/usr/bin/env bash

set -euo pipefail

DEFAULT_MODEL="gemini-2.0-flash"

function usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <THREAD_URL>

Fetch a thread, convert it to Markdown, and summarize it using Gemini.

Options:
  -m, --model MODEL     Gemini model to use (default: $DEFAULT_MODEL)
  -h, --help            Show this help message

Environment:
  GEMINI_API_KEY must be set.

Example:
  $0 -m gemini-1.5-pro https://example.com/thread.html
EOF
}

function get_thread_markdown() {
    local thread_id="$1"
    curl -sL "$thread_id" | pandoc --from html --to markdown
}

function gemini_summarize() {
    local input_text="$1"
    local model="$2"

    local json_safe_text
    json_safe_text=$(printf '%s' "$input_text" | jq -Rs .)

    local response
    response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d "{
              \"contents\": [
                {
                  \"parts\": [
                    { \"text\": $json_safe_text }
                  ]
                }
              ]
            }")

    echo "$response" | jq -r '.candidates[0].content.parts[0].text // "No summary returned."'
}

# Parse args
model="$DEFAULT_MODEL"
thread_url=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--model)
            model="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            exit 1
            ;;
        *)
            thread_url="$1"
            shift
            ;;
    esac
done

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
    echo "Error: GEMINI_API_KEY is not set." >&2
    exit 1
fi

if [[ -z "$thread_url" ]]; then
    echo "Error: THREAD_URL is required." >&2
    usage
    exit 1
fi

# Main logic
markdown=$(get_thread_markdown "$thread_url")
gemini_summarize "$markdown" "$model"