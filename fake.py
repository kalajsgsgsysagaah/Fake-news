import gradio as gr
import requests
import json
import os

print("Starting Fake News Detector App...")

# Get API key from environment variable
API_KEY = os.environ.get("API_KEY")

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

SYSTEM_PROMPT = """
You are a professional fact-checker.
Check whether the given news claim is true or false.
Explain clearly with reasoning.
Respond in clean markdown.
"""

def fact_check(claim):
    if not claim:
        return "⚠️ Please enter a news claim."

    if not API_KEY:
        return "❌ API_KEY not found. Set it in Railway variables."

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\nClaim:\n" + claim}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Build UI
with gr.Blocks(title="Fake News Detector") as demo:
    gr.Markdown("# 📰 Fake News Detector")
    gr.Markdown("Enter a claim to verify whether it is real or fake.")

    claim_input = gr.Textbox(
        label="News Claim",
        placeholder="Example: The Earth is flat."
    )

    check_button = gr.Button("Fact Check")
    output = gr.Markdown()

    check_button.click(fact_check, inputs=claim_input, outputs=output)


# Launch app
port = int(os.environ.get("PORT", 8080))

demo.launch(
    server_name="0.0.0.0",
    server_port=port,
    share=True   # you requested this
)
