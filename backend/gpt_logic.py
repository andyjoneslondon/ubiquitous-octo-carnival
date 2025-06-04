import openai
import os
import re
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = '''You are an assistant that receives transcribed voice input from taxi drivers.

Your task is to extract the user's intent and location from each input, and return a response ONLY as JSON. There are two possible intents:

- "report": when the driver provides information about something happening at a location (e.g. traffic, police, roadworks, protests, disruptions, events, news). Extract both the location and a short description as the status.
- "query": when the driver asks for information about a location. Extract only the location.

⚠️ Respond ONLY with raw JSON and NOTHING else — no markdown, no introduction, no explanation.

If it’s a report:
{ "intent": "report", "location": "Location Name", "status": "Short summary of what was reported" }

If it’s a query:
{ "intent": "query", "location": "Location Name" }

If the input is unclear, make your best guess based on context.
'''

def get_gpt_reply(text_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": text_input }
            ],
            temperature=0.3
        )
        reply_text = response.choices[0].message.content.strip()
        print("GPT raw reply:", repr(reply_text))

        # Extract the first JSON-like block from GPT's reply
        match = re.search(r"{.*?}", reply_text, re.DOTALL)
        if match:
            json_block = match.group(0)
            return json_block
        else:
            print("❌ Could not find JSON block in GPT reply")
            return ""
    except Exception as e:
        print("GPT EXCEPTION:", e)
        return ""
