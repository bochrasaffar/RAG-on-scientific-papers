from openai import OpenAI
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))



def prepare_messages(paragraphs, question):
    messages = [
        {"role": "system", "content": "You are an expert in responding to questions related to scientific papers."},
        {"role": "user",
         "content": "Generate an answer the following question based on the provided paragraphs that were previously extracted by a retrieval, do not mention which paragraph were used to answer:"}
    ]
    
    for idx, paragraph in enumerate(paragraphs, start=1):
        messages.append({"role": "user", "content": f"Paragraph {idx}: {paragraph}"})
    
    # Add the question
    messages.append({"role": "user", "content": f"Question: {question}"})
    
    return messages

def generate_answer(paragraphs,question):
    messages = prepare_messages(paragraphs,question)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature= 0.2,
    max_tokens=150
    )
    x = completion.choices[0].message
    return x.content