import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = 'You are an assistant that receives transcribed voice input from taxi drivers.\n\nYour task is to extract the user\'s intent and location from each input, and return a response ONLY as JSON. There are two possible intents:\n\n- "report": when the driver provides information about something happening at a location (e.g. traffic, police, roadworks, protests, disruptions, events, news). Extract both the location and a short description as the status.\n- "query": when the driver asks for information about a location. Extract only the location.\n\n⚠️ Respond ONLY with raw JSON and NOTHING else — no markdown, no introduction, no explanation.\n\nIf it’s a report:\n{ "intent": "report", "location": "Location Name", "status": "Short summary of what was reported" }\n\nIf it’s a query:\n{ "intent": "query", "location": "Location Name" }\n\nIf the input is unclear, make your best guess based on context.\n'

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
        return reply_text
    except Exception as e:
        return str(e)
