from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_reply(text_input):
    system_prompt = (
        "You are a helpful assistant for taxi drivers. "
        "Users will either report a location status or ask about one. "
        "Always respond ONLY in the following JSON format:\n\n"
        '{ "intent": "report", "location": "Oxford Street", "status": "heavy traffic" }\n'
        'OR\n'
        '{ "intent": "query", "location": "Oxford Street" }'
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_input}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
