import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_reply(text_input):
    system_prompt = (
        "You are a helpful assistant for taxi drivers. Users report or ask about traffic. "
        "Always return a helpful response in plain English."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_input}
        ],
        temperature=0.5
    )
    return response['choices'][0]['message']['content']