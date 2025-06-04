import openai
import os

# Initialize client using new SDK structure
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Stricter system prompt (as previously successful)
system_prompt = (
    "You are an assistant that receives transcribed voice input from taxi drivers.\n\n"
    "Your task is to extract the user's intent and location from each input, and return a response ONLY as JSON.\n\n"
    "There are two possible intents:\n"
    "- \"report\": when the driver provides information about something happening at a location "
    "(e.g. traffic, police, roadworks, protests, disruptions, events, news). Extract both the location and a short description as the status.\n"
    "- \"query\": when the driver asks for information about a location. Extract only the location.\n\n"
    "⚠️ Respond ONLY with raw JSON and NOTHING else — no markdown, no introduction, no explanation.\n\n"
    "If it’s a report:\n"
    "{ \"intent\": \"report\", \"location\": \"Location Name\", \"status\": \"Short summary of what was reported\" }\n\n"
    "If it’s a query:\n"
    "{ \"intent\": \"query\", \"location\": \"Location Name\" }\n\n"
    "If the input is unclear, make your best guess based on context."
)

def get_gpt_reply(text_input):
    if not client.api_key:
        print("❌ No OpenAI API key set!")
        return ""

    print("📤 Sending to GPT:", repr(text_input))
    print("🔑 Using OpenAI key:", client.api_key[:6] + "...")

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": text_input }
            ],
            temperature=0.3
        )
        reply_text = response.choices[0].message.content.strip()
        print("📥 GPT raw reply:", repr(reply_text))
        return reply_text
    except Exception as e:
        print("❌ GPT error:", e)
        return ""
