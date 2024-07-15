from openai import OpenAI
import openai
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
def aiProcess(command):
    openai.api_key = "your key"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses, please"},
            {"role": "user", "content": command}
        ]
    )

    response['choices'][0]['message']['content']