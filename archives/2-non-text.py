import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What is in this image"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://res.cloudinary.com/dk0z4ums3/image/upload/v1661753019/attached_image/inilah-cara-merawat-anak-kucing-yang-tepat-0-alodokter.jpg"
                },
            },
        ],
    }
]

response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)

content = response.choices[0].message.content

print(content)
