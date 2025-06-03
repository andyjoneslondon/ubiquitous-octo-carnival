import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = 'You are a helpful assistant that processes voice input from taxi drivers about specific locations.\n\nYour goal is to interpret each input and return structured JSON that identifies the user\'s intent and relevant location.\n\nThere are two types of intent:\n- "report": The user is providing information about something happening at a location (e.g., traffic, roadworks, police, accidents, events, disruptions, or local news). Extract the location and a brief summary of what they are reporting.\n- "query": The user is asking for an update or summary of the latest reports at a location. Extract the location only.\n\nAlways respond in JSON format like this:\n{\n  "intent": "report" or "query",\n  "location": "location name",\n  "summary": "short description"  ← only for reports\n}\n\nBe concise and consistent. The location should be a well-known area or landmark. If you\'re unsure, return a best guess based on context.\n'

def get_gpt_reply(text_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # You can change this to "gpt-3.5-turbo" if needed
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
