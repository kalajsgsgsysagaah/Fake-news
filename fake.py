import gradio as gr
import json
import requests
import os
import time

API_KEY = os.environ.get("API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="

SYSTEM_INSTRUCTION = {
    "parts": [
        {
            "text": """
You are a professional fact-checker.
Verify the claim using Google Search grounding.
Provide citations.
Respond in markdown.
"""
        }
    ]
}

def check_news(news_claim):
    if not news_claim:
        return "Please enter a claim."

    payload = {
        "contents": [{"parts": [{"text": news_claim}]}],
        "systemInstruction": SYSTEM_INSTRUCTION,
        "tools": [{"google_search": {}}]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            f"{API_URL}{API_KEY}",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        result = response.json()

        candidate = result.get("candidates", [])[0]
        text_response = candidate.get("content", {}).get("parts", [])[0].get("text", "No response.")

        return text_response

    except Exception as e:
        return f"Error: {e}"


with gr.Blocks(title="Fake News Detection") as demo:
    gr.Markdown("# Fake News Detection")
    gr.Markdown("Enter a news claim and verify it using live Google Search grounding.")

    text_input = gr.Textbox(label="News Claim")
    button = gr.Button("Fact Check")
    output = gr.Markdown()

    button.click(check_news, inputs=text_input, outputs=output)


port = int(os.environ.get("PORT", 7860))

demo.launch(
    server_name="0.0.0.0",
    server_port=port,
    theme=gr.themes.Soft()
)
