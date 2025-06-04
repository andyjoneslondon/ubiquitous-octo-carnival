import openai
import os
import re
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = '''You are an assistant that receives transcribed voice input from taxi drivers.

Your task is to extract the user's intent and location from each input, and return a response ONLY as JSON. There are two possible intents:

- "report": when the driver provides information about something happening at a location (e.g. traffic, police, roadworks, protests, disruptions, events, news). Extract both the location and a short description as the status.
- "query": when the driver asks for information about a location. Extract only the location.

⚠️ Return ONLY raw JSON. Do not include any explanation, markdown, or other formatting — just the JSON object. No backticks. No prefix. No comments.

If it’s a report:
{ "intent": "report", "location": "Location Name", "status": "Short summary of what was reported" }

If it’s a query:
{ "intent": "query", "location": "Location Name" }

If the input is unclear, make your best guess based on context.
'''

def get_gpt_reply(text_input):
    try:
        print("📤 Sending to GPT:", repr(text_input))
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_input}
            ],
            temperature=0.3
        )
        reply_text = response.choices[0].message.content.strip()
        print("📥 GPT raw reply:", repr(reply_text))

        # First try plain {...}
        match = re.search(r"{[\s\S]*}", reply_text)
        if match:
            return match.group(0)

        # Try backtick code block fallback
        match = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", reply_text)
        if match:
            return match.group(1)

        print("❌ Could not find JSON block in GPT reply")
        return ""
    except Exception as e:
        print("GPT EXCEPTION:", e)
        return ""
