# This class will handle communication with the GPT-3.5 AI model and sending requests to the OpenAI API.
import openai
import asyncio

OPENAI_API_KEY = "MY_API"

class GPTCommunicator:
    def __init__(self):
        #openai.api_key = os.getenv(OPENAI_API_KEY)
        openai.api_key = OPENAI_API_KEY
    async def send_prompt(self, prompt):
        # Asynchronously send prompt to the OpenAI API??await
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        #print(completion.choices[0].message.content)
        return completion


    def extract_response(self, api_response):
        # Extract AI's reply from the response
        ai_reply = api_response.choices[0].message.content
        return ai_reply
