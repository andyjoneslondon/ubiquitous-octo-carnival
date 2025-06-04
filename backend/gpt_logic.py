import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = "You are an assistant that receives transcribed voice input from taxi drivers. [...]"  # use your full prompt here

def get_gpt_reply(text_input):
    if not client.api_key:
        print("❌ No OpenAI API key set!")
        return ""

    print("📤 Sending to GPT:", repr(text_input))

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_input}
            ],
            temperature=0.3
        )
        reply_text = response.choices[0].message.content.strip()
        print("📥 GPT raw reply:", repr(reply_text))
        return reply_text
    except Exception as e:
        print("❌ GPT error:", e)
        return ""
